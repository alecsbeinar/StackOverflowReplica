from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages

from qa.forms import AskForm, AnswerForm, RegisterForm, LoginForm
from qa.models import Question, Answer, Session
from qa.tools import do_login


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
        'page': page
    }
    return render(request, 'qa/main.html', context)


def single_question(request, number):
    question = get_object_or_404(Question, id=number)
    answers = Answer.objects.filter(question_id=number)
    is_auth_error = False
    form = AnswerForm()

    if request.method == "POST":
        author = request.user
        if author is not None:
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


def ask_question(request):
    error = ''
    form = AskForm()
    if request.method == "POST":
        if request.user is not None:
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


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Registration succeed")
            return redirect("qa:login")
    else:
        form = RegisterForm()
    return render(request, 'qa/register.html', {
        'form': form,
    })


def login(request):
    error = ''
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        session = do_login(username, password)
        if session is not None:
            response = redirect("qa:main_page")
            response.set_cookie(
                'sessid', session.key,
                httponly=True,
                expires=session.expires
            )
            return response
        else:
            error = u'Incorrect login or password!'
    return render(request, 'qa/login.html', {
        "error": error,
        "form": form,
    })


def logout(request):
    sessid = request.COOKIES.get('sessid')
    if sessid is not None:
        Session.objects.filter(key=sessid).delete()
    url = request.GET.get('continue', '/')
    return HttpResponseRedirect(url)
