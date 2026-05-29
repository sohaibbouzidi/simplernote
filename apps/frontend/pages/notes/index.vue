<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-white">Notes</h1>
        <p class="text-sm text-slate-400">Search, filter, and edit your structured notes.</p>
      </div>
      <button @click="openCreate" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">New note</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-400">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading notes...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-red-500/50 bg-red-500/10 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchNotes" class="mt-3 rounded-md bg-slate-800 px-4 py-2 text-sm hover:bg-slate-700">Retry</button>
    </div>

    <div v-else-if="notes.length === 0" class="rounded-lg border border-dashed border-slate-800 p-12 text-center">
      <svg class="mx-auto h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
      <h3 class="mt-3 font-semibold text-white">No notes yet</h3>
      <p class="mt-1 text-sm text-slate-400">Create your first note to get started.</p>
      <button @click="openCreate" class="mt-4 rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">Create note</button>
    </div>

    <div v-else class="rounded-lg border border-slate-800 divide-y divide-slate-800">
      <div v-for="note in notes" :key="note.id" class="px-5 py-4 hover:bg-surface-50">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0 flex-1">
            <p class="font-medium text-white truncate">{{ note.title }}</p>
            <p class="text-sm text-slate-400 line-clamp-2 mt-0.5">{{ note.summary || note.content || 'No content' }}</p>
            <div class="mt-2 flex items-center gap-2 text-xs text-slate-400">
              <span v-if="note.note_type" class="rounded-full border border-slate-700 px-2 py-0.5">{{ note.note_type }}</span>
              <NuxtLink v-if="note.project_id && note.project_name" :to="`/projects/${note.project_id}`" class="text-brand-400 hover:underline">{{ note.project_name }}</NuxtLink>
            </div>
          </div>
          <button @click="openEdit(note)" class="shrink-0 rounded-md border border-slate-800 px-2.5 py-1 text-xs text-slate-400 hover:bg-slate-800">Edit</button>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="editing ? 'Edit note' : 'New note'">
      <form @submit.prevent="saveNote" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-white mb-1">Title</label>
          <input v-model="form.title" required class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm font-medium text-white mb-1">Content</label>
          <textarea v-model="form.content" rows="5" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm font-medium text-white mb-1">Type</label>
          <input v-model="form.note_type" placeholder="e.g. meeting, spec, idea" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white placeholder-slate-400 focus:border-brand-500 focus:outline-none" />
        </div>
        <div v-if="!editing">
          <label class="block text-sm font-medium text-white mb-1">Project (optional)</label>
          <select v-model="form.project_id" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none">
            <option value="">No project</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">{{ editing ? 'Save' : 'Create' }}</button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const notes = ref<any[]>([])
const projects = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showModal = ref(false)
const editing = ref<any | null>(null)
const form = ref({ title: "", content: "", note_type: "", project_id: "" })

async function fetchNotes() {
  loading.value = true; error.value = ""
  try { notes.value = (await api.get("/notes")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load notes"; notes.value = [] }
  finally { loading.value = false }
}

async function fetchProjects() {
  try { projects.value = (await api.get("/projects")).data } catch { projects.value = [] }
}

function openCreate() {
  editing.value = null
  form.value = { title: "", content: "", note_type: "", project_id: "" }
  showModal.value = true
}

function openEdit(note: any) {
  editing.value = note
  form.value = { title: note.title, content: note.content || "", note_type: note.note_type || "", project_id: note.project_id || "" }
  showModal.value = true
}

async function saveNote() {
  try {
    const payload: any = { title: form.value.title, content: form.value.content, note_type: form.value.note_type }
    if (form.value.project_id) payload.project_id = form.value.project_id
    if (editing.value) await api.patch(`/notes/${editing.value.id}`, payload)
    else await api.post("/notes", payload)
    showModal.value = false; await fetchNotes()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error saving note") }
}

onMounted(() => { fetchNotes(); fetchProjects() })
</script>
