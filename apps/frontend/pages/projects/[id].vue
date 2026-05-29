<template>
  <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
    <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
    <span class="ml-3">Loading project...</span>
  </div>

  <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
    <p>{{ error }}</p>
  </div>

  <template v-else>
    <div class="mb-8">
      <NuxtLink to="/projects" class="text-sm text-slate-400 hover:text-white">&larr; Projects</NuxtLink>
      <h1 class="mt-2 text-3xl font-semibold text-white">{{ project?.name }}</h1>
      <p class="text-slate-400">{{ project?.description || "No description" }}</p>
    </div>

    <section class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-semibold text-white">API Keys</h2>
          <p class="text-sm text-slate-400">Manage API keys tied to this project.</p>
        </div>
        <button @click="openCreate" class="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-400">Create key</button>
      </div>

      <div v-if="keysLoading" class="flex items-center justify-center py-12 text-slate-500">
        <svg class="h-5 w-5 animate-spin mr-2" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
        Loading keys...
      </div>

      <div v-else-if="keys.length === 0" class="rounded-2xl border border-dashed border-slate-700 p-8 text-center text-slate-500">
        No API keys for this project. Create one for your AI agents.
      </div>

      <div v-else class="space-y-3">
        <div v-for="key in keys" :key="key.id" class="flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-950 p-4">
          <div class="min-w-0">
            <p class="font-semibold text-white">{{ key.name }}</p>
            <p class="text-xs text-slate-500 mt-0.5">Permissions: {{ Object.keys(key.permissions).join(", ") || "none" }} &middot; Created: {{ formatDate(key.created_at) }}</p>
          </div>
          <button @click="confirmDelete(key)" class="shrink-0 rounded-xl bg-red-900/50 px-3 py-1.5 text-xs text-red-300 hover:bg-red-800/50">Revoke</button>
        </div>
      </div>
    </section>

    <Modal v-model="showCreate" title="Create API Key">
      <form @submit.prevent="createKey" class="space-y-4">
        <div>
          <label class="block text-sm text-slate-400 mb-1">Name</label>
          <input v-model="form.name" required placeholder="e.g. my-coding-agent" class="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-white focus:border-brand-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-2">Permissions</label>
          <div class="space-y-2">
            <label v-for="perm in permissionOptions" :key="perm.key" class="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-800/50 px-4 py-2.5">
              <input type="checkbox" v-model="form.permissions[perm.key]" class="rounded border-slate-600 bg-slate-700 text-brand-500 focus:ring-brand-500" />
              <span class="text-sm text-slate-300">{{ perm.label }}</span>
            </label>
          </div>
        </div>
        <div v-if="newKey" class="rounded-xl border border-brand-500/30 bg-brand-500/10 p-4">
          <p class="text-sm font-semibold text-brand-300">Key created! Copy it now — it won't be shown again.</p>
          <div class="mt-2">
            <CodeBlock :code="newKey" lang="plain" />
          </div>
        </div>
        <div v-if="!newKey" class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showCreate = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-xl bg-brand-500 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-400">Create</button>
        </div>
        <div v-else class="flex justify-end pt-2">
          <button type="button" @click="showCreate = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Done</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="showDelete" title="Revoke API Key?">
      <p class="text-slate-400 mb-6">Revoke <strong class="text-white">{{ deleting?.name }}</strong>? Any agent using this key will immediately lose access.</p>
      <div class="flex justify-end gap-3">
        <button @click="showDelete = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
        <button @click="deleteKey" class="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-500">Revoke</button>
      </div>
    </Modal>
  </template>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute } from "#app"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const route = useRoute()
const project = ref<any | null>(null)
const loading = ref(true)
const error = ref("")
const keys = ref<any[]>([])
const keysLoading = ref(true)
const showCreate = ref(false)
const showDelete = ref(false)
const deleting = ref<any | null>(null)
const newKey = ref<string | null>(null)

const permissionOptions = [
  { key: "read_notes", label: "Read notes & tasks" },
  { key: "write_notes", label: "Create & edit notes & tasks" },
]

const form = ref({ name: "", permissions: { read_notes: false, write_notes: false } })

const projectId = route.params.id as string

function formatDate(d: string) {
  return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
}

async function fetchProject() {
  try {
    project.value = (await api.get(`/projects/${projectId}`)).data
  } catch (e: any) {
    error.value = e?.response?.data?.detail || "Failed to load project"
  } finally {
    loading.value = false
  }
}

async function fetchKeys() {
  keysLoading.value = true
  try {
    keys.value = (await api.get(`/api-keys/project/${projectId}`)).data
  } catch {
    keys.value = []
  } finally {
    keysLoading.value = false
  }
}

function openCreate() {
  form.value = { name: "", permissions: { read_notes: false, write_notes: false } }
  newKey.value = null
  showCreate.value = true
}

function confirmDelete(key: any) { deleting.value = key; showDelete.value = true }

async function createKey() {
  try {
    const res = await api.post("/api-keys", { ...form.value, project_id: projectId })
    newKey.value = res.data.plain_text_key
    await fetchKeys()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error creating key") }
}

async function deleteKey() {
  if (!deleting.value) return
  try {
    await api.delete(`/api-keys/${deleting.value.id}`)
    showDelete.value = false; deleting.value = null; await fetchKeys()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error revoking key") }
}

onMounted(() => { fetchProject(); fetchKeys() })
</script>
