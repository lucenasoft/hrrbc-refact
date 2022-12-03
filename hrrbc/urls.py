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
    path('dashboard_all/', views.called_view, name='called_view'),
    path('dashboard/called/new', views.dashboard_called_new, name='called_new'),
    path('dashboard/called/<int:id>/edit/', views.dashboard_called_edit, name='called_edit'),
]
