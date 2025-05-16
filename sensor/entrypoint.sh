#!/bin/sh
set -e

# 1) Bật đăng nhập root và mật khẩu
sed -i 's|#PermitRootLogin prohibit-password|PermitRootLogin yes|' /etc/ssh/sshd_config
sed -i 's|#PasswordAuthentication yes|PasswordAuthentication yes|' /etc/ssh/sshd_config

# 2) Tạo thư mục mô phỏng thiết bị IoT
mkdir -p /etc/iot /var/log/iot /opt/iot /firmware /scripts /etc/ssl/iot /var/www/html /data

# 3) Tạo các file giả lập thiết bị
touch /etc/iot/config.conf \
      /etc/systemd/system/iot-service.service \
      /scripts/test_script.sh \
      /data/readme.txt

# 4) Tạo user nếu chưa có
if ! id -u "${SSH_USER}" >/dev/null 2>&1; then
    useradd -m -s /bin/bash "${SSH_USER}"
fi
echo "${SSH_USER}:${SSH_PASS}" | chpasswd

# 5) Tạo host key nếu chưa có
[ ! -f /etc/ssh/ssh_host_rsa_key ] && ssh-keygen -A

# 6) Ghi file thông tin thiết bị
cat <<EOF > /etc/device-info.conf
DEVICE_IP=${STATIC_IP}
SSH_USER=${SSH_USER}
SSH_PORT=22
EOF

# 7) In log thiết bị ra console
echo "===== DEVICE SERVER ====="
echo "→ IP nội bộ Docker: ${STATIC_IP}"
echo "→ SSH trên host: localhost:${HOST_SSH_PORT}"
echo "→ SSH user: ${SSH_USER}"
echo "========================="

# 8) Chạy SSH daemon ở foreground để container không thoát
exec /usr/sbin/sshd -D
