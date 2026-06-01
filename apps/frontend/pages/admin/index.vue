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

    <div v-else>
      <div class="flex justify-end mb-4">
        <button @click="showCreate = true" class="rounded-md bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-600">Create User</button>
      </div>

      <div class="rounded-lg border border-slate-800 overflow-hidden">
      <table class="w-full text-left text-sm">
        <thead class="bg-surface-50 text-slate-400">
          <tr>
            <th class="px-5 py-3 font-medium">Name</th>
            <th class="px-5 py-3 font-medium">Email</th>
            <th class="px-5 py-3 font-medium">Role</th>
            <th class="px-5 py-3 font-medium">Active</th>
            <th class="px-5 py-3 font-medium">Is Valid</th>
            <th class="px-5 py-3 font-medium">Created</th>
            <th class="px-5 py-3 font-medium">Last Login</th>
            <th class="px-5 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr v-for="user in users" :key="user.id" class="hover:bg-surface-50 transition-colors">
            <td class="px-5 py-3 text-white">{{ user.first_name || user.last_name ? `${user.first_name || ""} ${user.last_name || ""}`.trim() : "—" }}</td>
            <td class="px-5 py-3 text-slate-400">{{ user.email }}</td>
            <td class="px-5 py-3">
              <span :class="user.role === 'admin' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-slate-800 text-slate-400 border border-slate-700'" class="rounded-full px-2.5 py-0.5 text-xs font-medium">{{ user.role }}</span>
            </td>
            <td class="px-5 py-3">
              <span :class="user.is_active ? 'text-green-400' : 'text-red-400'" class="text-xs font-medium">{{ user.is_active ? "Active" : "Inactive" }}</span>
            </td>
            <td class="px-5 py-3">
              <span :class="user.email_confirmed ? 'text-green-400' : 'text-red-400'" class="text-xs font-medium">{{ user.email_confirmed ? "Valid" : "Pending" }}</span>
            </td>
            <td class="px-5 py-3 text-xs text-slate-400">{{ formatDate(user.created_at) }}</td>
            <td class="px-5 py-3 text-xs text-slate-400">{{ user.last_login_at ? formatDate(user.last_login_at) : "—" }}</td>
            <td class="px-5 py-3">
              <div class="flex items-center gap-2 justify-end">
                <button v-if="!user.email_confirmed" @click="verifyEmail(user.id)" class="rounded-md border border-green-800 px-2.5 py-1 text-xs text-green-400 hover:bg-green-500/10">Validate</button>
                <button v-if="user.role !== 'admin'" @click="promote(user.id)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-white hover:bg-slate-800">Promote</button>
                <button v-else @click="demote(user.id)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-amber-400 hover:bg-slate-800">Demote</button>
                <button v-if="user.is_active" @click="confirmToggleActive(user)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-red-400 hover:bg-red-500/10">Disable</button>
                <button v-else @click="toggleActive(user)" class="rounded-md border border-slate-800 px-2.5 py-1 text-xs text-green-400 hover:bg-green-500/10">Enable</button>
                <button @click="confirmHardDelete(user)" class="rounded-md border border-red-900 px-2.5 py-1 text-xs text-red-400 hover:bg-red-500/10">Delete Permanently</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>

    <Modal v-model="showCreate" title="Create User">
      <form @submit.prevent="createUser" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs text-slate-400">First Name</label>
            <input v-model="createForm.first_name" type="text" class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div>
            <label class="mb-1 block text-xs text-slate-400">Last Name</label>
            <input v-model="createForm.last_name" type="text" class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-indigo-500 focus:outline-none" />
          </div>
        </div>
        <div>
          <label class="mb-1 block text-xs text-slate-400">Email <span class="text-red-400">*</span></label>
          <input v-model="createForm.email" type="email" required class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-indigo-500 focus:outline-none" />
        </div>
        <div>
          <label class="mb-1 block text-xs text-slate-400">Password <span class="text-red-400">*</span></label>
          <input v-model="createForm.password" type="password" required class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-indigo-500 focus:outline-none" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs text-slate-400">Country</label>
            <input v-model="createForm.country" type="text" class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div>
            <label class="mb-1 block text-xs text-slate-400">City</label>
            <input v-model="createForm.city" type="text" class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-indigo-500 focus:outline-none" />
          </div>
        </div>
        <div class="flex items-center gap-6">
          <div>
            <label class="mb-1 block text-xs text-slate-400">Role</label>
            <select v-model="createForm.role" class="rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white focus:border-indigo-500 focus:outline-none">
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <label class="flex items-center gap-2 pt-5 text-sm text-slate-400">
            <input v-model="createForm.email_confirmed" type="checkbox" class="rounded border-slate-700 bg-slate-900 text-indigo-500 focus:ring-indigo-500" />
            Mark email as confirmed
          </label>
        </div>
        <p v-if="createError" class="text-sm text-red-400">{{ createError }}</p>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showCreate = false; createError = ''" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
          <button type="submit" class="rounded-md bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-600">Create</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="showConfirm" :title="disabling?.is_active === false ? 'Enable user?' : 'Disable user?'">
      <p class="text-sm text-slate-400 mb-6">
        <template v-if="disabling?.is_active === false">Enable user <strong class="text-white">{{ disabling?.email }}</strong>? They will be able to log in again.</template>
        <template v-else>Disable user <strong class="text-white">{{ disabling?.email }}</strong>? They will be unable to log in.</template>
      </p>
      <div class="flex justify-end gap-3">
        <button @click="showConfirm = false" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
        <button @click="confirmToggle" :class="disabling?.is_active === false ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'" class="rounded-md border border-slate-800 px-4 py-2 text-sm font-semibold text-white">{{ disabling?.is_active === false ? 'Enable' : 'Disable' }}</button>
      </div>
    </Modal>

    <Modal v-model="showHardDelete" title="Delete user permanently?">
      <p class="text-sm text-slate-400 mb-2">This will permanently delete <strong class="text-white">{{ hardDeleting?.email }}</strong> and <strong class="text-red-400">all their data</strong> (projects, notes, tasks, API keys, activity logs).</p>
      <p class="text-sm text-slate-400 mb-4">Type their email to confirm:</p>
      <input v-model="hardDeleteConfirmEmail" type="text" :placeholder="hardDeleting?.email" class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-600 focus:border-red-500 focus:outline-none" />
      <div class="flex justify-end gap-3 mt-5">
        <button @click="showHardDelete = false; hardDeleteConfirmEmail = ''" class="rounded-md border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700">Cancel</button>
        <button @click="executeHardDelete" :disabled="hardDeleteConfirmEmail !== hardDeleting?.email" class="rounded-md border border-slate-800 bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 disabled:opacity-40 disabled:cursor-not-allowed">Permanently Delete</button>
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
const showConfirm = ref(false)
const disabling = ref<any | null>(null)
const showHardDelete = ref(false)
const hardDeleting = ref<any | null>(null)
const hardDeleteConfirmEmail = ref("")
const showCreate = ref(false)
const createForm = ref({ email: "", password: "", first_name: "", last_name: "", country: "", city: "", role: "user", email_confirmed: false })
const createError = ref("")

async function createUser() {
  createError.value = ""
  try {
    await api.post("/admin/users", createForm.value)
    showCreate.value = false
    createForm.value = { email: "", password: "", first_name: "", last_name: "", country: "", city: "", role: "user", email_confirmed: false }
    toast.success("User created successfully")
    await fetchUsers()
  } catch (e: any) {
    createError.value = e?.response?.data?.detail || "Failed to create user"
  }
}

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

async function verifyEmail(id: string) {
  try { await api.patch(`/admin/users/${id}/verify-email`); await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

async function toggleActive(user: any) {
  try { await api.patch(`/admin/users/${user.id}/toggle-active`); await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

function confirmToggleActive(user: any) { disabling.value = user; showConfirm.value = true }

async function confirmToggle() {
  if (!disabling.value) return
  try { await api.patch(`/admin/users/${disabling.value.id}/toggle-active`); showConfirm.value = false; disabling.value = null; await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

function confirmHardDelete(user: any) { hardDeleting.value = user; hardDeleteConfirmEmail.value = ""; showHardDelete.value = true }

async function executeHardDelete() {
  if (!hardDeleting.value || hardDeleteConfirmEmail.value !== hardDeleting.value.email) return
  try { await api.delete(`/admin/users/${hardDeleting.value.id}/hard`); showHardDelete.value = false; hardDeleting.value = null; hardDeleteConfirmEmail.value = ""; await fetchUsers() } catch (e: any) { toast.error(e?.response?.data?.detail || "Error") }
}

onMounted(fetchUsers)
</script>
