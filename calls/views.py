from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.urls import reverse

from calls.actions.export_xlsx import export_xlsx
from calls.forms.called_form import AuthorCalledForm, AuthorPassForm
from calls.models import Called, Pass_point

from .forms import LoginForm

# Create your views here.

def envia_email(request):
    user = request.POST.get('username')
    description = request.POST.get('description')
    send_mail(user,description, 'getugbr@gmail.com', ['jonh.getus@gmail.com'], fail_silently=False,)
    messages.success(request, 'Passagem enviada!')

    return redirect('pass_dashboard')

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
    search = request.GET.get('search')
    if search:
        called = called.filter(user_requester__icontains=f'{search}')
    return render(request, 'dashboard.html', context={
        'calleds': called,
    })

def exportar_chamados_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Called'
    filename = 'lista_chamados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Called.objects.all().values_list(
        'title',
        'user_requester',
        'priority__name',
        'is_resolved',
        'author__first_name',
        'category__name',
        'call_defect',
        'description',
        'pendencies',
        'created_at',
    )
    columns = ('Titulo', 'Usuario Solicitante','Prioridade','Resolvido','Técnico','Setor','Defeito Relatado','Solução Aplicada','Pendencias','Data de Abertura')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

def exportar_registros_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Pass_point'
    filename = 'lista_registros.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Pass_point.objects.all().values_list(
        'author__first_name',
        'created_at',
        'description',
    )
    columns = ('Técnico', 'Data','Registro')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

@login_required(login_url='login', redirect_field_name='next')
def dashboard_all(request):
    called = Called.objects.all(
    ).order_by('-id')
    return render(request, 'dashboard_all.html', context={
        'calleds': called,
    })

@login_required(login_url='login', redirect_field_name='next')
def dashboard_called_new(request):
    form = AuthorCalledForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        called: Called = form.save(commit=False)

        called.author = request.user
        called.created_at = datetime.now()

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
def pass_dashboard(request):
    point = Pass_point.objects.all().order_by('-id')
    search = request.GET.get('search')
    if search:
        point = point.filter(created_at__icontains=f'{search}')
    return render(request, 'pass_dashboard.html', context= {
        'points': point,
    })

@login_required()
def pass_add(request):
    form = AuthorPassForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        point: Pass_point = form.save(commit=False)

        point.author = request.user
        point.created_at = datetime.now()

        point.save()

        messages.success(request,'Passagem registrada!')
        return redirect(reverse('pass_dashboard'))
    
    return render(request, 'new_pass.html', context= {
        'form': form
    })

@login_required(login_url='login', redirect_field_name='next')
def pass_view(request, id):
    pass_view = get_object_or_404(Pass_point, pk=id)
    return render(request, 'pass_view.html', context={
        'pass_view': pass_view,
    })

@login_required(login_url='login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('login'))

    logout(request)
    return redirect(reverse('login'))