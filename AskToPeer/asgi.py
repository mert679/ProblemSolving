"""
ASGI config for AskToPeer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os,django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AskToPeer.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import AskToPeerApp.routing 




application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
             AskToPeerApp.routing.websocket_urlpatterns
        )
    )
})
