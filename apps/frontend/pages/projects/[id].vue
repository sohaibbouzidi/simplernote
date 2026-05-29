<template>
  <div v-if="loading" class="flex items-center justify-center py-20 text-[#8b949e]">
    <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
    <span class="ml-3">Loading project...</span>
  </div>

  <div v-else-if="error" class="rounded-lg border border-[#f85149]/50 bg-[#f85149]/10 p-6 text-center text-[#f85149]">
    <p>{{ error }}</p>
  </div>

  <template v-else>
    <div class="mb-6">
      <NuxtLink to="/projects" class="text-sm text-[#8b949e] hover:text-[#58a6ff]">
        <svg class="mr-1 inline h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        Projects
      </NuxtLink>
      <div class="mt-2 flex items-start justify-between gap-4">
        <div class="min-w-0 flex-1">
          <h1 class="text-2xl font-semibold text-[#e6edf3]">
            <span class="mr-2 inline-flex items-center justify-center rounded-md border border-[#30363d] bg-[#21262d] px-1.5 py-0.5 text-xs font-medium text-[#8b949e]">project</span>
            {{ project?.name }}
          </h1>
          <p class="mt-1 text-sm text-[#8b949e]">{{ project?.description || "No description" }}</p>
        </div>
      </div>
    </div>

    <div class="mb-6 border-b border-[#21262d]">
      <nav class="-mb-px flex gap-1">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
          'relative inline-flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors',
          activeTab === tab.key
            ? 'text-[#e6edf3] after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[#f78166]'
            : 'text-[#8b949e] hover:text-[#e6edf3] hover:bg-[#161b22]'
        ]">
          <span v-html="tab.icon" class="h-4 w-4 inline-flex items-center justify-center" />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <div v-if="activeTab === 'notes'" class="space-y-4">
      <div class="flex items-center justify-between">
        <p class="text-sm text-[#8b949e]">{{ notes.length }} note{{ notes.length !== 1 ? 's' : '' }}</p>
        <button @click="openCreateNote" class="rounded-md border border-[#21262d] bg-[#238636] px-3 py-1.5 text-sm font-semibold text-white hover:bg-[#2c974b]">New note</button>
      </div>

      <div v-if="notesLoading" class="flex items-center justify-center py-12 text-[#8b949e] text-sm">
        <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
        Loading notes...
      </div>

      <div v-else-if="notes.length === 0" class="rounded-lg border border-dashed border-[#21262d] p-12 text-center">
        <svg class="mx-auto h-8 w-8 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        <p class="mt-3 text-sm font-medium text-[#e6edf3]">No notes yet</p>
        <p class="text-xs text-[#8b949e] mt-1">Create a note for this project.</p>
      </div>

      <div v-else class="rounded-lg border border-[#21262d] divide-y divide-[#21262d]">
        <div v-for="note in notes" :key="note.id" class="px-4 py-3 hover:bg-[#161b22] cursor-pointer" @click="openEditNote(note)">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0 flex-1">
              <p class="font-medium text-[#e6edf3] truncate">{{ note.title }}</p>
              <p class="text-sm text-[#8b949e] line-clamp-2 mt-0.5">{{ note.summary || note.content || 'No content' }}</p>
            </div>
            <div class="flex shrink-0 items-center gap-2 text-xs text-[#8b949e]">
              <span v-if="note.note_type" class="rounded-full border border-[#30363d] px-2 py-0.5 text-xs">{{ note.note_type }}</span>
              <span>{{ formatDate(note.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <Modal v-model="showNoteModal" :title="editingNote ? 'Edit note' : 'New note'">
        <form @submit.prevent="saveNote" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Title</label>
            <input v-model="noteForm.title" required class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Content</label>
            <textarea v-model="noteForm.content" rows="5" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Type</label>
            <input v-model="noteForm.note_type" placeholder="e.g. meeting, spec, idea" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] placeholder-[#8b949e] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showNoteModal = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Cancel</button>
            <button type="submit" class="rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">{{ editingNote ? 'Save' : 'Create' }}</button>
          </div>
        </form>
      </Modal>
    </div>

    <div v-if="activeTab === 'tasks'" class="space-y-4">
      <div class="flex items-center justify-between">
        <p class="text-sm text-[#8b949e]">{{ tasks.length }} task{{ tasks.length !== 1 ? 's' : '' }}</p>
        <button @click="openCreateTask" class="rounded-md border border-[#21262d] bg-[#238636] px-3 py-1.5 text-sm font-semibold text-white hover:bg-[#2c974b]">New task</button>
      </div>

      <div v-if="tasksLoading" class="flex items-center justify-center py-12 text-[#8b949e] text-sm">
        <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
        Loading tasks...
      </div>

      <div v-else-if="tasks.length === 0" class="rounded-lg border border-dashed border-[#21262d] p-12 text-center">
        <svg class="mx-auto h-8 w-8 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
        <p class="mt-3 text-sm font-medium text-[#e6edf3]">No tasks yet</p>
        <p class="text-xs text-[#8b949e] mt-1">Create a task for this project.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <div class="flex gap-4 min-w-max pb-2">
          <div v-for="lane in lanes" :key="lane.key" class="w-72 shrink-0">
            <div class="mb-2 flex items-center gap-2 px-1">
              <span :class="lane.dotClass" class="h-2.5 w-2.5 rounded-full inline-block" />
              <span class="text-xs font-semibold text-[#8b949e] uppercase tracking-wider">{{ lane.label }}</span>
              <span class="text-xs text-[#8b949e]">{{ groupedTasks[lane.key]?.length || 0 }}</span>
            </div>
            <div class="space-y-2">
              <div v-for="task in (groupedTasks[lane.key] || [])" :key="task.id" :class="['rounded-lg border p-3 cursor-pointer transition-colors', task.status === 'done' ? 'border-[#21262d] bg-[#161b22] opacity-60 hover:opacity-100' : task.status === 'in-progress' ? 'border-[#1f6feb]/40 bg-[#161b22] hover:bg-[#1c2333]' : task.status === 'blocked' ? 'border-[#f85149]/40 bg-[#161b22] hover:bg-[#2d1c1c]' : 'border-[#21262d] bg-[#161b22] hover:bg-[#1c2128]']" @click="openEditTask(task)">
                <p class="text-sm font-medium text-[#e6edf3]">{{ task.title }}</p>
                <p v-if="task.description" class="mt-1 text-xs text-[#8b949e] line-clamp-2">{{ task.description }}</p>
                <div class="mt-2 flex items-center gap-2 text-xs text-[#8b949e]">
                  <span v-if="task.priority" :class="task.priority === 'high' ? 'text-[#f85149]' : task.priority === 'medium' ? 'text-[#d29922]' : 'text-[#8b949e]'">{{ task.priority }}</span>
                  <span v-if="task.assigned_agent" class="truncate">@{{ task.assigned_agent }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Modal v-model="showTaskModal" :title="editingTask ? 'Edit task' : 'New task'">
        <form @submit.prevent="saveTask" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Title</label>
            <input v-model="taskForm.title" required class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Description</label>
            <textarea v-model="taskForm.description" rows="3" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-[#e6edf3] mb-1">Status</label>
              <select v-model="taskForm.status" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none">
                <option value="todo">Todo</option>
                <option value="in-progress">In Progress</option>
                <option value="review">Review</option>
                <option value="blocked">Blocked</option>
                <option value="done">Done</option>
                <option value="cancelled">Cancelled</option>
                <option value="backlog">Backlog</option>
                <option value="deferred">Deferred</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-[#e6edf3] mb-1">Priority</label>
              <select v-model="taskForm.priority" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showTaskModal = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Cancel</button>
            <button type="submit" class="rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">{{ editingTask ? 'Save' : 'Create' }}</button>
          </div>
        </form>
      </Modal>
    </div>

    <div v-if="activeTab === 'settings'" class="max-w-2xl space-y-8">
      <section class="rounded-lg border border-[#21262d]">
        <div class="border-b border-[#21262d] px-5 py-3">
          <h2 class="text-base font-semibold text-[#e6edf3]">Project info</h2>
        </div>
        <div class="px-5 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Name</label>
            <input v-model="settingsForm.name" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Description</label>
            <textarea v-model="settingsForm.description" rows="3" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div class="flex gap-3">
            <button @click="saveSettings" class="rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">Save</button>
            <button @click="confirmDeleteProject" class="rounded-md border border-[#21262d] bg-transparent px-4 py-2 text-sm text-[#f85149] hover:bg-[#f85149]/10">Delete project</button>
          </div>
        </div>
      </section>

      <section class="rounded-lg border border-[#21262d]">
        <div class="border-b border-[#21262d] px-5 py-3 flex items-center justify-between">
          <h2 class="text-base font-semibold text-[#e6edf3]">API Keys</h2>
          <button @click="openCreateKey" class="rounded-md border border-[#21262d] bg-[#238636] px-3 py-1.5 text-sm font-semibold text-white hover:bg-[#2c974b]">Create key</button>
        </div>
        <div v-if="keysLoading" class="px-5 py-8 text-center text-sm text-[#8b949e]">
          <svg class="mx-auto h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
          <span class="ml-2">Loading keys...</span>
        </div>
        <div v-else-if="keys.length === 0" class="px-5 py-8 text-center text-sm text-[#8b949e]">
          No API keys for this project.
        </div>
        <div v-else class="divide-y divide-[#21262d]">
          <div v-for="key in keys" :key="key.id" class="flex items-center justify-between px-5 py-3">
            <div class="min-w-0">
              <p class="font-medium text-[#e6edf3] text-sm">{{ key.name }}</p>
              <p class="text-xs text-[#8b949e] mt-0.5">Permissions: {{ Object.keys(key.permissions).join(", ") || "none" }}</p>
            </div>
            <button @click="confirmDeleteKey(key)" class="shrink-0 rounded-md border border-[#21262d] px-2.5 py-1 text-xs text-[#f85149] hover:bg-[#f85149]/10">Revoke</button>
          </div>
        </div>
      </section>

      <Modal v-model="showCreateKey" title="Create API Key">
        <form @submit.prevent="createKey" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-1">Name</label>
            <input v-model="keyForm.name" required placeholder="e.g. my-coding-agent" class="w-full rounded-md border border-[#30363d] bg-[#0d1117] px-3 py-2 text-sm text-[#e6edf3] placeholder-[#8b949e] focus:border-[#2ea043] focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#e6edf3] mb-2">Permissions</label>
            <div class="space-y-2">
              <label v-for="perm in permissionOptions" :key="perm.key" class="flex items-center gap-3 rounded-md border border-[#21262d] bg-[#161b22] px-3 py-2">
                <input type="checkbox" v-model="keyForm.permissions[perm.key]" class="rounded border-[#30363d] bg-[#0d1117] text-[#2ea043] focus:ring-[#2ea043]" />
                <span class="text-sm text-[#e6edf3]">{{ perm.label }}</span>
              </label>
            </div>
          </div>
          <div v-if="newKeyValue" class="rounded-md border border-[#2ea043]/30 bg-[#2ea043]/10 p-3">
            <p class="text-sm font-semibold text-[#56d364]">Key created! Copy it now — it won't be shown again.</p>
            <div class="mt-2">
              <CodeBlock :code="newKeyValue" lang="plain" />
            </div>
          </div>
          <div v-if="!newKeyValue" class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showCreateKey = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Cancel</button>
            <button type="submit" class="rounded-md border border-[#21262d] bg-[#238636] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2c974b]">Create</button>
          </div>
          <div v-else class="flex justify-end pt-2">
            <button type="button" @click="showCreateKey = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Done</button>
          </div>
        </form>
      </Modal>

      <Modal v-model="showRevokeKey" title="Revoke API Key?">
        <p class="text-sm text-[#8b949e] mb-6">Revoke <strong class="text-[#e6edf3]">{{ deletingKey?.name }}</strong>? Any agent using this key will immediately lose access.</p>
        <div class="flex justify-end gap-3">
          <button @click="showRevokeKey = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Cancel</button>
          <button @click="deleteKey" class="rounded-md border border-[#21262d] bg-[#f85149] px-4 py-2 text-sm font-semibold text-white hover:bg-[#da3633]">Revoke</button>
        </div>
      </Modal>

      <Modal v-model="showDeleteProject" title="Delete Project?">
        <p class="text-sm text-[#8b949e] mb-6">Delete <strong class="text-[#e6edf3]">{{ project?.name }}</strong>? This will also delete all notes, tasks, and API keys in this project.</p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteProject = false" class="rounded-md border border-[#21262d] bg-[#21262d] px-4 py-2 text-sm text-[#e6edf3] hover:bg-[#30363d]">Cancel</button>
          <button @click="deleteProject" class="rounded-md border border-[#21262d] bg-[#f85149] px-4 py-2 text-sm font-semibold text-white hover:bg-[#da3633]">Delete</button>
        </div>
      </Modal>
    </div>
  </template>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "#app"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const route = useRoute()
const router = useRouter()
const projectId = route.params.id as string

const project = ref<any | null>(null)
const loading = ref(true)
const error = ref("")
const activeTab = ref("notes")

const tabs = [
  { key: "notes", label: "Notes", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>' },
  { key: "tasks", label: "Tasks", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>' },
  { key: "settings", label: "Settings", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>' },
]

const settingsForm = ref({ name: "", description: "" })

async function fetchProject() {
  try {
    const res = (await api.get(`/projects/${projectId}`)).data
    project.value = res
    settingsForm.value = { name: res.name, description: res.description || "" }
  } catch (e: any) {
    error.value = e?.response?.data?.detail || "Failed to load project"
  } finally {
    loading.value = false
  }
}

async function saveSettings() {
  try {
    const res = (await api.patch(`/projects/${projectId}`, settingsForm.value)).data
    project.value = res
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving project") }
}

function confirmDeleteProject() { showDeleteProject.value = true }

async function deleteProject() {
  try {
    await api.delete(`/projects/${projectId}`)
    showDeleteProject.value = false
    router.push("/projects")
  } catch (e: any) { alert(e?.response?.data?.detail || "Error deleting project") }
}

const notes = ref<any[]>([])
const notesLoading = ref(false)
const showNoteModal = ref(false)
const editingNote = ref<any | null>(null)
const noteForm = ref({ title: "", content: "", note_type: "" })

async function fetchNotes() {
  notesLoading.value = true
  try {
    notes.value = (await api.get(`/notes?project_id=${projectId}`)).data
  } catch { notes.value = [] }
  finally { notesLoading.value = false }
}

function openCreateNote() {
  editingNote.value = null
  noteForm.value = { title: "", content: "", note_type: "" }
  showNoteModal.value = true
}

function openEditNote(note: any) {
  editingNote.value = note
  noteForm.value = { title: note.title, content: note.content || "", note_type: note.note_type || "" }
  showNoteModal.value = true
}

async function saveNote() {
  try {
    if (editingNote.value) {
      await api.patch(`/notes/${editingNote.value.id}`, noteForm.value)
    } else {
      await api.post("/notes", { ...noteForm.value, project_id: projectId })
    }
    showNoteModal.value = false
    await fetchNotes()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving note") }
}

const tasks = ref<any[]>([])
const tasksLoading = ref(false)
const showTaskModal = ref(false)
const editingTask = ref<any | null>(null)
const taskForm = ref({ title: "", description: "", status: "todo", priority: "medium" })

const lanes = [
  { key: "backlog", label: "Backlog", dotClass: "bg-[#8b949e]" },
  { key: "todo", label: "Todo", dotClass: "bg-[#8b949e]" },
  { key: "in-progress", label: "In Progress", dotClass: "bg-[#58a6ff]" },
  { key: "review", label: "Review", dotClass: "bg-[#d29922]" },
  { key: "blocked", label: "Blocked", dotClass: "bg-[#f85149]" },
  { key: "done", label: "Done", dotClass: "bg-[#56d364]" },
  { key: "cancelled", label: "Cancelled", dotClass: "bg-[#8b949e]" },
  { key: "deferred", label: "Deferred", dotClass: "bg-[#8b949e]" },
]

const groupedTasks = computed(() => {
  const groups: Record<string, any[]> = {}
  for (const lane of lanes) groups[lane.key] = []
  for (const task of tasks.value) {
    if (groups[task.status]) groups[task.status].push(task)
    else groups["backlog"].push(task)
  }
  return groups
})

async function fetchTasks() {
  tasksLoading.value = true
  try {
    tasks.value = (await api.get(`/tasks?project_id=${projectId}`)).data
  } catch { tasks.value = [] }
  finally { tasksLoading.value = false }
}

function openCreateTask() {
  editingTask.value = null
  taskForm.value = { title: "", description: "", status: "todo", priority: "medium" }
  showTaskModal.value = true
}

function openEditTask(task: any) {
  editingTask.value = task
  taskForm.value = { title: task.title, description: task.description || "", status: task.status, priority: task.priority || "medium" }
  showTaskModal.value = true
}

async function saveTask() {
  try {
    if (editingTask.value) {
      await api.patch(`/tasks/${editingTask.value.id}`, taskForm.value)
    } else {
      await api.post("/tasks", { ...taskForm.value, project_id: projectId })
    }
    showTaskModal.value = false
    await fetchTasks()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving task") }
}

const keys = ref<any[]>([])
const keysLoading = ref(false)
const showCreateKey = ref(false)
const showRevokeKey = ref(false)
const showDeleteProject = ref(false)
const deletingKey = ref<any | null>(null)
const newKeyValue = ref<string | null>(null)
const keyForm = ref({ name: "", permissions: { read_notes: false, write_notes: false } })

const permissionOptions = [
  { key: "read_notes", label: "Read notes & tasks" },
  { key: "write_notes", label: "Create & edit notes & tasks" },
]

async function fetchKeys() {
  keysLoading.value = true
  try { keys.value = (await api.get(`/api-keys/project/${projectId}`)).data } catch { keys.value = [] }
  finally { keysLoading.value = false }
}

function openCreateKey() {
  keyForm.value = { name: "", permissions: { read_notes: false, write_notes: false } }
  newKeyValue.value = null
  showCreateKey.value = true
}

function confirmDeleteKey(key: any) { deletingKey.value = key; showRevokeKey.value = true }

async function deleteKey() {
  if (!deletingKey.value) return
  try {
    await api.delete(`/api-keys/${deletingKey.value.id}`)
    showRevokeKey.value = false; deletingKey.value = null; await fetchKeys()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error revoking key") }
}

async function createKey() {
  try {
    const res = await api.post("/api-keys", { ...keyForm.value, project_id: projectId })
    newKeyValue.value = res.data.plain_text_key
    await fetchKeys()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error creating key") }
}

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

onMounted(() => {
  fetchProject()
  fetchNotes()
  fetchTasks()
  fetchKeys()
})
</script>
