<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-white">Projects</h1>
        <p class="text-sm text-slate-400">AI agent memory workspaces.</p>
      </div>
      <button @click="openCreate" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">New project</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-400">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading projects...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-red-500/50 bg-red-500/10 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchProjects" class="mt-3 rounded-md bg-slate-800 px-4 py-2 text-sm hover:bg-slate-700">Retry</button>
    </div>

    <div v-else-if="filtered.length === 0" class="rounded-lg border border-slate-800 p-12 text-center">
      <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-slate-800">
        <svg class="h-6 w-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
      </div>
      <h3 class="font-semibold text-white">{{ searchQuery ? 'No matching projects' : 'No projects yet' }}</h3>
      <p class="mt-1 text-sm text-slate-400">{{ searchQuery ? 'Try a different search term.' : 'Create your first project to get started.' }}</p>
      <button v-if="!searchQuery" @click="openCreate" class="mt-4 rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">Create project</button>
    </div>

    <template v-else>
      <div class="flex items-center gap-3 rounded-lg border border-slate-800 bg-surface-50 px-4 py-2.5">
        <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        <input v-model="searchQuery" placeholder="Find a project..." class="flex-1 bg-transparent text-sm text-white placeholder-slate-400 focus:outline-none" />
      </div>

      <div class="rounded-lg border border-slate-800 divide-y divide-slate-800">
        <NuxtLink v-for="project in filtered" :key="project.id" :to="`/projects/${project.id}`" class="flex items-center gap-4 px-5 py-4 hover:bg-surface-50">
          <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-slate-700 bg-slate-800">
            <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
          </div>
          <div class="min-w-0 flex-1">
            <p class="truncate font-semibold text-brand-400 hover:underline">{{ project.name }}</p>
            <p v-if="project.description" class="mt-0.5 truncate text-sm text-slate-400">{{ project.description }}</p>
          </div>
          <span class="shrink-0 text-xs text-slate-400">Updated {{ formatDate(project.updated_at || project.created_at) }}</span>
        </NuxtLink>
      </div>
    </template>

    <Modal v-model="showModal" title="New project">
      <form @submit.prevent="saveProject" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-white mb-1">Project name</label>
          <input v-model="form.name" required placeholder="e.g. my-ai-workspace" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white placeholder-slate-400 focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm font-medium text-white mb-1">Description</label>
          <textarea v-model="form.description" rows="3" placeholder="Optional description" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white placeholder-slate-400 focus:border-brand-500 focus:outline-none" />
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">Create</button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useRoute } from "#app"
import { getApiInstance } from "@/services/api"
import { useToast } from "@/composables/useToast"

const api = getApiInstance()
const route = useRoute()
const toast = useToast()
const projects = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showModal = ref(false)
const searchQuery = ref((route.query.q as string) || "")
const form = ref({ name: "", description: "" })

const filtered = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return projects.value
  return projects.value.filter(p => p.name.toLowerCase().includes(q) || (p.description || "").toLowerCase().includes(q))
})

function formatDate(d: string) {
  if (!d) return ""
  const date = new Date(d)
  const now = new Date()
  const diff = (now.getTime() - date.getTime()) / 1000
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
}

function openCreate() {
  form.value = { name: "", description: "" }
  showModal.value = true
}

async function fetchProjects() {
  loading.value = true; error.value = ""
  try { projects.value = (await api.get("/projects")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load projects"; projects.value = [] }
  finally { loading.value = false }
}

async function saveProject() {
  try {
    await api.post("/projects", form.value)
    showModal.value = false; await fetchProjects()
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error saving project") }
}

onMounted(fetchProjects)
</script>
