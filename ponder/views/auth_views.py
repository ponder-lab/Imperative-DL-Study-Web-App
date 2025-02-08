from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from ponder.forms import UserRegistrationForm
from ponder.models import Categorizer

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='Categorizer').exists() and not Categorizer.objects.filter(user=user).exists():
                    return HttpResponseRedirect('/categorizers/new')
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'ponder/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'ponder/register.html', {'form': form})

@login_required
def special(request):
    return HttpResponse("You are logged in")