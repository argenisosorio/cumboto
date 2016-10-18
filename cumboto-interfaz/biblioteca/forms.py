from django import forms
from django.forms import ModelForm
from biblioteca.models import registrar_app

class registrar_form(ModelForm):
    cargar_app = forms.FileField(
        label=("Cargar Aplicación"),
        widget=forms.FileInput(attrs={'class': 'filestyle',
                                      'type': 'file',
                                      'data-placeholder' : 'Archivos permitidos: .zip y .tar.gz',
                                      'data-buttonName' : 'btn-primary',
                                      'data-toggle': 'tooltip',
                                      'data-buttonText': 'Buscar archivo',
                                      'data-classInput' : 'input-small',
                                      #'data-size':'sm'

                                   }))

    class Meta:
        model = registrar_app
        fields=['cargar_app']
        