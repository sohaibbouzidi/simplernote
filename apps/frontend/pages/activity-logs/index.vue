<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-semibold text-white">Activity Logs</h1>
      <p class="text-slate-400">Track note changes, task updates, and API usage.</p>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading activity logs...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchLogs" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <div v-else-if="logs.length === 0" class="rounded-2xl border border-slate-800/50 bg-surface-50/50 p-12 text-center">
      <p class="text-3xl mb-4">🔍</p>
      <h3 class="font-display text-xl font-semibold text-white">No activity yet</h3>
      <p class="mt-2 text-sm text-slate-400">Activity will appear here as you use the app.</p>
    </div>

    <div v-else class="space-y-4">
      <div v-for="entry in logs" :key="entry.id" class="rounded-3xl border border-slate-800 bg-slate-950 p-5">
        <div class="flex items-center justify-between gap-4">
          <p class="font-semibold text-white">{{ entry.action }}</p>
          <span class="text-sm text-slate-400">{{ entry.created_at }}</span>
        </div>
        <p class="mt-2 text-slate-400">Entity: {{ entry.entity_type }} / {{ entry.entity_id || 'N/A' }}</p>
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

async function fetchLogs() {
  loading.value = true; error.value = ""
  try {
    const response = await api.get("/activity-logs")
    logs.value = response.data
  } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load activity logs"; logs.value = [] }
  finally { loading.value = false }
}

onMounted(fetchLogs)
</script>
