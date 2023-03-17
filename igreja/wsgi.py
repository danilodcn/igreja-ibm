"""
configuração WSGI para o projeto.

Isso é exposto em uma variável ``application``.

Para mais informações, veja:
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "igreja.settings")

application: WSGIHandler = get_wsgi_application()
"""
aplicação wsgi
"""