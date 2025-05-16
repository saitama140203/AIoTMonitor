FROM ubuntu:22.04

# Set noninteractive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# 1) Cài SSH server và nano editor
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       openssh-server \
       nano \
    && rm -rf /var/lib/apt/lists/*

# 2) Tạo thư mục cho sshd
RUN mkdir -p /var/run/sshd

# 3) Copy entrypoint script và grant execute
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 4) Open SSH port
EXPOSE 22

# 5) Start via entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]