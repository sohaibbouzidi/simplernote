<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-semibold text-white">Admin</h1>
      <p class="text-slate-400">Manage users and their roles.</p>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500">
      <svg class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
      <span class="ml-3">Loading users...</span>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-800/50 bg-red-950/30 p-6 text-center text-red-400">
      <p>{{ error }}</p>
      <button @click="fetchUsers" class="mt-3 rounded-xl bg-red-800/30 px-4 py-2 text-sm hover:bg-red-800/50">Retry</button>
    </div>

    <div v-else class="rounded-3xl border border-slate-800 overflow-hidden">
      <table class="w-full text-left text-sm">
        <thead class="bg-slate-900/80 text-slate-400">
          <tr>
            <th class="px-6 py-4 font-medium">Email</th>
            <th class="px-6 py-4 font-medium">Role</th>
            <th class="px-6 py-4 font-medium">Active</th>
            <th class="px-6 py-4 font-medium">Created</th>
            <th class="px-6 py-4 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr v-for="user in users" :key="user.id" class="bg-slate-950 transition hover:bg-slate-900/50">
            <td class="px-6 py-4 text-white">{{ user.email }}</td>
            <td class="px-6 py-4">
              <span :class="user.role === 'admin' ? 'bg-violet-500/20 text-violet-300' : 'bg-slate-800 text-slate-400'" class="rounded-full px-3 py-1 text-xs font-medium">{{ user.role }}</span>
            </td>
            <td class="px-6 py-4">
              <span :class="user.is_active ? 'text-green-400' : 'text-red-400'" class="text-sm">{{ user.is_active ? "Active" : "Inactive" }}</span>
            </td>
            <td class="px-6 py-4 text-slate-400">{{ formatDate(user.created_at) }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-2">
                <button v-if="user.role !== 'admin'" @click="promote(user)" class="rounded-lg bg-violet-900/50 px-3 py-1.5 text-xs text-violet-300 hover:bg-violet-800/50">Promote</button>
                <button v-if="user.role === 'admin' && user.id !== auth.user?.id" @click="demote(user)" class="rounded-lg bg-amber-900/50 px-3 py-1.5 text-xs text-amber-300 hover:bg-amber-800/50">Demote</button>
                <button v-if="user.id !== auth.user?.id" @click="confirmDelete(user)" class="rounded-lg bg-red-900/50 px-3 py-1.5 text-xs text-red-300 hover:bg-red-800/50">Delete</button>
                <span v-else class="text-xs text-slate-600">You</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Modal v-model="showDelete" title="Delete User?">
      <p class="text-slate-400 mb-6">Permanently delete <strong class="text-white">{{ deleting?.email }}</strong> and all associated data?</p>
      <div class="flex justify-end gap-3">
        <button @click="showDelete = false" class="rounded-xl bg-slate-800 px-5 py-2.5 text-sm text-slate-300 hover:bg-slate-700">Cancel</button>
        <button @click="deleteUser" class="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-500">Delete</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"
import { useAuthStore } from "@/stores/auth"

const api = getApiInstance()
const auth = useAuthStore()
const users = ref<any[]>([])
const loading = ref(true)
const error = ref("")
const showDelete = ref(false)
const deleting = ref<any | null>(null)

function formatDate(d: string) {
  return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
}

async function fetchUsers() {
  loading.value = true; error.value = ""
  try { users.value = (await api.get("/admin/users")).data } catch (e: any) { error.value = e?.response?.data?.detail || "Failed to load users"; users.value = [] }
  finally { loading.value = false }
}

async function promote(user: any) {
  try {
    await api.patch(`/admin/users/${user.id}/role?role=admin`)
    await fetchUsers()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error promoting user") }
}

async function demote(user: any) {
  try {
    await api.patch(`/admin/users/${user.id}/role?role=user`)
    await fetchUsers()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error demoting user") }
}

function confirmDelete(user: any) { deleting.value = user; showDelete.value = true }

async function deleteUser() {
  if (!deleting.value) return
  try {
    await api.delete(`/admin/users/${deleting.value.id}`)
    showDelete.value = false; deleting.value = null; await fetchUsers()
  } catch (e: any) { alert(e?.response?.data?.detail || "Error deleting user") }
}

onMounted(fetchUsers)
</script>
