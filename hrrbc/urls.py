from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from calls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard/')),
    path('login/', views.login_view, name='login'),
    path('create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_all/', views.dashboard_all, name='dashboard_all'),
    path('dashboard/called/new', views.dashboard_called_new, name='called_new'),
    path('dashboard/called/<int:id>/edit/', views.dashboard_called_edit, name='called_edit'),
    path('export/xlsx', views.exportar_chamados_xlsx, name='export_xlsx'),
    path('export_pass/xlsx', views.exportar_registros_xlsx, name='export_pass_xlsx'),
    path('called/<int:id>/', views.called_view, name='called_view'),
    path('pass_dashboard/', views.pass_dashboard, name='pass_dashboard'),
    path('pass_dashboard/<int:id>/', views.pass_view, name='pass_view'),
    path('pass_dashboard/add', views.pass_add, name='pass_add')

]
