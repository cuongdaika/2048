import os
import django

# Thiết lập môi trường
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User


USERNAME = 'cuongdaika'
EMAIL = 'cuongdaika@gmail.com'
PASSWORD = '123'

def create_superuser():
    if User.objects.filter(username=USERNAME).exists():
        print(f"Admin {USERNAME} already exists.")
    else:
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"Superuser {USERNAME} created successfully!")

if __name__ == "__main__":
    create_superuser()