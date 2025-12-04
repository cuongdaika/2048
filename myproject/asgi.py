import os
from django.core.asgi import get_asgi_application

# 1. Thiết lập biến môi trường ĐẦU TIÊN
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 2. Khởi tạo Django ASGI App ĐẦU TIÊN
# Dòng này bắt buộc phải chạy trước khi import game.routing
django_asgi_app = get_asgi_application()

# 3. BÂY GIỜ mới được import các thư viện Channels và code của bạn
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import game.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app, # Sử dụng biến đã khởi tạo ở trên
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns
        )
    ),
})