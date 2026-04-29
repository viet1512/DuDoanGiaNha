# Sử dụng hình ảnh với Python 3.8
FROM python:3.8-slim

# Cài đặt các dependencies
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Chạy ứng dụng
CMD ["python", "app.py"]
