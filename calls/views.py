import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
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

@login_required(login_url='login', redirect_field_name='next')
def dashboard(request):
    called = Called.objects.filter(
    author=request.user
    ).order_by('-id')
    return render(request, 'dashboard.html', context={
        'calleds': called,
    })

@login_required(login_url='login', redirect_field_name='next')
def dashboard_all(request):
    called = Called.objects.all(
    ).order_by('-id')
    if request.POST.get('dashboard_all') == request.user.username:
        return render(request, 'dashboard_all.html', context={
            'calleds': called,
        })
    else:
        return render(reverse('login'))

@login_required(login_url='login', redirect_field_name='next')
def dashboard_called_new(request):
    form = AuthorCalledForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        called: Called = form.save(commit=False)

        called.author = request.user
        called.created_at = datetime.datetime.now()

        called.save()

        messages.success(request,'Chamado registrado!')
        return redirect(reverse('dashboard'))
    
    return render(request, 'new_called.html', context= {
        'form': form
    })

@login_required(login_url='login', redirect_field_name='next')
def dashboard_called_edit(request, id):
    called = Called.objects.get(
        author=request.user,
        pk=id,
        
    )

    if not called:
        raise Http404()

    form = AuthorCalledForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=called
    )

    if form.is_valid():
        called = form.save(commit=False)
        called.author = request.user
        form.save()
        messages.success(request,'Seu chamado foi alterado!')
        return redirect(reverse('dashboard'))

    return render(request,'edit_called.html', context={
        'calleds': called,
        'form': form,
    })

@login_required(login_url='login', redirect_field_name='next')
def called_view(request, id):
    called = get_object_or_404(Called, pk=id)
    return render(request, 'called_view.html', context={
        'called': called,
    })

@login_required(login_url='login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('login'))

    logout(request)
    return redirect(reverse('login'))