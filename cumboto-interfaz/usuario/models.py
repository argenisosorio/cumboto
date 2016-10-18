from __future__ import unicode_literals
from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Profile(models.Model):

    ## Establece la cedula de identidad del usuario
    cedula = models.CharField(
        max_length=8, help_text=("Cédula de Identidad del usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d]{7,8}+$',
                ("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 7 u 8 carácteres.")
            ),
        ]
    )

    ## Establece el canal donde labora el usuario
    canal = models.CharField(
        max_length=175, help_text=("Canal de televisión")
    )

    ## Establece el cargo del usuario
    cargo = models.CharField(
        max_length=175, help_text=("Cargo del usuario")
    )

    ## Establece el teléfono de contacto del usuario
    telefono = models.CharField(
        max_length=20, help_text=("Número telefónico de contacto con el usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d+-]+$',
                ("Número telefónico inválido. Solo se permiten números, y los signos + o -")
            ),
        ]
    )

    ## Establece la relación entre el usuario y el perfil
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",
        help_text=("Relación entre los datos de registro y el usuario con acceso al sistema")
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
