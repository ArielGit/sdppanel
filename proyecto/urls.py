from django.urls import path
from proyecto import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login2/', auth_views.LoginView.as_view(template_name='registration/login2.html'), name='login2'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('proyectos/', views.ProyectoListView.as_view(), name="proyectos"),
]
