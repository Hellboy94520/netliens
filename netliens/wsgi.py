"""
WSGI config for netliens project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/django_project/app')
sys.path.append('/django_project/app/netliens')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netliens.settings')

application = get_wsgi_application()
