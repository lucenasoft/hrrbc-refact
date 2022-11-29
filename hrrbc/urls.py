from django.contrib import admin
from django.urls import path

from calls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('create/', views.login_create, name='login_create'),
]
