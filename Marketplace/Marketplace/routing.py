from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import Market.routing
import Chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Market.routing.websocket_urlpatterns +
            Chat.routing.websocket_urlpatterns
        )
    ),
})
