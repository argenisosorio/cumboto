# coding=utf-8
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cumboto',
        'USER': 'cumboto',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True, # Crea transacciones en cada peticion de la vista
    }
}
