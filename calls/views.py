import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from calls.forms.called_form import AuthorCalledForm
from calls.models import Called

from .forms import LoginForm

# Create your views here.

def login_view(request):
    form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'form_action': reverse('login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect(reverse('dashboard'))

        else:
            messages.error(request, 'Login ou senha incorretos.')

    return redirect(login_url)

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    return render(request, 'dashboard.html')