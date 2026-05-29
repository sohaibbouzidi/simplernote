<template>
  <div class="space-y-8">
    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading dashboard...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="loadDashboard" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <template v-else>
    <section class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-semibold text-white">Dashboard</h1>
          <p class="text-slate-400">Overview of your recent activity, notes, and task status.</p>
        </div>
      </div>
      <div class="mt-8 grid gap-6 sm:grid-cols-3">
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <p class="text-sm uppercase text-slate-500">Notes</p>
          <p class="mt-4 text-4xl font-semibold text-white">{{ stats.notes }}</p>
        </div>
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <p class="text-sm uppercase text-slate-500">Tasks</p>
          <p class="mt-4 text-4xl font-semibold text-white">{{ stats.tasks }}</p>
        </div>
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <p class="text-sm uppercase text-slate-500">Projects</p>
          <p class="mt-4 text-4xl font-semibold text-white">{{ stats.projects }}</p>
        </div>
      </div>
    </section>

    <section class="grid gap-6 xl:grid-cols-2">
      <div class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
        <h2 class="text-2xl font-semibold text-white">Recent Notes</h2>
        <p class="mt-2 text-slate-400">A quick look at the latest note updates in your projects.</p>
        <div class="mt-6 space-y-4">
          <div v-for="note in recentNotes" :key="note.id" class="rounded-3xl border border-slate-800 bg-slate-950 p-4">
            <p class="font-semibold text-white truncate">{{ note.title }}</p>
            <p class="mt-1 text-slate-400 line-clamp-2 text-sm">{{ note.summary || note.content || 'No content' }}</p>
          </div>
          <div v-if="recentNotes.length === 0" class="rounded-3xl border border-slate-800 bg-slate-950 p-4 text-center text-sm text-slate-500">No notes yet</div>
        </div>
      </div>
      <div class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
        <h2 class="text-2xl font-semibold text-white">Recent Activity</h2>
        <p class="mt-2 text-slate-400">User and AI agent lifecycle events.</p>
        <ul class="mt-6 space-y-3">
          <li v-for="log in recentLogs" :key="log.id" class="rounded-3xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-300">
            <span class="font-semibold text-white">{{ log.action }}</span> — {{ log.entity_type }}
            <span class="text-slate-500 ml-2">{{ formatDate(log.created_at) }}</span>
          </li>
          <li v-if="recentLogs.length === 0" class="rounded-3xl border border-slate-800 bg-slate-950 p-4 text-center text-sm text-slate-500">No activity yet</li>
        </ul>
      </div>
    </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const stats = ref({ notes: 0, tasks: 0, projects: 0 })
const recentNotes = ref<any[]>([])
const recentLogs = ref<any[]>([])
const loading = ref(true)
const error = ref("")

function formatDate(d: string) {
  return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })
}

async function loadDashboard() {
  loading.value = true; error.value = ""
  try {
    const [notesRes, tasksRes, projectsRes, logsRes] = await Promise.all([
      api.get("/notes"),
      api.get("/tasks"),
      api.get("/projects"),
      api.get("/activity-logs"),
    ])
    stats.value = { notes: notesRes.data.length, tasks: tasksRes.data.length, projects: projectsRes.data.length }
    recentNotes.value = notesRes.data.slice(0, 3)
    recentLogs.value = logsRes.data.slice(0, 5)
  } catch (e: any) {
    error.value = e?.response?.data?.detail || "Failed to load dashboard"
    stats.value = { notes: 0, tasks: 0, projects: 0 }
  } finally { loading.value = false }
}

onMounted(loadDashboard)
</script>
