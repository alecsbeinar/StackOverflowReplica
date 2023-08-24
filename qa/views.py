from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from qa.forms import AskForm, AnswerForm
from qa.models import Question, Answer


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def main(request):
    if "popular" not in request.path:
        questions = Question.objects.new()
    else:
        questions = Question.objects.popular()
    limit = 2

    try:
        page = request.GET.get('page', 1)
    except ValueError:
        raise Http404

    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page='

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'user': request.user,
    }
    return render(request, 'qa/main.html', context)


@login_required
def single_question(request, number):
    question = get_object_or_404(Question, id=number)
    answers = Answer.objects.filter(question_id=number)
    is_auth_error = False
    form = AnswerForm()

    if request.method == "POST":
        author = request.user
        if author.is_authenticated:
            answer = Answer(author=author, question=question)
            form = AnswerForm(request.POST, instance=answer)
            form.save()
            return HttpResponseRedirect(request.path_info)
        else:
            is_auth_error = True

    context = {
        "question": question,
        "answers": answers,
        "form": form,
        "is_auth_error": is_auth_error,
    }
    return render(request, "qa/question.html", context)


@login_required
def ask_question(request):
    error = ''
    form = AskForm()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = AskForm(request.POST)
            form.author = request.user
            if form.is_valid():
                question = form.save()
                return HttpResponseRedirect(question.get_url())
        else:
            error = "You must be logged in to create a question."

    return render(request, 'qa/question_add.html', {
        'form': form,
        "error": error,
    })


