FROM python:3.10-slim

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn và script khởi động
COPY . .

# Gán quyền cho script khởi động
RUN chmod +x entrypoint.sh

# Biến môi trường
ENV PYTHONPATH=/app

# Cổng
EXPOSE 8000

# Chạy bằng entrypoint
ENTRYPOINT ["bash", "./entrypoint.sh"]

