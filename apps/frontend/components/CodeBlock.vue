<template>
  <div class="group relative rounded-2xl border border-slate-700/50 bg-slate-950 overflow-hidden">
    <div class="flex items-center justify-between border-b border-slate-800 px-4 py-2">
      <span class="text-xs font-medium text-slate-500 uppercase tracking-wider">{{ lang }}</span>
      <button @click="copy" class="flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs text-slate-400 transition-all hover:bg-slate-800 hover:text-slate-200">
        <svg v-if="!copied" class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
        <svg v-else class="h-3.5 w-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
        <span :class="copied ? 'text-emerald-400' : ''">{{ copied ? 'Copied!' : 'Copy' }}</span>
      </button>
    </div>
    <pre class="overflow-x-auto p-4 text-sm leading-relaxed"><code class="text-slate-200">{{ code }}</code></pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"

const props = defineProps<{ code: string; lang?: string }>()

const copied = ref(false)

async function copy() {
  try {
    await navigator.clipboard.writeText(props.code)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // fallback for insecure contexts
    const ta = document.createElement("textarea")
    ta.value = props.code
    document.body.appendChild(ta)
    ta.select()
    document.execCommand("copy")
    document.body.removeChild(ta)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  }
}
</script>
