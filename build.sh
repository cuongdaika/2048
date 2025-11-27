#!/usr/bin/env bash
# build.sh

# Exit ngay lập tức nếu có lỗi xảy ra
set -o errexit

# Cài đặt gói (Render đã làm, nhưng thêm vào để đảm bảo)
pip install -r requirements.txt

# Chạy migrate để tạo bảng
python manage.py migrate

# Thu thập Static files (Whitenoise)
python manage.py collectstatic --no-input