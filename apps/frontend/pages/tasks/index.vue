<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-[#e6edf3]">Tasks</h1>
        <p class="text-sm text-[#8b949e]">Organize work with status lanes across all projects.</p>
      </div>
      <button @click="openCreate" class="rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">Add task</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-[#8b949e]">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading tasks...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-[#f85149]/50 bg-[#f85149]/10 p-6 text-center text-[#f85149]">
      <p>{{ error }}</p>
      <button @click="fetchTasks" class="mt-3 rounded-md bg-[#21262d] px-4 py-2 text-sm hover:bg-[#30363d]">Retry</button>
    </div>

    <div v-else-if="tasks.length === 0" class="rounded-lg border border-dashed border-[#21262d] p-12 text-center">
      <svg class="mx-auto h-8 w-8 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
      <h3 class="mt-3 font-semibold text-[#e6edf3]">No tasks yet</h3>
      <p class="mt-1 text-sm text-[#8b949e]">Create your first task to get started.</p>
      <button @click="openCreate" class="mt-4 rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">Create task</button>
    </div>

    <div v-else class="overflow-x-auto pb-4">
      <div class="flex gap-4 min-w-max">
        <div v-for="lane in lanes" :key="lane.key" class="w-72 shrink-0">
          <div class="mb-3 flex items-center gap-2 px-1">
            <span :class="lane.dotClass" class="h-2.5 w-2.5 rounded-full inline-block" />
            <span class="text-xs font-semibold text-[#8b949e] uppercase tracking-wider">{{ lane.label }}</span>
            <span class="text-xs text-[#8b949e]">{{ lane.tasks.length }}</span>
          </div>
          <div class="space-y-2">
            <div v-for="task in lane.tasks" :key="task.id" :class="['cursor-pointer rounded-lg border p-3 transition-colors', task.status === 'done' ? 'border-[#21262d] bg-[#161b22] opacity-60 hover:opacity-100' : task.status === 'in-progress' ? 'border-[#1f6feb]/40 bg-[#161b22] hover:bg-[#1c2333]' : task.status === 'blocked' ? 'border-[#f85149]/40 bg-[#161b22] hover:bg-[#2d1c1c]' : 'border-[#21262d] bg-[#161b22] hover:bg-[#1c2128]']" @click="openEdit(task)">
              <div class="flex items-start justify-between gap-2">
                <p class="text-sm font-medium text-[#e6edf3]">{{ task.title }}</p>
                <span v-if="task.priority" :class="task.priority === 'high' ? 'text-[#f85149]' : task.priority === 'medium' ? 'text-[#d29922]' : 'text-[#8b949e]'" class="shrink-0 text-xs">{{ task.priority }}</span>
              </div>
              <p v-if="task.description" class="mt-1 text-xs text-[#8b949e] line-clamp-2">{{ task.description }}</p>
              <div class="mt-2 flex items-center gap-2 text-xs text-[#8b949e]">
                <span v-if="task.project_name" class="truncate text-[#58a6ff]">{{ task.project_name }}</span>
                <span v-if="task.assigned_agent">@{{ task.assigned_agent }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit task' : 'New task'">
      <form @submit.prevent="saveTask" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-[#e6edf3] mb-1">Title</label>
          <input v-model="form.title" required class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm font-medium text-[#e6edf3] mb-1">Description</label>
          <textarea v-model="form.description" rows="3" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Status</label>
            <select v-model="form.status" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none">
              <option v-for="l in laneOptions" :key="l.key" :value="l.key">{{ l.label }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Priority</label>
            <select v-model="form.priority" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>
        <div v-if="!editing">
          <label class="block text-sm font-medium text-[#e6edf3] mb-1">Project (optional)</label>
          <select v-model="form.project_id" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none">
            <option value="">No project</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Cancel</button>
          <button type="submit" class="rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">{{ editing ? 'Save' : 'Create' }}</button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const tasks = ref<any[]>([])
const projects = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showModal = ref(false)
const editing = ref<any | null>(null)
const form = ref({ title: "", description: "", status: "todo", priority: "medium", project_id: "" })

const laneOptions = [
  { key: "backlog", label: "Backlog", dotClass: "bg-[#8b949e]" },
  { key: "todo", label: "Todo", dotClass: "bg-[#8b949e]" },
  { key: "in-progress", label: "In Progress", dotClass: "bg-[#58a6ff]" },
  { key: "review", label: "Review", dotClass: "bg-[#d29922]" },
  { key: "blocked", label: "Blocked", dotClass: "bg-[#f85149]" },
  { key: "done", label: "Done", dotClass: "bg-[#56d364]" },
  { key: "cancelled", label: "Cancelled", dotClass: "bg-[#8b949e]" },
  { key: "deferred", label: "Deferred", dotClass: "bg-[#8b949e]" },
]

const lanes = computed(() => {
  const groups: Record<string, any[]> = {}
  for (const l of laneOptions) groups[l.key] = []
  for (const task of tasks.value) {
    if (groups[task.status]) groups[task.status].push(task)
    else groups["backlog"].push(task)
  }
  return laneOptions.map(l => ({ ...l, tasks: groups[l.key] || [] }))
})

async function fetchTasks() {
  loading.value = true; error.value = ""
  try { tasks.value = (await api.get("/tasks")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load tasks"; tasks.value = [] }
  finally { loading.value = false }
}

async function fetchProjects() {
  try { projects.value = (await api.get("/projects")).data } catch { projects.value = [] }
}

function openCreate() {
  editing.value = null
  form.value = { title: "", description: "", status: "todo", priority: "medium", project_id: "" }
  showModal.value = true
}

function openEdit(task: any) {
  editing.value = task
  form.value = { title: task.title, description: task.description || "", status: task.status, priority: task.priority || "medium", project_id: task.project_id || "" }
  showModal.value = true
}

async function saveTask() {
  try {
    const payload: any = { title: form.value.title, description: form.value.description, status: form.value.status, priority: form.value.priority }
    if (form.value.project_id) payload.project_id = form.value.project_id
    if (editing.value) await api.patch(`/tasks/${editing.value.id}`, payload)
    else await api.post("/tasks", payload)
    showModal.value = false; await fetchTasks()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving task") }
}

onMounted(() => { fetchTasks(); fetchProjects() })
</script>
