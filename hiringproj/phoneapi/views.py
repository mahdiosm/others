from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from phoneapi.forms import PhoneForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # return to where the user was before logging in
                # get the next query in url
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'phoneapi/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def success_view(request):
    return render(request, 'phoneapi/success.html')


@login_required
def index(request):
    if request.method == "GET":
        # create a form
        form = PhoneForm()
        return render(request, "phoneapi/index.html", {"form": form})
    elif request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("success_add_phone"))
        return render(request, "phoneapi/index.html", {"form": form})
