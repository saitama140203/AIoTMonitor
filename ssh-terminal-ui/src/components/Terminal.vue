<template>
  <div ref="termContainer" class="terminal"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'

const termContainer = ref(null)
let term, ws

// Lấy config từ env
const WS_URL   = import.meta.env.VITE_WS_URL   // "ws://localhost:8000/api/v1/ssh"
const SSH_HOST = import.meta.env.VITE_SSH_HOST // "localhost"
const SSH_PORT = Number(import.meta.env.VITE_SSH_PORT) || 2222
const SSH_USER = import.meta.env.VITE_SSH_USER // "root"
const SSH_PASS = import.meta.env.VITE_SSH_PASS // "secret123"
const SSH_ID = import.meta.env.VITE_SSH_ID // "secret123"
onMounted(() => {
  // Khởi xterm
  term = new Terminal({ cols: 80, rows: 24 })
  term.open(termContainer.value)
  term.write('\x1b[32m⏳ Đang kết nối WebSocket tới SSH-proxy...\x1b[0m\r\n')

  // Mở WebSocket tới FastAPI
  ws = new WebSocket(WS_URL)
  ws.onopen = () => {
    term.write('\x1b[32m✅ WebSocket đã kết nối\x1b[0m\r\n')
    term.write(`\x1b[36m→ SSH: ${SSH_USER}@${SSH_HOST}:${SSH_PORT}\x1b[0m\r\n\n`)

    // Gửi payload SSH đến FastAPI
    ws.send(JSON.stringify({
      host: SSH_HOST,
      port: SSH_PORT,
      username: SSH_USER,
      password: SSH_PASS,
      profile_id:SSH_ID
    }))

    // Tự động chạy lệnh show cấu hình device
    setTimeout(() => {
      term.write('\r\n\x1b[33m→ Chạy: cat /etc/device-info.conf\x1b[0m\r\n')
      ws.send('cat /etc/device-info.conf\n')
    }, 500)
  }

  ws.onmessage = evt => {
    term.write(evt.data)
  }
  ws.onclose = () => {
    term.write('\r\n\x1b[31m🔌 WebSocket đã đóng\x1b[0m\r\n')
  }
  ws.onerror = err => {
    console.error(err)
    term.write('\r\n\x1b[31m❌ Lỗi WebSocket\x1b[0m\r\n')
  }

  // Khi người dùng gõ, đẩy thẳng đến SSH
  term.onData(data => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(data)
    }
  })
})

onUnmounted(() => {
  ws && ws.close()
  term && term.dispose()
})
</script>

<style scoped>
.terminal {
  width: 100%;
  height: 100%;
  background: black;
}
</style>
