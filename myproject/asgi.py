import os
from django.core.asgi import get_asgi_application

# 1. Thiết lập môi trường
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 2. Khởi động Django
django_asgi_app = get_asgi_application()

# --- ĐOẠN CODE MỚI: TỰ ĐỘNG TẠO ADMIN KHI SERVER KHỞI ĐỘNG ---
# (Chỉ chạy khi database trống hoặc mất admin do reset)
try:
    from django.contrib.auth.models import User
    if not User.objects.filter(username='cuongdaika').exists():
        print(">>> DANG TAO TAI KHOAN ADMIN... <<<")
        User.objects.create_superuser('cuongdaika', 'cuongdaika@gmail.com', 'matkhaucuaban') # <--- Đổi mật khẩu ở đây
        print(">>> TAO ADMIN THANH CONG! <<<")
    else:
        print(">>> ADMIN DA TON TAI <<<")
except Exception as e:
    print(f">>> LOI TAO ADMIN: {e} <<<")
# -------------------------------------------------------------

# 3. Import Channels (phải để sau khi Django khởi động)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import game.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns
        )
    ),
})