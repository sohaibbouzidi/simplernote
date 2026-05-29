<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-semibold text-white">Admin</h1>
      <p class="text-sm text-slate-400">Manage users and their roles.</p>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-400">
      <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading users...</span>
    </div>

    <div v-else-if="error" class="rounded-lg border border-red-500/50 bg-red-500/10 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchUsers" class="mt-3 rounded-md bg-slate-800 px-4 py-2 text-sm hover:bg-slate-700">Retry</button>
    </div>

    <div v-else class="rounded-lg border border-slate-800 overflow-hidden">
      <table class="w-full text-left text-sm">
        <thead class="bg-surface-50 text-slate-400">
          <tr>
            <th class="px-5 py-3 font-medium">Email</th>
            <th class="px-5 py-3 font-medium">Role</th>
            <th class="px-5 py-3 font-medium">Active</th>
            <th class="px-5 py-3 font-medium">Created</th>
            <th class="px-5 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr v-for="user in users" :key="user.id" class="hover:bg-surface-50 transition-colors">
            <td class="px-5 py-3 text-white">{{ user.email }}</td>
            <td class="px-5 py-3">
              <span :class="user.role === 'admin' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-slate-800 text-slate-400 border border-slate-700'" class="rounded-full px-2.5 py-0.5 text-xs font-medium">{{ user.role }}</span>
            </td>
            <td class="px-5 py-3">
              <span :class="user.is_active ? 'text-green-400' : 'text-red-400'" class="text-xs font-medium">{{ user.is_active ? "Active" : "Inactive" }}</span>
            </td>
            <td class="px-5 py-3 text-xs text-slate-400">{{ formatDate(user.created_at) }}</td>
            <td class="px-5 py-3">
              <div class="flex items-center gap-2">
                <button v-if="user.role !== 'admin'" @click="promote(user.id)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-white hover:bg-slate-800">Promote</button>
                <button v-else @click="demote(user.id)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-amber-400 hover:bg-slate-800">Demote</button>
                <button @click="confirmDelete(user)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-red-400 hover:bg-red-500/10">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Modal v-model="showDelete" title="Delete user?">
      <p class="text-sm text-slate-400 mb-6">Delete user <strong class="text-white">{{ deleting?.email }}</strong>? This cannot be undone.</p>
      <div class="flex justify-end gap-3">
        <button @click="showDelete = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
        <button @click="deleteUser" class="rounded-md border border-slate-800 bg-red-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600">Delete</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"
import { useToast } from "@/composables/useToast"

const api = getApiInstance()
const toast = useToast()
const users = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showDelete = ref(false)
const deleting = ref<any | null>(null)

function formatDate(d: string) {
  if (!d) return ""
  return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
}

async function fetchUsers() {
  loading.value = true; error.value = ""
  try { users.value = (await api.get("/admin/users")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load users" }
  finally { loading.value = false }
}

async function promote(id: string) {
  try { await api.patch(`/admin/users/${id}/role`, { role: "admin" }); await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

async function demote(id: string) {
  try { await api.patch(`/admin/users/${id}/role`, { role: "user" }); await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

function confirmDelete(user: any) { deleting.value = user; showDelete.value = true }

async function deleteUser() {
  if (!deleting.value) return
  try { await api.delete(`/admin/users/${deleting.value.id}`); showDelete.value = false; deleting.value = null; await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

onMounted(fetchUsers)
</script>
