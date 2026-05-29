<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">Projects</h1>
        <p class="text-slate-400">Create and manage your AI memory workspaces.</p>
      </div>
      <button @click="openCreate" class="rounded-2xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">New project</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading projects...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchProjects" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <div v-else-if="projects.length === 0" class="rounded-2xl border border-slate-800/50 bg-surface-50/50 p-12 text-center">
      <p class="text-3xl mb-4">📁</p>
      <h3 class="font-display text-xl font-semibold text-white">No projects yet</h3>
      <p class="mt-2 text-sm text-slate-400">Create your first project to get started.</p>
      <button @click="openCreate" class="mt-6 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">Create project</button>
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      <div v-for="project in projects" :key="project.id" class="group rounded-2xl border border-slate-800/50 bg-surface-50/50 p-6 transition-all hover:border-violet-500/20 hover:shadow-xl hover:shadow-violet-500/5">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <h2 class="text-xl font-semibold text-white truncate">{{ project.name }}</h2>
            <p class="mt-2 text-sm text-slate-400">{{ project.description || 'No description provided.' }}</p>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-3">
          <button @click="openEdit(project)" class="rounded-lg bg-slate-800/60 px-3 py-1.5 text-xs text-slate-300 transition-all hover:bg-slate-700/80">Edit</button>
          <button @click="confirmDelete(project)" class="rounded-lg bg-red-900/30 px-3 py-1.5 text-xs text-red-300 transition-all hover:bg-red-800/50">Delete</button>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit Project' : 'New Project'">
      <form @submit.prevent="saveProject" class="space-y-4">
        <div>
          <label class="block text-sm text-slate-400 mb-1">Name</label>
          <input v-model="form.name" required class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">Description</label>
          <textarea v-model="form.description" rows="3" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">{{ editing ? 'Save' : 'Create' }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="showDelete" title="Delete Project?">
      <p class="text-slate-400 mb-6">Delete <strong class="text-white">{{ deleting?.name }}</strong>? This will also delete all notes and tasks in this project.</p>
      <div class="flex justify-end gap-3">
        <button @click="showDelete = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
        <button @click="deleteProject" class="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-500">Delete</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const projects = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showModal = ref(false)
const showDelete = ref(false)
const editing = ref<any | null>(null)
const deleting = ref<any | null>(null)

const form = ref({ name: "", description: "" })

watch(showModal, (v) => { if (!v) { editing.value = null; form.value = { name: "", description: "" } } })

function openCreate() { editing.value = null; form.value = { name: "", description: "" }; showModal.value = true }
function openEdit(project: any) { editing.value = project; form.value = { name: project.name, description: project.description || "" }; showModal.value = true }
function confirmDelete(project: any) { deleting.value = project; showDelete.value = true }

async function fetchProjects() {
  loading.value = true; error.value = ""
  try { projects.value = (await api.get("/projects")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load projects"; projects.value = [] }
  finally { loading.value = false }
}

async function saveProject() {
  try {
    if (editing.value) await api.patch(`/projects/${editing.value.id}`, form.value)
    else await api.post("/projects", form.value)
    showModal.value = false; await fetchProjects()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving project") }
}

async function deleteProject() {
  if (!deleting.value) return
  try {
    await api.delete(`/projects/${deleting.value.id}`)
    showDelete.value = false; deleting.value = null; await fetchProjects()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error deleting project") }
}

onMounted(fetchProjects)
</script>
