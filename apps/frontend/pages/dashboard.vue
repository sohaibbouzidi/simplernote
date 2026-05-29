<template>
  <div class="space-y-8">
    <div v-if="loading" class="flex items-center justify-center py-20 text-[#8b949e]">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading dashboard...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-[#f85149]/50 bg-[#f85149]/10 p-6 text-center text-[#f85149]">
      <p>{{ error }}</p>
      <button @click="loadDashboard" class="mt-3 rounded-md bg-[#21262d] px-4 py-2 text-sm hover:bg-[#30363d]">Retry</button>
    </div>

    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-semibold text-[#e6edf3]">Welcome{{ auth.user?.email ? ', ' + auth.user.email.split('@')[0] : '' }}</h1>
          <p class="mt-1 text-sm text-[#8b949e]">Manage your AI agent workspaces.</p>
        </div>
        <NuxtLink to="/projects" class="rounded-md border border-[#21262d] bg-[#2ea043] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">New project</NuxtLink>
      </div>

      <div class="grid gap-4 sm:grid-cols-3">
        <div class="rounded-lg border border-[#21262d] bg-[#161b22] p-5">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-md bg-[#1f6feb]/20">
              <svg class="h-5 w-5 text-[#58a6ff]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
            </div>
            <div>
              <p class="text-2xl font-semibold text-[#e6edf3]">{{ stats.projects }}</p>
              <p class="text-sm text-[#8b949e]">Projects</p>
            </div>
          </div>
        </div>
        <div class="rounded-lg border border-[#21262d] bg-[#161b22] p-5">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-md bg-[#d29922]/20">
              <svg class="h-5 w-5 text-[#d29922]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            </div>
            <div>
              <p class="text-2xl font-semibold text-[#e6edf3]">{{ stats.notes }}</p>
              <p class="text-sm text-[#8b949e]">Notes</p>
            </div>
          </div>
        </div>
        <div class="rounded-lg border border-[#21262d] bg-[#161b22] p-5">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-md bg-[#2ea043]/20">
              <svg class="h-5 w-5 text-[#56d364]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
            </div>
            <div>
              <p class="text-2xl font-semibold text-[#e6edf3]">{{ stats.tasks }}</p>
              <p class="text-sm text-[#8b949e]">Tasks</p>
            </div>
          </div>
        </div>
      </div>

      <section class="rounded-lg border border-[#21262d]">
        <div class="border-b border-[#21262d] px-5 py-3">
          <h2 class="text-base font-semibold text-[#e6edf3]">Recent projects</h2>
        </div>
        <div v-if="recentProjects.length === 0" class="px-5 py-12 text-center text-sm text-[#8b949e]">
          <p class="mb-3">No projects yet</p>
          <NuxtLink to="/projects/new" class="text-[#58a6ff] hover:underline">Create your first project</NuxtLink>
        </div>
        <div v-else class="divide-y divide-[#21262d]">
          <NuxtLink v-for="p in recentProjects" :key="p.id" :to="`/projects/${p.id}`" class="flex items-center gap-4 px-5 py-4 hover:bg-[#161b22]">
            <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-[#30363d] bg-[#21262d]">
              <svg class="h-4 w-4 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
            </div>
            <div class="min-w-0 flex-1">
              <p class="truncate font-semibold text-[#e6edf3]">{{ p.name }}</p>
              <p v-if="p.description" class="truncate text-sm text-[#8b949e]">{{ p.description }}</p>
            </div>
            <span class="shrink-0 text-xs text-[#8b949e]">{{ formatDate(p.created_at) }}</span>
          </NuxtLink>
        </div>
      </section>

      <section class="rounded-lg border border-[#21262d]">
        <div class="border-b border-[#21262d] px-5 py-3">
          <h2 class="text-base font-semibold text-[#e6edf3]">Recent activity</h2>
        </div>
        <div v-if="recentLogs.length === 0" class="px-5 py-12 text-center text-sm text-[#8b949e]">
          No activity yet
        </div>
        <div v-else class="divide-y divide-[#21262d]">
          <div v-for="log in recentLogs" :key="log.id" class="flex items-center gap-3 px-5 py-3 text-sm">
            <div class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#21262d]">
              <svg class="h-3 w-3 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <span class="text-[#e6edf3]"><strong>{{ log.action }}</strong> on {{ log.entity_type }}</span>
            <span class="ml-auto text-[#8b949e]">{{ formatDate(log.created_at) }}</span>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"
import { getApiInstance } from "@/services/api"

const auth = useAuthStore()
const api = getApiInstance()
const stats = ref({ notes: 0, tasks: 0, projects: 0 })
const recentProjects = ref<any[]>([])
const recentLogs = ref<any[]>([])
const loading = ref(true)
const error = ref("")

function formatDate(d: string) {
  return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric" })
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
    recentProjects.value = projectsRes.data.slice(0, 5)
    recentLogs.value = logsRes.data.slice(0, 5)
  } catch (e: any) {
    error.value = e?.response?.data?.detail || "Failed to load dashboard"
  } finally { loading.value = false }
}

onMounted(loadDashboard)
</script>
