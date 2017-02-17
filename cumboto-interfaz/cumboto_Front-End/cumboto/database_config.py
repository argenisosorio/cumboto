# coding=utf-8
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cumboto2017',
        'USER': 'administrador',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUESTS': True, # Crea transacciones en cada peticion de la vista
    }
}
