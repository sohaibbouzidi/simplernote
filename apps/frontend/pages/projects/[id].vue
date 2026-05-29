<template>
  <div v-if="loading" class="flex items-center justify-center py-20 text-slate-400">
    <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
    <span class="ml-3">Loading project...</span>
  </div>

  <div v-else-if="error" class="rounded-lg border border-red-500/50 bg-red-500/10 p-6 text-center text-red-400">
    <p>{{ error }}</p>
  </div>

  <template v-else>
    <div class="mb-6">
      <NuxtLink to="/projects" class="text-sm text-slate-400 hover:text-brand-400">
        <svg class="mr-1 inline h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        Projects
      </NuxtLink>
      <div class="mt-2 flex items-start justify-between gap-4">
        <div class="min-w-0 flex-1">
          <h1 class="text-2xl font-semibold text-white">
            <span class="mr-2 inline-flex items-center justify-center rounded-md border border-slate-700 bg-slate-800 px-1.5 py-0.5 text-xs font-medium text-slate-400">project</span>
            {{ project?.name }}
          </h1>
          <p class="mt-1 text-sm text-slate-400">{{ project?.description || "No description" }}</p>
        </div>
      </div>
    </div>

    <div class="mb-6 border-b border-slate-800">
      <nav class="-mb-px flex gap-1">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
          'relative inline-flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors',
          activeTab === tab.key
            ? 'text-white after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-brand-400'
            : 'text-slate-400 hover:text-white hover:bg-surface-50'
        ]">
          <span v-html="tab.icon" class="h-4 w-4 inline-flex items-center justify-center" />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <div v-if="activeTab === 'notes'" class="space-y-4">
      <div class="flex items-center justify-between">
        <p class="text-sm text-slate-400">{{ notes.length }} note{{ notes.length !== 1 ? 's' : '' }}</p>
        <button @click="openCreateNote" class="rounded-md border border-slate-800 bg-brand-500 px-3 py-1.5 text-sm font-semibold text-white hover:bg-brand-400">New note</button>
      </div>

      <div v-if="notesLoading" class="flex items-center justify-center py-12 text-slate-400 text-sm">
        <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
        Loading notes...
      </div>

      <div v-else-if="notes.length === 0" class="rounded-lg border border-dashed border-slate-800 p-12 text-center">
        <svg class="mx-auto h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        <p class="mt-3 text-sm font-medium text-white">No notes yet</p>
        <p class="text-xs text-slate-400 mt-1">Create a note for this project.</p>
      </div>

      <div v-else class="rounded-lg border border-slate-800 divide-y divide-slate-800">
        <div v-for="note in notes" :key="note.id" class="px-4 py-3 hover:bg-surface-50 cursor-pointer" @click="openEditNote(note)">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0 flex-1">
              <p class="font-medium text-white truncate">{{ note.title }}</p>
              <p class="text-sm text-slate-400 line-clamp-2 mt-0.5">{{ note.summary || note.content || 'No content' }}</p>
            </div>
            <div class="flex shrink-0 items-center gap-2 text-xs text-slate-400">
              <span v-if="note.note_type" class="rounded-full border border-slate-700 px-2 py-0.5 text-xs">{{ note.note_type }}</span>
              <span>{{ formatDate(note.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <Modal v-model="showNoteModal" :title="editingNote ? 'Edit note' : 'New note'">
        <form @submit.prevent="saveNote" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-white mb-1">Title</label>
            <input v-model="noteForm.title" required class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-white mb-1">Content</label>
            <textarea v-model="noteForm.content" rows="5" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-white mb-1">Type</label>
            <input v-model="noteForm.note_type" placeholder="e.g. meeting, spec, idea" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white placeholder-slate-400 focus:border-brand-500 focus:outline-none" />
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showNoteModal = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
            <button type="submit" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">{{ editingNote ? 'Save' : 'Create' }}</button>
          </div>
        </form>
      </Modal>
    </div>

    <div v-if="activeTab === 'tasks'" class="space-y-4">
      <div class="flex items-center justify-between">
        <p class="text-sm text-slate-400">{{ tasks.length }} task{{ tasks.length !== 1 ? 's' : '' }}</p>
        <button @click="openCreateTask" class="rounded-md border border-slate-800 bg-brand-500 px-3 py-1.5 text-sm font-semibold text-white hover:bg-brand-400">New task</button>
      </div>

      <div v-if="tasksLoading" class="flex items-center justify-center py-12 text-slate-400 text-sm">
        <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
        Loading tasks...
      </div>

      <div v-else-if="tasks.length === 0" class="rounded-lg border border-dashed border-slate-800 p-12 text-center">
        <svg class="mx-auto h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
        <p class="mt-3 text-sm font-medium text-white">No tasks yet</p>
        <p class="text-xs text-slate-400 mt-1">Create a task for this project.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <div class="flex gap-4 min-w-max pb-2">
          <div v-for="lane in lanes" :key="lane.key" class="w-72 shrink-0">
            <div class="mb-2 flex items-center gap-2 px-1">
              <span :class="lane.dotClass" class="h-2.5 w-2.5 rounded-full inline-block" />
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">{{ lane.label }}</span>
              <span class="text-xs text-slate-400">{{ groupedTasks[lane.key]?.length || 0 }}</span>
            </div>
            <div class="space-y-2">
              <div v-for="task in (groupedTasks[lane.key] || [])" :key="task.id" :class="['rounded-lg border p-3 cursor-pointer transition-colors', task.status === 'done' ? 'border-slate-800 bg-surface-50 opacity-60 hover:opacity-100' : task.status === 'in-progress' ? 'border-brand-500/40 bg-surface-50 hover:bg-brand-500/10' : task.status === 'blocked' ? 'border-red-500/40 bg-surface-50 hover:bg-red-500/10' : 'border-slate-800 bg-surface-50 hover:bg-slate-800/50']" @click="openEditTask(task)">
                <p class="text-sm font-medium text-white">{{ task.title }}</p>
                <p v-if="task.description" class="mt-1 text-xs text-slate-400 line-clamp-2">{{ task.description }}</p>
                <div class="mt-2 flex items-center gap-2 text-xs text-slate-400">
                  <span v-if="task.priority" :class="task.priority === 'high' ? 'text-red-400' : task.priority === 'medium' ? 'text-amber-400' : 'text-slate-400'">{{ task.priority }}</span>
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
            <label class="block text-sm font-medium text-white mb-1">Title</label>
            <input v-model="taskForm.title" required class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-white mb-1">Description</label>
            <textarea v-model="taskForm.description" rows="3" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-white mb-1">Status</label>
              <SelectDropdown v-model="taskForm.status" :options="taskStatusOptions" />
            </div>
            <div>
              <label class="block text-sm font-medium text-white mb-1">Priority</label>
              <SelectDropdown v-model="taskForm.priority" :options="taskPriorityOptions" />
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showTaskModal = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
            <button type="submit" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">{{ editingTask ? 'Save' : 'Create' }}</button>
          </div>
        </form>
      </Modal>
    </div>

    <div v-if="activeTab === 'ai-context'" class="space-y-6">
      <div class="flex items-center gap-6 border-b border-slate-800">
        <button
          v-for="st in aiSubTabs"
          :key="st.key"
          @click="aiSubTab = st.key"
          class="relative pb-3 text-sm font-medium transition-colors"
          :class="aiSubTab === st.key ? 'text-white' : 'text-slate-400 hover:text-slate-200'"
        >
          {{ st.label }}
          <span v-if="aiSubTab === st.key" class="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-400" />
        </button>
        <div v-if="aiRateLimit" class="ml-auto flex items-center gap-1.5 text-xs text-slate-500">
          <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
          {{ aiRateLimit.remaining }}/{{ aiRateLimit.limit }} left
        </div>
      </div>

      <div v-if="aiSubTab === 'search'">
        <div class="mb-4 flex gap-3">
          <input
            v-model="aiSearchQuery"
            @keydown.enter="handleAiSearch"
            placeholder="Search notes and tasks..."
            class="flex-1 rounded-lg border border-slate-800 bg-surface px-4 py-2.5 text-sm text-white outline-none placeholder:text-slate-600 focus:border-brand-500"
          />
          <button
            @click="handleAiSearch"
            :disabled="!aiSearchQuery.trim()"
            class="rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-brand-600 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Search
          </button>
        </div>

        <div v-if="aiSearchLoading" class="flex items-center justify-center py-16">
          <svg class="h-8 w-8 animate-spin text-brand-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
          <span class="ml-3 text-sm text-slate-400">Searching...</span>
        </div>

        <div v-else-if="aiSearchError" class="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          <p>{{ aiSearchError }}</p>
        </div>

        <template v-else-if="aiSearchResults">
          <div v-if="aiSearchResults.notes.length > 0" class="mb-6">
            <h2 class="mb-3 text-sm font-semibold text-slate-300 uppercase tracking-wider">Notes ({{ aiSearchResults.notes.length }})</h2>
            <div class="space-y-2">
              <div v-for="note in aiSearchResults.notes" :key="note.id" class="rounded-lg border border-slate-800 bg-surface-50 px-4 py-3 transition-colors hover:border-slate-700">
                <div class="flex items-center gap-2">
                  <span class="font-medium text-white">{{ note.title }}</span>
                  <span class="rounded bg-slate-800 px-1.5 py-0.5 text-xs text-slate-400">{{ note.note_type }}</span>
                </div>
                <p class="mt-1 text-sm text-slate-500 line-clamp-1">{{ note.content || note.summary || "No content" }}</p>
                <div class="mt-1.5 flex items-center gap-3 text-xs text-slate-600">
                  <span v-if="note.tags?.length" class="flex gap-1">
                    <span v-for="tag in note.tags.slice(0, 3)" :key="tag" class="text-slate-500">#{{ tag }}</span>
                    <span v-if="note.tags.length > 3" class="text-slate-600">+{{ note.tags.length - 3 }}</span>
                  </span>
                  <span>{{ formatDate(note.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="aiSearchResults.tasks.length > 0" class="mb-6">
            <h2 class="mb-3 text-sm font-semibold text-slate-300 uppercase tracking-wider">Tasks ({{ aiSearchResults.tasks.length }})</h2>
            <div class="space-y-2">
              <div v-for="task in aiSearchResults.tasks" :key="task.id" class="rounded-lg border border-slate-800 bg-surface-50 px-4 py-3 transition-colors hover:border-slate-700">
                <div class="flex items-center gap-2">
                  <span class="font-medium text-white">{{ task.title }}</span>
                  <span class="rounded px-1.5 py-0.5 text-xs font-medium" :class="statusBadge(task.status)">{{ task.status }}</span>
                  <span class="rounded px-1.5 py-0.5 text-xs font-medium" :class="priorityBadge(task.priority)">{{ task.priority }}</span>
                </div>
                <p v-if="task.description" class="mt-1 text-sm text-slate-500 line-clamp-1">{{ task.description }}</p>
                <div class="mt-1.5 text-xs text-slate-600">{{ formatDate(task.created_at) }}</div>
              </div>
            </div>
          </div>

          <div v-if="aiSearchResults.notes.length === 0 && aiSearchResults.tasks.length === 0" class="py-16 text-center">
            <p class="text-sm text-slate-500">No results found for <span class="font-mono text-slate-400">"{{ aiLastQuery }}"</span></p>
          </div>
        </template>

        <div v-else class="py-16 text-center">
          <svg class="mx-auto mb-3 h-10 w-10 text-slate-700" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          <p class="text-sm text-slate-500">Search this project's notes and tasks</p>
          <p class="mt-1 text-xs text-slate-600">Enter a query above to find relevant context for your AI agents</p>
        </div>
      </div>

      <div v-if="aiSubTab === 'import'">
        <p class="mb-4 text-sm text-slate-400">Paste JSON below to batch import notes and tasks into this project.</p>
        <div class="mb-4">
          <textarea
            v-model="aiImportJson"
            @input="aiImportError = ''"
            rows="12"
            placeholder='{\n  "notes": [\n    {\n      "title": "My Note",\n      "content": "...",\n      "note_type": "documentation"\n    }\n  ],\n  "tasks": [\n    {\n      "title": "My Task",\n      "status": "todo",\n      "priority": "medium"\n    }\n  ]\n}'
            class="w-full rounded-lg border border-slate-800 bg-surface px-4 py-3 font-mono text-sm text-white outline-none placeholder:text-slate-700 focus:border-brand-500"
          ></textarea>
        </div>
        <div class="flex items-center gap-4">
          <label class="cursor-pointer rounded-lg border border-slate-800 bg-surface-50 px-4 py-2 text-sm text-slate-300 transition-colors hover:border-slate-700 hover:text-white">
            Upload .json
            <input type="file" accept=".json" @change="handleAiFileUpload" class="hidden" />
          </label>
          <button
            @click="handleAiImport"
            :disabled="!aiImportJson.trim() || aiImportLoading"
            class="rounded-lg bg-brand-500 px-5 py-2 text-sm font-semibold text-white transition-all hover:bg-brand-600 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <span v-if="aiImportLoading" class="flex items-center gap-2">
              <svg class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
              Importing...
            </span>
            <span v-else>Import</span>
          </button>
          <span v-if="aiImportError" class="text-sm text-red-400">{{ aiImportError }}</span>
          <span v-else-if="aiImportSuccess" class="text-sm text-green-400">{{ aiImportSuccess }}</span>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'settings'" class="max-w-2xl space-y-8">
      <section class="rounded-lg border border-slate-800">
        <div class="border-b border-slate-800 px-5 py-3">
          <h2 class="text-base font-semibold text-white">Project info</h2>
        </div>
        <div class="px-5 py-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-white mb-1">Name</label>
            <input v-model="settingsForm.name" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-white mb-1">Description</label>
            <textarea v-model="settingsForm.description" rows="3" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none" />
          </div>
          <div class="flex gap-3">
            <button @click="saveSettings" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">Save</button>
            <button @click="confirmDeleteProject" class="rounded-md border border-slate-800 bg-transparent px-4 py-2 text-sm text-red-400 hover:bg-red-500/10">Delete project</button>
          </div>
        </div>
      </section>

      <section class="rounded-lg border border-slate-800">
        <div class="border-b border-slate-800 px-5 py-3 flex items-center justify-between">
          <h2 class="text-base font-semibold text-white">API Keys</h2>
          <button v-if="keys.length === 0" @click="openCreateKey" class="rounded-md border border-slate-800 bg-brand-500 px-3 py-1.5 text-sm font-semibold text-white hover:bg-brand-400">Create key</button>
          <span v-else class="text-xs text-slate-500">Max 1 key per project</span>
        </div>
        <div v-if="keysLoading" class="px-5 py-8 text-center text-sm text-slate-400">
          <svg class="mx-auto h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
          <span class="ml-2">Loading keys...</span>
        </div>
        <div v-else-if="keys.length === 0" class="px-5 py-8 text-center text-sm text-slate-400">
          No API keys for this project. Create one to enable AI agent access.
        </div>
        <div v-else class="divide-y divide-slate-800">
          <div v-for="key in keys" :key="key.id" class="flex items-center justify-between px-5 py-3">
            <div class="min-w-0">
              <p class="font-medium text-white text-sm">{{ key.name }}</p>
              <p class="text-xs text-slate-400 mt-0.5">Permissions: {{ Object.keys(key.permissions).join(", ") || "none" }}</p>
            </div>
            <button @click="confirmDeleteKey(key)" class="shrink-0 rounded-md border border-slate-800 px-2.5 py-1 text-xs text-red-400 hover:bg-red-500/10">Revoke</button>
          </div>
        </div>
      </section>

      <Modal v-model="showCreateKey" title="Create API Key">
        <form @submit.prevent="createKey" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-white mb-1">Name</label>
            <input v-model="keyForm.name" required placeholder="e.g. my-coding-agent" class="w-full rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm text-white placeholder-slate-400 focus:border-brand-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-white mb-2">Permissions</label>
            <div class="space-y-2">
              <label v-for="perm in permissionOptions" :key="perm.key" class="flex items-center gap-3 rounded-md border border-slate-800 bg-surface-50 px-3 py-2">
                <input type="checkbox" v-model="keyForm.permissions[perm.key]" class="rounded border-slate-700 bg-surface text-brand-500 focus:ring-brand-500" />
                <span class="text-sm text-white">{{ perm.label }}</span>
              </label>
            </div>
          </div>
          <div v-if="newKeyValue" class="rounded-md border border-brand-500/30 bg-brand-500/10 p-3">
            <p class="text-sm font-semibold text-green-400">Key created! Copy it now — it won't be shown again.</p>
            <div class="mt-2">
              <CodeBlock :code="newKeyValue" lang="plain" />
            </div>
          </div>
          <div v-if="!newKeyValue" class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showCreateKey = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
            <button type="submit" class="rounded-md border border-slate-800 bg-brand-500 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-400">Create</button>
          </div>
          <div v-else class="flex justify-end pt-2">
            <button type="button" @click="showCreateKey = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Done</button>
          </div>
        </form>
      </Modal>

      <Modal v-model="showRevokeKey" title="Revoke API Key?">
        <p class="text-sm text-slate-400 mb-6">Revoke <strong class="text-white">{{ deletingKey?.name }}</strong>? Any agent using this key will immediately lose access.</p>
        <div class="flex justify-end gap-3">
          <button @click="showRevokeKey = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
          <button @click="deleteKey" class="rounded-md border border-slate-800 bg-red-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600">Revoke</button>
        </div>
      </Modal>

      <Modal v-model="showDeleteProject" title="Delete Project?">
        <p class="text-sm text-slate-400 mb-6">Delete <strong class="text-white">{{ project?.name }}</strong>? This will also delete all notes, tasks, and API keys in this project.</p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteProject = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
          <button @click="deleteProject" class="rounded-md border border-slate-800 bg-red-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600">Delete</button>
        </div>
      </Modal>
    </div>
  </template>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "#app"
import { getApiInstance } from "@/services/api"
import { useToast } from "@/composables/useToast"

const api = getApiInstance()
const route = useRoute()
const router = useRouter()
const projectId = route.params.id as string
const toast = useToast()

const project = ref<any | null>(null)
const loading = ref(true)
const error = ref("")
const activeTab = ref("notes")

const tabs = [
  { key: "notes", label: "Notes", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>' },
  { key: "tasks", label: "Tasks", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>' },
  { key: "ai-context", label: "AI Context", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>' },
  { key: "settings", label: "Settings", icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>' },
]

const settingsForm = ref({ name: "", description: "" })

const taskStatusOptions = [
  { value: "backlog", label: "Backlog" },
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "In Progress" },
  { value: "review", label: "Review" },
  { value: "blocked", label: "Blocked" },
  { value: "done", label: "Done" },
  { value: "cancelled", label: "Cancelled" },
  { value: "deferred", label: "Deferred" },
]

const taskPriorityOptions = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
]

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
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error saving project") }
}

function confirmDeleteProject() { showDeleteProject.value = true }

async function deleteProject() {
  try {
    await api.delete(`/projects/${projectId}`)
    showDeleteProject.value = false
    router.push("/projects")
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error deleting project") }
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
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error saving note") }
}

const tasks = ref<any[]>([])
const tasksLoading = ref(false)
const showTaskModal = ref(false)
const editingTask = ref<any | null>(null)
const taskForm = ref({ title: "", description: "", status: "todo", priority: "medium" })

const lanes = [
  { key: "backlog", label: "Backlog", dotClass: "bg-slate-400" },
  { key: "todo", label: "Todo", dotClass: "bg-slate-400" },
  { key: "in-progress", label: "In Progress", dotClass: "bg-brand-400" },
  { key: "review", label: "Review", dotClass: "bg-amber-400" },
  { key: "blocked", label: "Blocked", dotClass: "bg-red-500" },
  { key: "done", label: "Done", dotClass: "bg-green-400" },
  { key: "cancelled", label: "Cancelled", dotClass: "bg-slate-400" },
  { key: "deferred", label: "Deferred", dotClass: "bg-slate-400" },
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
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error saving task") }
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
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error revoking key") }
}

async function createKey() {
  try {
    const res = await api.post("/api-keys", { ...keyForm.value, project_id: projectId })
    newKeyValue.value = res.data.plain_text_key
    await fetchKeys()
  } catch (e: any) { toast.error(e?.response?.data?.detail || "Error creating key") }
}

const aiSubTabs = [
  { key: "search", label: "Search" },
  { key: "import", label: "Import" },
]
const aiSubTab = ref("search")
const aiSearchQuery = ref("")
const aiLastQuery = ref("")
const aiSearchLoading = ref(false)
const aiSearchError = ref("")
const aiSearchResults = ref<any | null>(null)
const aiImportJson = ref("")
const aiImportLoading = ref(false)
const aiImportError = ref("")
const aiImportSuccess = ref("")
const aiRateLimit = ref<{ limit: number; remaining: number } | null>(null)

async function handleAiSearch() {
  const q = aiSearchQuery.value.trim()
  if (!q) return
  aiLastQuery.value = q
  aiSearchLoading.value = true
  aiSearchError.value = ""
  aiSearchResults.value = null
  aiRateLimit.value = null
  try {
    const res = await api.get(`/ai-context/search?query=${encodeURIComponent(q)}&project_id=${projectId}`)
    aiSearchResults.value = res.data
    const limit = parseInt(res.headers["x-ratelimit-remaining"])
    if (!isNaN(limit)) {
      aiRateLimit.value = {
        limit: parseInt(res.headers["x-ratelimit-limit"]) || 30,
        remaining: limit,
      }
    }
  } catch (e: any) {
    aiSearchError.value = e?.response?.data?.detail || "Search failed"
  } finally {
    aiSearchLoading.value = false
  }
}

function handleAiFileUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    aiImportJson.value = reader.result as string
    aiImportError.value = ""
  }
  reader.readAsText(file)
}

async function handleAiImport() {
  let payload: any
  try {
    payload = JSON.parse(aiImportJson.value)
  } catch {
    aiImportError.value = "Invalid JSON"
    return
  }
  aiImportLoading.value = true
  aiImportError.value = ""
  aiImportSuccess.value = ""
  try {
    const res = await api.post("/ai-context/import", { ...payload, project_id: projectId })
    const notes = res.data.notes || 0
    const tasks = res.data.tasks || 0
    aiImportSuccess.value = `Imported ${notes} note${notes !== 1 ? "s" : ""} and ${tasks} task${tasks !== 1 ? "s" : ""}`
    aiImportJson.value = ""
  } catch (e: any) {
    aiImportError.value = e?.response?.data?.detail || "Import failed"
  } finally {
    aiImportLoading.value = false
  }
}

function statusBadge(status: string) {
  const map: Record<string, string> = {
    backlog: "bg-slate-400/10 text-slate-400",
    todo: "bg-slate-400/10 text-slate-400",
    "in-progress": "bg-brand-400/10 text-brand-400",
    review: "bg-amber-400/10 text-amber-400",
    blocked: "bg-red-400/10 text-red-400",
    done: "bg-green-400/10 text-green-400",
    cancelled: "bg-slate-400/10 text-slate-400",
    deferred: "bg-slate-400/10 text-slate-400",
  }
  return map[status] || "bg-slate-400/10 text-slate-400"
}

function priorityBadge(priority: string) {
  const map: Record<string, string> = {
    low: "bg-slate-400/10 text-slate-400",
    medium: "bg-amber-400/10 text-amber-400",
    high: "bg-red-400/10 text-red-400",
  }
  return map[priority] || "bg-slate-400/10 text-slate-400"
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
