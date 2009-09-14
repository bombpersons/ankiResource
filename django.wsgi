import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'ankiResource.settings_prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
