FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    nano \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

# Tạo thư mục /app và copy file
WORKDIR /app
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Kiểm tra file đã được copy
RUN ls -la /app/entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/app/entrypoint.sh"]