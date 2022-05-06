# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1673062/data/www/kazantracks.ru/routsweb')
sys.path.insert(1, '/var/www/u1673062/data/djangoenv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'routsweb.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()