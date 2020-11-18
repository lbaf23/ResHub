from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from ResHub.controller import WebSocket

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('websocketTest/<str:pk>', WebSocket.web_socket_connect),
        ])
    ),
})