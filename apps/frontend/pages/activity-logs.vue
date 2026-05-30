<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-white">Activity Log</h1>
        <p class="mt-1 text-sm text-slate-400">Audit trail for all changes across your projects.</p>
      </div>
      <button v-if="logs.length" @click="fetchLogs" class="rounded-md border border-slate-800 bg-surface-50 px-3 py-1.5 text-sm text-slate-300 hover:bg-slate-700">
        Refresh
      </button>
    </div>

    <div class="flex flex-wrap gap-2">
      <button
        v-for="f in filters"
        :key="f.key"
        @click="activeFilter = f.key"
        :class="[
          'rounded-full px-3 py-1 text-xs font-medium transition-colors',
          activeFilter === f.key
            ? 'bg-brand-500/20 text-brand-400 border border-brand-500/30'
            : 'bg-slate-800 text-slate-400 border border-slate-700 hover:text-white'
        ]"
      >
        {{ f.label }}
      </button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-400">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading activity log...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-red-500/50 bg-red-500/10 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchLogs" class="mt-3 rounded-md bg-slate-800 px-4 py-2 text-sm hover:bg-slate-700">Retry</button>
    </div>

    <div v-else-if="filteredLogs.length === 0" class="rounded-lg border border-dashed border-slate-800 p-16 text-center">
      <svg class="mx-auto h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <p class="mt-3 text-sm font-medium text-white">No activity yet</p>
      <p class="mt-1 text-xs text-slate-400">Actions like creating notes, tasks, and projects will appear here.</p>
    </div>

    <div v-else class="rounded-lg border border-slate-800 overflow-hidden">
      <table class="w-full text-left text-sm">
        <thead class="bg-surface-50 text-slate-400">
          <tr>
            <th class="px-5 py-3 font-medium">Action</th>
            <th class="px-5 py-3 font-medium">Entity</th>
            <th class="px-5 py-3 font-medium hidden sm:table-cell">Details</th>
            <th class="px-5 py-3 font-medium text-right">When</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr v-for="log in filteredLogs" :key="log.id" class="hover:bg-surface-50 transition-colors">
            <td class="px-5 py-3">
              <div class="flex items-center gap-3">
                <span :class="actionIcon(log.action)" class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs">
                  {{ actionEmoji(log.action) }}
                </span>
                <span class="font-medium text-white capitalize">{{ log.action.replace(/_/g, " ") }}</span>
              </div>
            </td>
            <td class="px-5 py-3">
              <span :class="entityBadgeClass(log.entity_type)" class="rounded-full px-2.5 py-0.5 text-xs font-medium capitalize">{{ log.entity_type.replace(/_/g, " ") }}</span>
            </td>
            <td class="px-5 py-3 text-xs text-slate-400 hidden sm:table-cell max-w-xs truncate">
              {{ formatPayload(log) }}
            </td>
            <td class="px-5 py-3 text-right">
              <span class="text-xs text-slate-400" :title="new Date(log.created_at).toLocaleString()">{{ timeAgo(log.created_at) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()

const logs = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const activeFilter = ref("all")

const filters = [
  { key: "all", label: "All" },
  { key: "note", label: "Notes" },
  { key: "task", label: "Tasks" },
  { key: "project", label: "Projects" },
  { key: "api_key", label: "API Keys" },
]

const filteredLogs = computed(() => {
  if (activeFilter.value === "all") return logs.value
  return logs.value.filter((l) => l.entity_type === activeFilter.value)
})

function actionEmoji(action: string) {
  const map: Record<string, string> = {
    create: "+",
    update: "~",
    delete: "×",
  }
  return map[action] || "•"
}

function actionIcon(action: string) {
  const base = "bg-slate-800 text-slate-400"
  if (action === "create") return "bg-green-500/20 text-green-400 " + base
  if (action === "update") return "bg-amber-500/20 text-amber-400 " + base
  if (action === "delete") return "bg-red-500/20 text-red-400 " + base
  return base
}

function entityBadgeClass(type: string) {
  if (type === "note") return "bg-amber-500/20 text-amber-400 border border-amber-500/30"
  if (type === "task") return "bg-brand-500/20 text-brand-400 border border-brand-500/30"
  if (type === "project") return "bg-violet-500/20 text-violet-400 border border-violet-500/30"
  if (type === "api_key") return "bg-slate-800 text-slate-400 border border-slate-700"
  return "bg-slate-800 text-slate-400 border border-slate-700"
}

function formatPayload(log: any) {
  if (log.payload) {
    const p = log.payload
    if (p.title) return p.title
    if (p.name) return p.name
    if (p.email) return p.email
  }
  if (log.entity_id) return `ID: ${log.entity_id.slice(0, 8)}...`
  return "—"
}

function timeAgo(d: string) {
  const diff = (Date.now() - new Date(d).getTime()) / 1000
  if (diff < 60) return "just now"
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric" })
}

async function fetchLogs() {
  loading.value = true
  error.value = ""
  try {
    logs.value = (await api.get("/activity-logs")).data
  } catch (e: any) {
    error.value = e?.response?.data?.detail || "Failed to load activity logs"
  } finally {
    loading.value = false
  }
}

onMounted(fetchLogs)
</script>
