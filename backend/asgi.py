# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# import django
# django.setup()

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# import chat_app.routing

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),

#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat_app.routing.websocket_urlpatterns
#         )
#     ),
# })


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

import chat_app.routing

User = get_user_model()

@database_sync_to_async
def get_user(token_string):
    try:
        validated_token = AccessToken(token_string)
        return User.objects.get(id=validated_token['user_id'])
    except Exception:
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # சப்-ப்ரோட்டோகால்ஸ் மூலமாக ரியாக்ட் அனுப்பும் டோக்கனை பிரித்தல்
        subprotocols = scope.get('subprotocols', [])
        token = subprotocols[0] if subprotocols else None

        if token:
            scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()
            
        return await self.inner(scope, receive, send)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                chat_app.routing.websocket_urlpatterns
            )
        )
    ),
})