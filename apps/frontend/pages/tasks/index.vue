<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">Tasks</h1>
        <p class="text-slate-400">Organize work with status lanes and subtasks.</p>
      </div>
      <button @click="openCreate" class="rounded-2xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">Add task</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading tasks...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchTasks" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <div v-else-if="tasks.length === 0" class="rounded-2xl border border-slate-800/50 bg-surface-50/50 p-12 text-center">
      <p class="text-3xl mb-4">📋</p>
      <h3 class="font-display text-xl font-semibold text-white">No tasks yet</h3>
      <p class="mt-2 text-sm text-slate-400">Create your first task to get started.</p>
      <button @click="openCreate" class="mt-6 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">Create task</button>
    </div>

    <div v-else class="grid gap-4 lg:grid-cols-4">
      <div v-for="lane in lanes" :key="lane.name" class="rounded-3xl border border-slate-800 bg-slate-950 p-5">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-white">{{ lane.label }}</h2>
          <span class="rounded-full bg-slate-800 px-2.5 py-0.5 text-xs text-slate-400">{{ lane.tasks.length }}</span>
        </div>
        <div class="space-y-4 min-h-[120px]">
          <div v-for="task in lane.tasks" :key="task.id" class="rounded-2xl border border-slate-800 bg-slate-900 p-4 text-slate-200">
            <div class="flex items-start justify-between gap-2">
              <p class="font-semibold">{{ task.title }}</p>
              <span :class="priorityClass(task.priority)" class="shrink-0 rounded-full px-2 py-0.5 text-xs">{{ task.priority }}</span>
            </div>
            <p class="mt-2 text-sm text-slate-400 line-clamp-2">{{ task.description }}</p>
            <div class="mt-3 flex items-center gap-2">
              <button @click="openEdit(task)" class="rounded-lg bg-slate-800 px-2.5 py-1 text-xs text-slate-300 hover:bg-slate-700">Edit</button>
              <button @click="quickMove(task)" class="rounded-lg bg-slate-800 px-2.5 py-1 text-xs text-slate-300 hover:bg-slate-700">Move</button>
              <button @click="confirmDelete(task)" class="rounded-lg bg-red-900/50 px-2.5 py-1 text-xs text-red-300 hover:bg-red-800/50">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit Task' : 'New Task'">
      <form @submit.prevent="saveTask" class="space-y-4">
        <div>
          <label class="block text-sm text-slate-400 mb-1">Project</label>
          <select v-model="form.project_id" required class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none">
            <option value="" disabled>Select a project</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">Title</label>
          <input v-model="form.title" required class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">Description</label>
          <textarea v-model="form.description" rows="3" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div class="flex gap-4">
          <div class="flex-1">
            <label class="block text-sm text-slate-400 mb-1">Status</label>
            <select v-model="form.status" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none">
              <option v-for="l in lanes" :key="l.name" :value="l.name">{{ l.label }}</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="block text-sm text-slate-400 mb-1">Priority</label>
            <select v-model="form.priority" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none">
              <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">Assigned Agent</label>
          <input v-model="form.assigned_agent" placeholder="agent-name (optional)" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">{{ editing ? 'Save' : 'Create' }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="showMove" title="Move Task">
      <div class="space-y-3">
        <p class="text-slate-400">Move <strong class="text-white">{{ moving?.title }}</strong> to:</p>
        <div class="flex flex-wrap gap-2">
          <button v-for="l in lanes" :key="l.name" @click="moveTask(l.name)" :class="moving?.status === l.name ? 'border-brand-500 bg-brand-500/20' : 'border-slate-700 hover:border-slate-600'" class="rounded-xl border px-4 py-2 text-sm text-white">
            {{ l.label }}
          </button>
        </div>
      </div>
    </Modal>

    <Modal v-model="showDelete" title="Delete Task?">
      <p class="text-slate-400 mb-6">Delete <strong class="text-white">{{ deleting?.title }}</strong>?</p>
      <div class="flex justify-end gap-3">
        <button @click="showDelete = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
        <button @click="deleteTask" class="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-500">Delete</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const tasks = ref<any[]>([])
const projects = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showModal = ref(false)
const showMove = ref(false)
const showDelete = ref(false)
const editing = ref<any | null>(null)
const moving = ref<any | null>(null)
const deleting = ref<any | null>(null)

const laneDefs = [
  { name: "todo", label: "Todo" },
  { name: "planning", label: "Planning" },
  { name: "research", label: "Research" },
  { name: "coding", label: "Coding" },
  { name: "review", label: "Review" },
  { name: "testing", label: "Testing" },
  { name: "done", label: "Done" },
  { name: "blocked", label: "Blocked" },
]

const lanes = computed(() =>
  laneDefs.map((l) => ({ ...l, tasks: tasks.value.filter((t: any) => t.status === l.name) }))
)

const form = ref({ project_id: "", title: "", description: "", status: "todo", priority: "medium", assigned_agent: "" })

watch(showModal, (v) => { if (!v) { editing.value = null; resetForm() } })

function resetForm() {
  form.value = { project_id: "", title: "", description: "", status: "todo", priority: "medium", assigned_agent: "" }
}

function openCreate() { editing.value = null; resetForm(); showModal.value = true }

function openEdit(task: any) {
  editing.value = task
  form.value = { project_id: task.project_id, title: task.title, description: task.description || "", status: task.status, priority: task.priority, assigned_agent: task.assigned_agent || "" }
  showModal.value = true
}

function quickMove(task: any) { moving.value = task; showMove.value = true }

async function moveTask(status: string) {
  if (!moving.value) return
  try {
    await api.patch(`/tasks/${moving.value.id}`, { status })
    showMove.value = false; await fetchTasks()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error moving task") }
}

function confirmDelete(task: any) { deleting.value = task; showDelete.value = true }

function priorityClass(p: string) {
  if (p === "critical") return "bg-red-900/50 text-red-300"
  if (p === "high") return "bg-orange-900/50 text-orange-300"
  if (p === "medium") return "bg-blue-900/50 text-blue-300"
  return "bg-slate-800 text-slate-400"
}

async function fetchTasks() {
  loading.value = true; error.value = ""
  try { tasks.value = (await api.get("/tasks")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load tasks"; tasks.value = [] }
  finally { loading.value = false }
}
async function fetchProjects() {
  try { projects.value = (await api.get("/projects")).data } catch (e) { console.error(e) }
}

async function saveTask() {
  try {
    if (editing.value) await api.patch(`/tasks/${editing.value.id}`, form.value)
    else await api.post("/tasks", form.value)
    showModal.value = false; await fetchTasks()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving task") }
}

async function deleteTask() {
  if (!deleting.value) return
  try {
    await api.delete(`/tasks/${deleting.value.id}`)
    showDelete.value = false; deleting.value = null; await fetchTasks()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error deleting task") }
}

onMounted(async () => { await Promise.all([fetchTasks(), fetchProjects()]) })
</script>
