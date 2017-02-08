#!/usr/bin/env python
# -*- coding: utf-8 -*-
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
