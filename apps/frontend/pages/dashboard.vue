<template>
  <div class="space-y-8">
    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-400">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading dashboard...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-red-500/50 bg-red-500/10 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="loadDashboard" class="mt-3 rounded-md bg-slate-800 px-4 py-2 text-sm hover:bg-slate-700">Retry</button>
    </div>

    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-semibold text-white">Welcome{{ auth.user?.last_name ? ', ' + auth.user.last_name : '' }}</h1>
          <p class="mt-1 text-sm text-slate-400">Manage your AI agent workspaces.</p>
        </div>
        <NuxtLink to="/projects" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">New project</NuxtLink>
      </div>

      <div class="grid gap-4 sm:grid-cols-1">
        <div class="rounded-lg border border-slate-800 bg-surface-50 p-5">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-md bg-brand-500/20">
              <svg class="h-5 w-5 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
            </div>
            <div>
              <p class="text-2xl font-semibold text-white">{{ stats.projects }}</p>
              <p class="text-sm text-slate-400">Projects</p>
            </div>
          </div>
        </div>
      </div>

      <section class="rounded-lg border border-slate-800">
        <div class="border-b border-slate-800 px-5 py-3">
          <h2 class="text-base font-semibold text-white">Recent projects</h2>
        </div>
        <div v-if="recentProjects.length === 0" class="px-5 py-12 text-center text-sm text-slate-400">
          <p class="mb-3">No projects yet</p>
          <NuxtLink to="/projects" class="text-brand-400 hover:underline">Create your first project</NuxtLink>
        </div>
        <div v-else class="divide-y divide-slate-800">
          <NuxtLink v-for="p in recentProjects" :key="p.id" :to="`/projects/${p.id}`" class="flex items-center gap-4 px-5 py-4 hover:bg-surface-50">
            <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-slate-700 bg-slate-800">
              <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
            </div>
            <div class="min-w-0 flex-1">
              <p class="truncate font-semibold text-white">{{ p.name }}</p>
              <p v-if="p.description" class="truncate text-sm text-slate-400">{{ p.description }}</p>
            </div>
            <span class="shrink-0 text-xs text-slate-400">{{ formatDate(p.created_at) }}</span>
          </NuxtLink>
        </div>
      </section>

      <section class="rounded-lg border border-slate-800">
        <div class="border-b border-slate-800 px-5 py-3">
          <h2 class="text-base font-semibold text-white">Recent activity</h2>
        </div>
        <div v-if="recentLogs.length === 0" class="px-5 py-12 text-center text-sm text-slate-400">
          No activity yet
        </div>
        <div v-else class="divide-y divide-slate-800">
          <div v-for="log in recentLogs" :key="log.id" class="flex items-center gap-3 px-5 py-3 text-sm">
            <div class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-800">
              <svg class="h-3 w-3 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <span class="text-white"><strong>{{ log.action }}</strong> on {{ log.entity_type }}</span>
            <span class="ml-auto text-slate-400">{{ formatDate(log.created_at) }}</span>
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
const stats = ref({ projects: 0 })
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
    const [projectsRes, logsRes] = await Promise.all([
      api.get("/projects"),
      api.get("/activity-logs"),
    ])
    stats.value = { projects: projectsRes.data.length }
    recentProjects.value = projectsRes.data.slice(0, 5)
    recentLogs.value = logsRes.data.slice(0, 5)
  } catch (e: any) {
    error.value = e?.response?.data?.detail || "Failed to load dashboard"
  } finally { loading.value = false }
}

onMounted(loadDashboard)
</script>
