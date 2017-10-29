from django.shortcuts import render, redirect
from webacl.forms import LoginForm


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return redirect('webacl/login_success.html')
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}

    return render(request, 'webacl/login.html', context)


def login_success(request):
    context = {}

    return render(request, 'webacl/login_success.html', context)


def login_failure(request):
    context = {}

    return render(request, 'webacl/login_failure.html', context)