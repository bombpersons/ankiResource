import os, sys
import ankiResource.settings_prod
sys.path.append(ankiResource.settings_prod.SITE_ROOT)


os.environ['DJANGO_SETTINGS_MODULE'] = 'ankiResource.settings_prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
