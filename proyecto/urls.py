from django.urls import path
from proyecto import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('proyectos/', views.ProyectoListView.as_view(), name="proyectos"),
]
