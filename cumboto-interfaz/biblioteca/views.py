from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib import messages
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView
from biblioteca.forms import registrar_form


class registrar_view(CreateView):
    template_name= 'registro_app.html'
    form_class = registrar_form
    success_url = reverse_lazy('biblioteca:registrar-app')
   
    def registrar_valid(request):
        if request.method == 'POST':
            form = registrar_form(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('biblioteca:registrar-app')
        else:
            form = registrar_form()
            
        return render(request, 'registro_app.html',{'form':form}, context_instance=RequestContext(request))

