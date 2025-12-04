#!/usr/bin/env bash
# build.sh

# Exit ngay lập tức nếu có lỗi xảy ra
set -o errexit

# Cài đặt gói
pip install -r requirements.txt

# Chạy migrate để tạo bảng (quan trọng)
python manage.py migrate

# Thu thập Static files
python manage.py collectstatic --no-input

# --- PHẦN THÊM MỚI ---
# Chạy script tự động tạo Admin
python create_superuser.py