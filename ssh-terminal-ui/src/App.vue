<template>
  <div id="app" style="height:100vh; display:flex; flex-direction:column;">
    <header style="padding:10px; background:#222; color:#fff;">
      <h1 style="margin:0; font-size:1.2rem;">SSH Terminal</h1>
    </header>
    <main style="flex:1;">
      <Terminal />
    </main>
  </div>
</template>

<script setup>
import Terminal from './components/Terminal.vue'
</script>
