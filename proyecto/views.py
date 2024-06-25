from django.shortcuts import render
from django.views import generic
from proyecto.models import Proyecto 

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def inicio(request):
    return render(request, 'inicio.html',{})

class ProyectoListView(generic.ListView):
    model = Proyecto

    #    context_object_name = 'proyectos'
    #    queryset = Proyecto.objects.all()
    #    template_name = 'proyectos.html'

    template_name = 'proyectos.html'

    def get_context_data(self, **kwargs):
        proyectos = Proyecto.objects.all()
        context = super(ProyectoListView, self).get_context_data(**kwargs)
        context['proyectos'] = proyectos
        return context
