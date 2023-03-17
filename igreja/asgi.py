"""
configuração ASGI do projeto.

Isso é exposto em uma variável ``application``.

Para mais informações, veja:
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "igreja.settings")

application = get_asgi_application()
