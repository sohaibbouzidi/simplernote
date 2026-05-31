<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
    <!-- Header -->
    <div class="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="mb-6">
          <h1 class="text-4xl font-bold mb-2">API Documentation</h1>
          <p class="text-slate-400">All endpoints for AI agent integration — authentication via <code class="text-brand-400">X-API-KEY</code> header</p>
        </div>
        <div class="flex flex-col sm:flex-row gap-4">
          <!-- Search Bar -->
          <div class="flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search endpoints..."
              class="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <!-- Method Filter -->
          <select
            v-model="selectedMethod"
            class="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          >
            <option value="">All Methods</option>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PATCH">PATCH</option>
            <option value="DELETE">DELETE</option>
          </select>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- API Info -->
      <div class="mb-8 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <p class="text-slate-400 text-sm mb-1">Base URL</p>
          <p class="text-lg font-mono">http://localhost/api</p>
        </div>
        <div class="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <p class="text-slate-400 text-sm mb-1">Total Resources</p>
          <p class="text-lg font-bold">{{ Object.keys(apiData.resources).length }}</p>
        </div>
        <div class="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <p class="text-slate-400 text-sm mb-1">Total Endpoints</p>
          <p class="text-lg font-bold">{{ totalEndpoints }}</p>
        </div>
        <div class="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <p class="text-slate-400 text-sm mb-1">Auth Methods</p>
          <p class="text-sm">JWT • API Key</p>
        </div>
      </div>

      <!-- Resource Tabs -->
      <div class="mb-8">
        <div class="flex flex-wrap gap-2 mb-6">
          <button
            v-for="resource in sortedResources"
            :key="resource"
            @click="selectedResource = resource"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all',
              selectedResource === resource
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 border border-slate-700 text-slate-300 hover:border-slate-600'
            ]"
          >
            {{ formatResourceName(resource) }}
            <span class="ml-2 text-xs bg-slate-700 px-2 py-1 rounded">
              {{ apiData.resources[resource].endpoints.length }}
            </span>
          </button>
        </div>
      </div>

      <!-- Endpoints List -->
      <div class="space-y-4">
        <div
          v-for="endpoint in filteredEndpoints"
          :key="`${endpoint.resource}-${endpoint.method}-${endpoint.route}`"
          class="bg-slate-800 border border-slate-700 rounded-lg overflow-hidden hover:border-slate-600 transition-all group cursor-pointer"
          @click="selectEndpoint(endpoint)"
        >
          <div class="p-6">
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <div :class="['px-3 py-1 rounded-md font-mono text-sm font-bold whitespace-nowrap', methodColors[endpoint.method]]">
                  {{ endpoint.method }}
                </div>
                <div class="min-w-0 flex-1">
                  <p class="font-mono text-blue-400 group-hover:text-blue-300 transition-colors truncate">
                    {{ endpoint.route }}
                  </p>
                  <p class="text-slate-400 text-sm mt-1">{{ endpoint.description }}</p>
                </div>
              </div>
              <svg class="w-5 h-5 text-slate-500 group-hover:text-slate-400 transition-colors flex-shrink-0 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>

            <!-- Meta Info -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm mt-4">
              <div v-if="endpoint.response_model" class="flex items-center gap-2">
                <span class="text-slate-500">Response:</span>
                <span class="text-slate-300">{{ endpoint.response_model }}</span>
              </div>
              <div v-if="endpoint.status_code" class="flex items-center gap-2">
                <span class="text-slate-500">Status:</span>
                <span class="text-green-400">{{ endpoint.status_code }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-slate-500">Permissions:</span>
                <span class="text-amber-400">{{ formatPermissions(endpoint.permissions) }}</span>
              </div>
              <div v-if="endpoint.query_parameters && endpoint.query_parameters.length" class="flex items-center gap-2">
                <span class="text-slate-500">Params:</span>
                <span class="text-cyan-400">{{ endpoint.query_parameters.length }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredEndpoints.length === 0" class="text-center py-12 text-slate-400">
          <p>No endpoints match your search criteria</p>
        </div>
      </div>

      <!-- Detailed View Modal -->
      <div
        v-if="selectedEndpointDetail"
        class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 overflow-y-auto"
        @click="selectedEndpointDetail = null"
      >
        <div class="min-h-screen flex items-center justify-center p-4" @click.stop="">
          <div
            class="bg-slate-800 border border-slate-700 rounded-lg w-full max-w-3xl max-h-96 overflow-y-auto shadow-2xl"
            @click.stop=""
          >
            <div class="sticky top-0 bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
              <h2 class="text-xl font-bold">Endpoint Details</h2>
              <button
                @click="selectedEndpointDetail = null"
                class="text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div class="p-6 space-y-6">
              <!-- Route -->
              <div>
                <p class="text-slate-400 text-sm mb-2">Route</p>
                <div class="flex items-center gap-2">
                  <span :class="['px-3 py-1 rounded-md font-mono text-sm font-bold', methodColors[selectedEndpointDetail.method]]">
                    {{ selectedEndpointDetail.method }}
                  </span>
                  <code class="flex-1 bg-slate-900 px-3 py-2 rounded text-blue-400 font-mono text-sm overflow-x-auto">
                    {{ selectedEndpointDetail.route }}
                  </code>
                </div>
              </div>

              <!-- Description -->
              <div>
                <p class="text-slate-400 text-sm mb-2">Description</p>
                <p class="text-white">{{ selectedEndpointDetail.description }}</p>
              </div>

              <!-- Query Parameters -->
              <div v-if="selectedEndpointDetail.query_parameters && selectedEndpointDetail.query_parameters.length">
                <p class="text-slate-400 text-sm mb-2">Query Parameters</p>
                <div class="space-y-2">
                  <div
                    v-for="param in selectedEndpointDetail.query_parameters"
                    :key="param.name"
                    class="bg-slate-900 p-3 rounded"
                  >
                    <p class="font-mono text-blue-400">{{ param.name }}: <span class="text-cyan-400">{{ param.type }}</span></p>
                    <p v-if="param.default" class="text-slate-400 text-sm">Default: {{ param.default }}</p>
                  </div>
                </div>
              </div>

              <!-- Path Parameters -->
              <div v-if="selectedEndpointDetail.path_parameters && selectedEndpointDetail.path_parameters.length">
                <p class="text-slate-400 text-sm mb-2">Path Parameters</p>
                <div class="space-y-2">
                  <div
                    v-for="param in selectedEndpointDetail.path_parameters"
                    :key="param.name"
                    class="bg-slate-900 p-3 rounded"
                  >
                    <p class="font-mono text-orange-400">{{ param.name }}: <span class="text-cyan-400">{{ param.type }}</span></p>
                  </div>
                </div>
              </div>

              <!-- Request Model -->
              <div v-if="selectedEndpointDetail.request_model">
                <p class="text-slate-400 text-sm mb-2">Request Body</p>
                <code class="bg-slate-900 px-3 py-2 rounded text-green-400 font-mono text-sm block">
                  {{ selectedEndpointDetail.request_model }}
                </code>
              </div>

              <!-- Response Model -->
              <div v-if="selectedEndpointDetail.response_model">
                <p class="text-slate-400 text-sm mb-2">Response</p>
                <code class="bg-slate-900 px-3 py-2 rounded text-green-400 font-mono text-sm block">
                  {{ selectedEndpointDetail.response_model }}
                </code>
              </div>

              <!-- Permissions -->
              <div>
                <p class="text-slate-400 text-sm mb-2">Permissions</p>
                <p class="text-amber-400">{{ formatPermissions(selectedEndpointDetail.permissions) }}</p>
              </div>

              <!-- Status Code -->
              <div v-if="selectedEndpointDetail.status_code">
                <p class="text-slate-400 text-sm mb-2">Status Code</p>
                <p class="text-green-400 font-mono">{{ selectedEndpointDetail.status_code }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Permission Levels Info -->
      <div class="mt-16 pt-8 border-t border-slate-700">
        <h3 class="text-xl font-bold mb-6">Permission Levels</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="(description, permission) in apiData.permission_levels"
            :key="permission"
            class="bg-slate-800 border border-slate-700 rounded-lg p-4"
          >
            <p class="text-amber-400 font-mono font-bold mb-1">{{ permission }}</p>
            <p class="text-slate-300 text-sm">{{ description }}</p>
          </div>
        </div>
      </div>

      <!-- Features Info -->
      <div class="mt-8">
        <h3 class="text-xl font-bold mb-6">Key Features</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
            <p class="text-green-400 font-bold mb-2">✓ Soft Delete</p>
            <p class="text-slate-300 text-sm">Notes, tasks, and projects support soft deletes - recoverable items</p>
          </div>
          <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
            <p class="text-green-400 font-bold mb-2">✓ Rate Limiting</p>
            <p class="text-slate-300 text-sm">Global rate limiting with configurable limits per endpoint</p>
          </div>
          <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
            <p class="text-green-400 font-bold mb-2">✓ Audit Trail</p>
            <p class="text-slate-300 text-sm">All actions tracked with authentication method</p>
          </div>
          <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
            <p class="text-green-400 font-bold mb-2">✓ Dual Auth</p>
            <p class="text-slate-300 text-sm">JWT tokens and API key authentication supported</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRuntimeConfig } from '#app'

const config = useRuntimeConfig()

const apiData = {
  api_structure: {
    base_url: config.public.apiBase,
    authentication: "X-API-KEY header",
    analysis_date: "2026-05-30"
  },
  resources: {
    ai_agent: {
      file_path: "apps/backend/app/api/endpoints/ai_agent.py",
      base_route: "/ai-agent",
      description: "Full CRUD over a single project via X-API-KEY auth — notes, tasks, and AI context",
      endpoints: [
        {
          method: "GET",
          route: "/ai-agent/projects",
          description: "List accessible projects (scoped to API key project if bound)",
          request_model: null,
          response_model: "List[ProjectSchema]",
          query_parameters: [],
          permissions: "authenticated"
        },
        {
          method: "GET",
          route: "/ai-agent/projects/{project_id}/notes",
          description: "List notes in a project, with optional type and search filters",
          request_model: null,
          response_model: "List[NoteSchema]",
          query_parameters: [
            { name: "note_type", type: "Optional[str]" },
            { name: "search", type: "Optional[str]" }
          ],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "read_notes"
        },
        {
          method: "POST",
          route: "/ai-agent/projects/{project_id}/notes",
          description: "Create a new note in the project",
          request_model: "NoteCreateSchema",
          response_model: "NoteSchema",
          status_code: 201,
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "write_notes"
        },
        {
          method: "PATCH",
          route: "/ai-agent/projects/{project_id}/notes/{note_id}",
          description: "Update an existing note",
          request_model: "NoteUpdateSchema",
          response_model: "NoteSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" },
            { name: "note_id", type: "str" }
          ],
          permissions: "write_notes"
        },
        {
          method: "DELETE",
          route: "/ai-agent/projects/{project_id}/notes/{note_id}",
          description: "Soft-delete a note",
          request_model: null,
          response_model: null,
          status_code: 204,
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" },
            { name: "note_id", type: "str" }
          ],
          permissions: "write_notes"
        },
        {
          method: "PATCH",
          route: "/ai-agent/projects/{project_id}/notes/{note_id}/restore",
          description: "Restore a soft-deleted note",
          request_model: null,
          response_model: "NoteSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" },
            { name: "note_id", type: "str" }
          ],
          permissions: "write_notes"
        },
        {
          method: "GET",
          route: "/ai-agent/projects/{project_id}/tasks",
          description: "List tasks in a project, optionally filtered by status",
          request_model: null,
          response_model: "List[TaskSchema]",
          query_parameters: [
            { name: "status", type: "Optional[str]" }
          ],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "read_tasks"
        },
        {
          method: "POST",
          route: "/ai-agent/projects/{project_id}/tasks",
          description: "Create a new task in the project",
          request_model: "TaskCreateSchema",
          response_model: "TaskSchema",
          status_code: 201,
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "write_tasks"
        },
        {
          method: "PATCH",
          route: "/ai-agent/projects/{project_id}/tasks/{task_id}",
          description: "Update an existing task",
          request_model: "TaskUpdateSchema",
          response_model: "TaskSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" },
            { name: "task_id", type: "str" }
          ],
          permissions: "write_tasks"
        },
        {
          method: "DELETE",
          route: "/ai-agent/projects/{project_id}/tasks/{task_id}",
          description: "Soft-delete a task",
          request_model: null,
          response_model: null,
          status_code: 204,
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" },
            { name: "task_id", type: "str" }
          ],
          permissions: "write_tasks"
        },
        {
          method: "PATCH",
          route: "/ai-agent/projects/{project_id}/tasks/{task_id}/restore",
          description: "Restore a soft-deleted task",
          request_model: null,
          response_model: "TaskSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" },
            { name: "task_id", type: "str" }
          ],
          permissions: "write_tasks"
        },
        {
          method: "GET",
          route: "/ai-agent/projects/{project_id}/context",
          description: "Get the AI context document for a project",
          request_model: null,
          response_model: "AiContextSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "read_ai_context"
        },
        {
          method: "POST",
          route: "/ai-agent/projects/{project_id}/context",
          description: "Create a new AI context for a project",
          request_model: "object (content: string)",
          response_model: "AiContextSchema",
          status_code: 201,
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "write_ai_context"
        },
        {
          method: "PUT",
          route: "/ai-agent/projects/{project_id}/context",
          description: "Replace the AI context content for a project",
          request_model: "object (content: string)",
          response_model: "AiContextSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "write_ai_context"
        },
        {
          method: "DELETE",
          route: "/ai-agent/projects/{project_id}/context",
          description: "Delete the AI context for a project",
          request_model: null,
          response_model: null,
          status_code: 204,
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "write_ai_context"
        },
        {
          method: "POST",
          route: "/ai-agent/projects/{project_id}/context/import",
          description: "Auto-import all notes and tasks into the AI context document",
          request_model: "object ({})",
          response_model: "AiContextSchema",
          query_parameters: [],
          path_parameters: [
            { name: "project_id", type: "str" }
          ],
          permissions: "write_ai_context"
        },
        {
          method: "GET",
          route: "/ai-agent/search",
          description: "Search across all notes and tasks by text query",
          request_model: null,
          response_model: "List[SearchResultItem]",
          query_parameters: [
            { name: "query", type: "str", required: true },
            { name: "project_id", type: "Optional[str]" }
          ],
          permissions: "read_notes, read_tasks"
        }
      ]
    }
  },
  permission_levels: {
    read_notes: "Permission to read notes",
    write_notes: "Permission to create/update/delete notes",
    read_tasks: "Permission to read tasks",
    write_tasks: "Permission to create/update/delete tasks",
    read_ai_context: "Permission to read AI context",
    write_ai_context: "Permission to create/update/delete AI context"
  }
}

const searchQuery = ref('')
const selectedMethod = ref('')
const selectedResource = ref('ai_agent')
const selectedEndpointDetail = ref(null)

const methodColors = {
  GET: 'bg-blue-600/30 text-blue-300 border border-blue-600/50',
  POST: 'bg-green-600/30 text-green-300 border border-green-600/50',
  PATCH: 'bg-amber-600/30 text-amber-300 border border-amber-600/50',
  DELETE: 'bg-red-600/30 text-red-300 border border-red-600/50'
}

const sortedResources = computed(() => {
  return Object.keys(apiData.resources).sort()
})

const totalEndpoints = computed(() => {
  return Object.values(apiData.resources).reduce((acc, resource) => acc + resource.endpoints.length, 0)
})

const filteredEndpoints = computed(() => {
  const allEndpoints = []
  
  Object.entries(apiData.resources).forEach(([resourceKey, resource]) => {
    resource.endpoints.forEach((endpoint) => {
      allEndpoints.push({
        resource: resourceKey,
        ...endpoint
      })
    })
  })

  return allEndpoints
    .filter(endpoint => {
      const matchesSearch = 
        searchQuery.value === '' ||
        endpoint.route.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        endpoint.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      
      const matchesMethod = selectedMethod.value === '' || endpoint.method === selectedMethod.value
      const matchesResource = selectedResource.value === '' || endpoint.resource === selectedResource.value
      
      return matchesSearch && matchesMethod && matchesResource
    })
    .sort((a, b) => {
      const order = { GET: 0, POST: 1, PATCH: 2, DELETE: 3 }
      return (order[a.method] || 0) - (order[b.method] || 0)
    })
})

const formatResourceName = (resource) => {
  return resource.charAt(0).toUpperCase() + resource.slice(1).replace(/_/g, ' ')
}

const formatPermissions = (permissions) => {
  if (!permissions) return 'N/A'
  if (typeof permissions === 'string') {
    return permissions
      .replace(/^none \(public endpoint\)$/, 'Public')
      .replace(/^authenticated$/, 'Authenticated')
      .replace(/_/g, ' ')
      .split(',')
      .map(p => p.trim())
      .join(', ')
  }
  return 'N/A'
}

const selectEndpoint = (endpoint) => {
  selectedEndpointDetail.value = endpoint
}
</script>
