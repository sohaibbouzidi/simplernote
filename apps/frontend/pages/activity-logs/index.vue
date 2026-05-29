<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-semibold text-[#e6edf3]">Activity Logs</h1>
      <p class="text-sm text-[#8b949e]">Track note changes, task updates, and API usage.</p>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-[#8b949e]">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading activity logs...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-[#f85149]/50 bg-[#f85149]/10 p-6 text-center text-[#f85149]">
      <p>{{ error }}</p>
      <button @click="fetchLogs" class="mt-3 rounded-md bg-[#21262d] px-4 py-2 text-sm hover:bg-[#30363d]">Retry</button>
    </div>

    <div v-else-if="logs.length === 0" class="rounded-lg border border-dashed border-[#21262d] p-12 text-center">
      <svg class="mx-auto h-8 w-8 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <h3 class="mt-3 font-semibold text-[#e6edf3]">No activity yet</h3>
      <p class="mt-1 text-sm text-[#8b949e]">Activity will appear here as you use the app.</p>
    </div>

    <div v-else class="rounded-lg border border-[#21262d] divide-y divide-[#21262d]">
      <div v-for="entry in logs" :key="entry.id" class="flex items-center gap-3 px-5 py-3 text-sm hover:bg-[#161b22]">
        <div class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#21262d]">
          <svg class="h-3 w-3 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <div class="min-w-0 flex-1">
          <span class="font-medium text-[#e6edf3]">{{ entry.action }}</span>
          <span class="text-[#8b949e]"> on {{ entry.entity_type }}</span>
        </div>
        <span class="shrink-0 text-xs text-[#8b949e]">{{ formatDate(entry.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const logs = ref<any[]>([])
const loading = ref(true)
const error = ref("")

function formatDate(d: string) {
  if (!d) return ""
  const date = new Date(d)
  const now = new Date()
  const diff = (now.getTime() - date.getTime()) / 1000
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })
}

async function fetchLogs() {
  loading.value = true; error.value = ""
  try { logs.value = (await api.get("/activity-logs")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load logs"; logs.value = [] }
  finally { loading.value = false }
}

onMounted(fetchLogs)
</script>
