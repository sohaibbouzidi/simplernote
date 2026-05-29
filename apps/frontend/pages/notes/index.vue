<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">Notes</h1>
        <p class="text-slate-400">Search, filter, and edit your structured notes.</p>
      </div>
      <button @click="openCreate" class="rounded-2xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">New note</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading notes...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchNotes" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <div v-else-if="notes.length === 0" class="rounded-2xl border border-slate-800/50 bg-surface-50/50 p-12 text-center">
      <p class="text-3xl mb-4">📝</p>
      <h3 class="font-display text-xl font-semibold text-white">No notes yet</h3>
      <p class="mt-2 text-sm text-slate-400">Create your first note to get started.</p>
      <button @click="openCreate" class="mt-6 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">Create note</button>
    </div>

    <div v-else class="grid gap-6 lg:grid-cols-3">
      <div v-for="note in notes" :key="note.id" class="space-y-4">
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <div class="flex items-center justify-between gap-3">
            <h2 class="text-lg font-semibold text-white truncate">{{ note.title }}</h2>
            <span class="shrink-0 rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">{{ note.note_type }}</span>
          </div>
          <p class="mt-3 text-slate-400 line-clamp-3">{{ note.summary || note.content }}</p>
          <div class="mt-4 flex items-center gap-3">
            <button @click="openEdit(note)" class="rounded-xl bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700">Edit</button>
            <button @click="confirmDelete(note)" class="rounded-xl bg-red-900/50 px-3 py-1.5 text-xs text-red-300 hover:bg-red-800/50">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit Note' : 'New Note'">
      <form @submit.prevent="saveNote" class="space-y-4">
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
          <label class="block text-sm text-slate-400 mb-1">Content</label>
          <textarea v-model="form.content" rows="4" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">Summary</label>
          <input v-model="form.summary" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div class="flex gap-4">
          <div class="flex-1">
            <label class="block text-sm text-slate-400 mb-1">Type</label>
            <select v-model="form.note_type" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none">
              <option v-for="t in noteTypes" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="block text-sm text-slate-400 mb-1">Tags (comma-separated)</label>
            <input v-model="tagsInput" placeholder="ai, architecture" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:brightness-110">{{ editing ? 'Save' : 'Create' }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="showDelete" title="Delete Note?">
      <p class="text-slate-400 mb-6">Are you sure you want to delete <strong class="text-white">{{ deleting?.title }}</strong>?</p>
      <div class="flex justify-end gap-3">
        <button @click="showDelete = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
        <button @click="deleteNote" class="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-500">Delete</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const notes = ref<any[]>([])
const projects = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showModal = ref(false)
const showDelete = ref(false)
const editing = ref<any | null>(null)
const deleting = ref<any | null>(null)
const tagsInput = ref("")

const noteTypes = ["memory", "decision", "research", "issue", "workflow", "architecture", "documentation"]

const form = ref({
  project_id: "",
  title: "",
  content: "",
  summary: "",
  note_type: "documentation",
})

watch(showModal, (v) => { if (!v) { editing.value = null; resetForm() } })

function resetForm() {
  form.value = { project_id: "", title: "", content: "", summary: "", note_type: "documentation" }
  tagsInput.value = ""
}

function openCreate() {
  editing.value = null
  resetForm()
  showModal.value = true
}

function openEdit(note: any) {
  editing.value = note
  form.value = { project_id: note.project_id, title: note.title, content: note.content || "", summary: note.summary || "", note_type: note.note_type }
  tagsInput.value = (note.tags || []).join(", ")
  showModal.value = true
}

function confirmDelete(note: any) {
  deleting.value = note
  showDelete.value = true
}

async function fetchNotes() {
  loading.value = true; error.value = ""
  try {
    const res = await api.get("/notes")
    notes.value = res.data
  } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load notes"; notes.value = [] }
  finally { loading.value = false }
}

async function fetchProjects() {
  try {
    const res = await api.get("/projects")
    projects.value = res.data
  } catch (e) { console.error(e) }
}

async function saveNote() {
  const tags = tagsInput.value ? tagsInput.value.split(",").map((t: string) => t.trim()).filter(Boolean) : []
  const payload = { ...form.value, tags }
  try {
    if (editing.value) {
      await api.patch(`/notes/${editing.value.id}`, payload)
    } else {
      await api.post("/notes", payload)
    }
    showModal.value = false
    await fetchNotes()
  } catch (e: any) {
    alert(e?.response?.data?.detail || "Error saving note")
  }
}

async function deleteNote() {
  if (!deleting.value) return
  try {
    await api.delete(`/notes/${deleting.value.id}`)
    showDelete.value = false
    deleting.value = null
    await fetchNotes()
  } catch (e: any) {
    alert(e?.response?.data?.detail || "Error deleting note")
  }
}

onMounted(async () => {
  await Promise.all([fetchNotes(), fetchProjects()])
})
</script>
