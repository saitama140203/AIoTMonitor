<template>
  <div ref="termContainer" class="terminal h-full w-full"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, defineExpose } from 'vue'
import { Terminal as XTerminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import 'xterm/css/xterm.css'

const termContainer = ref<HTMLElement | null>(null)
let term: XTerminal | null = null
let fitAddon: FitAddon | null = null
let ws: WebSocket | null = null
let currentConfig: any = null

const WS_URL = import.meta.env.VITE_WS_URL

function scrollToBottom() {
  setTimeout(() => {
    if (termContainer.value) {
      termContainer.value.scrollTop = termContainer.value.scrollHeight
    }
  }, 10)
}

function initTerminal() {
  if (term) term.dispose()
  term = new XTerminal({
    cursorBlink: true,
    fontSize: 15,
    theme: { background: '#13131a', foreground: '#f4f4f4' }
  })
  fitAddon = new FitAddon()
  term.loadAddon(fitAddon)
  term.open(termContainer.value!)
  fitAddon.fit()
  setTimeout(() => fitAddon?.fit(), 20)
  term.writeln('🟢 Terminal sẵn sàng.\r\n')
  scrollToBottom()
  // Sự kiện resize gửi về backend
  term.onResize(({ cols, rows }) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "resize", cols, rows }))
    }
  })
}

function connect(config: any) {
  if (!config?.host) return
  ws?.close()
  currentConfig = config
  if (!term) initTerminal()
  else {
    term.clear()
    fitAddon?.fit()
  }
  ws = new WebSocket(WS_URL)
  ws.onopen = () => {
    ws!.send(JSON.stringify(config))
    // Gửi resize ngay khi connect
    if (term) {
      ws!.send(JSON.stringify({ type: "resize", cols: term.cols, rows: term.rows }))
    }
    term?.writeln(`\r\n🔗 Đã kết nối tới ${config.host}\r\n`)
    scrollToBottom()
  }
  ws.onmessage = e => {
    term?.write(e.data)
    scrollToBottom()
  }
  ws.onclose = () => {
    //term?.writeln('\r\n🔌 Đã ngắt kết nối')
    //scrollToBottom()
    let data = e.data;
    let parsed = null;

    // Thử parse JSON, nếu lỗi thì giữ nguyên text
    try {
      parsed = JSON.parse(data);
    } catch {
      parsed = null;
    }

    if (parsed && parsed.type === "terminate") {
      // Backend đã gửi lệnh terminate session
      term?.writeln('\r\n🔴 Phiên làm việc đã bị supervisor ngắt kết nối!\r\n')
      scrollToBottom()
      ws?.close()
      alert("Phiên làm việc đã bị supervisor ngắt kết nối!")
    } else if (typeof data === "string" && data.includes("Session terminated by supervisor")) {
      // Trường hợp server gửi message thuần text
      term?.writeln('\r\n🔴 Phiên làm việc đã bị supervisor ngắt kết nối!\r\n')
      scrollToBottom()
      ws?.close()
      alert("Phiên làm việc đã bị supervisor ngắt kết nối!")
    } else {
      // Bình thường thì in ra terminal
      term?.write(data)
      scrollToBottom()
    }
  }
  ws.onerror = e => {
    term?.writeln('\r\n⚠️ Lỗi kết nối')
    scrollToBottom()
    console.error(e)
  }
  term?.onData(d => ws?.send(d))
  scrollToBottom()
}

function disconnect() {
  ws?.close()
  term?.writeln('\r\n🔌 Đã đóng kết nối terminal')
  scrollToBottom()
}

defineExpose({ connect, disconnect })

onMounted(() => {
  initTerminal()
  scrollToBottom()
  window.addEventListener("resize", () => {
    fitAddon?.fit()
    // Gửi lại resize khi window resize
    if (term && ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "resize", cols: term.cols, rows: term.rows }))
    }
  })
})

onUnmounted(() => {
  ws?.close()
  term?.dispose()
})
</script>

<style scoped>
.terminal {
  background: #13131a;
  color: #fafafa;
  font-family: 'Fira Mono', 'Menlo', 'Consolas', 'Monaco', 'monospace';
  width: 100%;
  height: 100%;
  min-height: 280px;
  max-height: 520px;
  border-radius: 0.75rem;
  overflow-y: auto;
  padding: 0 !important;
}
</style>
