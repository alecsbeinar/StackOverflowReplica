from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from users.forms import RegisterForm, LoginForm, ProfileForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Registration succeed")
            return redirect("users:login")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {
        'form': form,
    })


def login_view(request):
    error = ''
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main_page")
        else:
            error = u'Incorrect login or password!'
    return render(request, 'users/login.html', {
        "error": error,
        "form": form,
    })


def logout_view(request):
    logout(request)
    url = request.GET.get('continue', '/')
    return HttpResponseRedirect(url)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect("users:profile")
    else:
        form = ProfileForm(instance=request.user)
    context = {
        "form": form,
        "user": request.user,
    }
    return render(request, "users/profile.html", context=context)
