<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">API Keys</h1>
        <p class="text-slate-400">Create and manage keys for external agents.</p>
      </div>
      <button @click="openCreate" class="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-400">Create key</button>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading API keys...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchKeys" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <div v-else-if="keys.length === 0" class="rounded-3xl border border-slate-800 bg-slate-950 p-8 text-center text-slate-500">
      No API keys yet. Create one for your AI agents.
    </div>

    <div v-else class="space-y-4">
      <div v-for="key in keys" :key="key.id" class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <h2 class="text-lg font-semibold text-white">{{ key.name }}</h2>
            <p class="text-slate-400 text-sm mt-1">Permissions: {{ Object.keys(key.permissions).join(", ") || "none" }}</p>
            <p class="text-slate-500 text-xs mt-1">Created: {{ formatDate(key.created_at) }}</p>
          </div>
          <button @click="confirmDelete(key)" class="shrink-0 rounded-xl bg-red-900/50 px-3 py-1.5 text-xs text-red-300 hover:bg-red-800/50">Revoke</button>
        </div>
      </div>
    </div>

    <div v-if="keys.length > 0" class="rounded-3xl border border-slate-800/50 bg-surface-50/50 overflow-hidden">
      <button @click="showGuide = !showGuide" class="flex w-full items-center justify-between px-6 py-4 text-left transition hover:bg-slate-800/20">
        <div>
          <h3 class="font-display text-lg font-semibold text-white">AI Agent Setup Guide</h3>
          <p class="text-sm text-slate-400">How to connect AI agents to the Simplernote API using your API key.</p>
        </div>
        <svg :class="showGuide ? 'rotate-180' : ''" class="h-5 w-5 text-slate-400 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
      </button>

      <div v-if="showGuide" class="border-t border-slate-800/50 px-6 py-6 space-y-8">

        <div>
          <h4 class="font-semibold text-white mb-2">1. Authentication</h4>
          <p class="text-sm text-slate-400 mb-3">Include your API key in the <code class="text-brand-300">Authorization</code> header of every request.</p>
          <CodeBlock :code="snippets.auth" lang="http" />
        </div>

        <div>
          <h4 class="font-semibold text-white mb-2">2. AI Context (Search &amp; Import)</h4>
          <p class="text-sm text-slate-400 mb-3">Search across notes and tasks, or batch-import data for your AI agent.</p>
          <div class="space-y-3">
            <div>
              <p class="text-xs text-slate-500 mb-1.5">Search knowledge base</p>
              <CodeBlock :code="snippets.aiSearch" lang="bash" />
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1.5">Import notes &amp; tasks</p>
              <CodeBlock :code="snippets.aiImport" lang="bash" />
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-semibold text-white mb-2">3. Notes</h4>
          <div class="space-y-3">
            <div>
              <p class="text-xs text-slate-500 mb-1.5">List all notes</p>
              <CodeBlock :code="snippets.notesList" lang="bash" />
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1.5">Create a note</p>
              <CodeBlock :code="snippets.notesCreate" lang="bash" />
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-semibold text-white mb-2">4. Tasks</h4>
          <div class="space-y-3">
            <div>
              <p class="text-xs text-slate-500 mb-1.5">List all tasks</p>
              <CodeBlock :code="snippets.tasksList" lang="bash" />
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1.5">Create a task</p>
              <CodeBlock :code="snippets.tasksCreate" lang="bash" />
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-semibold text-white mb-2">5. Projects</h4>
          <div class="space-y-3">
            <div>
              <p class="text-xs text-slate-500 mb-1.5">List all projects</p>
              <CodeBlock :code="snippets.projectsList" lang="bash" />
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1.5">Create a project</p>
              <CodeBlock :code="snippets.projectsCreate" lang="bash" />
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-semibold text-white mb-2">6. Python (requests)</h4>
          <CodeBlock :code="snippets.python" lang="python" />
        </div>

        <div>
          <h4 class="font-semibold text-white mb-2">7. JavaScript (fetch)</h4>
          <CodeBlock :code="snippets.javascript" lang="javascript" />
        </div>

      </div>
    </div>

    <Modal v-model="showModal" title="Create API Key">
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
          <button type="button" @click="showModal = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-xl bg-brand-500 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-400">Create</button>
        </div>
        <div v-else class="flex justify-end pt-2">
          <button type="button" @click="showModal = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Done</button>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const api = getApiInstance()
const keys = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showGuide = ref(false)
const showModal = ref(false)
const showDelete = ref(false)
const deleting = ref<any | null>(null)
const newKey = ref<string | null>(null)

const permissionOptions = [
  { key: "read_notes", label: "Read notes & tasks" },
  { key: "write_notes", label: "Create & edit notes & tasks" },
]

const form = ref({ name: "", permissions: { read_notes: false, write_notes: false } })

const snippets = {
  auth: "Authorization: Bearer YOUR_API_KEY",
  aiSearch: `curl -H "Authorization: Bearer YOUR_API_KEY" "http://localhost:8000/api/ai-context/search?query=your+search+term"`,
  aiImport: `curl -X POST "http://localhost:8000/api/ai-context/import" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "notes": [
    {"project_id": "...", "title": "Note title", "content": "Note content", "note_type": "memory"}
  ],
  "tasks": [
    {"project_id": "...", "title": "Task title", "description": "Task description", "status": "todo"}
  ]
}'`,
  notesList: `curl -H "Authorization: Bearer YOUR_API_KEY" "http://localhost:8000/api/notes"`,
  notesCreate: `curl -X POST "http://localhost:8000/api/notes" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "project_id": "...",
  "title": "My Note",
  "content": "Note content here",
  "summary": "Brief summary",
  "note_type": "documentation",
  "tags": ["ai", "notes"]
}'`,
  tasksList: `curl -H "Authorization: Bearer YOUR_API_KEY" "http://localhost:8000/api/tasks"`,
  tasksCreate: `curl -X POST "http://localhost:8000/api/tasks" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "project_id": "...",
  "title": "My Task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium",
  "assigned_agent": "my-agent"
}'`,
  projectsList: `curl -H "Authorization: Bearer YOUR_API_KEY" "http://localhost:8000/api/projects"`,
  projectsCreate: `curl -X POST "http://localhost:8000/api/projects" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"name": "My Project", "description": "Project description"}'`,
  python: `import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# List projects
projects = requests.get(f"{BASE_URL}/projects", headers=HEADERS).json()
print(f"Projects: {len(projects)}")

# Create a note
note = requests.post(f"{BASE_URL}/notes", headers=HEADERS, json={
    "project_id": projects[0]["id"],
    "title": "AI Context Note",
    "content": "This was created by an AI agent",
    "note_type": "memory",
    "tags": ["ai"]
}).json()
print(f"Created note: {note['id']}")

# Search knowledge base
results = requests.get(
    f"{BASE_URL}/ai-context/search",
    params={"query": "AI context"},
    headers=HEADERS
).json()
print(f"Found {len(results['notes'])} notes, {len(results['tasks'])} tasks")`,
  javascript: `const API_KEY = "YOUR_API_KEY";
const BASE_URL = "http://localhost:8000/api";
const HEADERS = { Authorization: \`Bearer \${API_KEY}\` };

// List projects
const projects = await fetch(\`\${BASE_URL}/projects\`, { headers: HEADERS }).then(r => r.json());
console.log(\`Projects: \${projects.length}\`);

// Create a note
const note = await fetch(\`\${BASE_URL}/notes\`, {
  method: "POST",
  headers: { ...HEADERS, "Content-Type": "application/json" },
  body: JSON.stringify({
    project_id: projects[0].id,
    title: "AI Context Note",
    content: "Created by an AI agent",
    note_type: "memory",
    tags: ["ai"]
  })
}).then(r => r.json());
console.log(\`Created note: \${note.id}\`);

// Search knowledge base
const results = await fetch(
  \`\${BASE_URL}/ai-context/search?query=AI+context\`,
  { headers: HEADERS }
).then(r => r.json());
console.log(\`Found \${results.notes.length} notes, \${results.tasks.length} tasks\`);`,
}

function openCreate() {
  form.value = { name: "", permissions: { read_notes: false, write_notes: false } }
  newKey.value = null
  showModal.value = true
}

function confirmDelete(key: any) { deleting.value = key; showDelete.value = true }

function formatDate(d: string) {
  return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
}

async function fetchKeys() {
  loading.value = true; error.value = ""
  try { keys.value = (await api.get("/api-keys")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load API keys"; keys.value = [] }
  finally { loading.value = false }
}

async function createKey() {
  try {
    const res = await api.post("/api-keys", form.value)
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

onMounted(fetchKeys)
</script>
