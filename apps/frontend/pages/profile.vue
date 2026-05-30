<template>
  <div class="max-w-3xl mx-auto">
    <div class="flex items-center gap-4">
      <div v-if="user?.picture_url" class="h-24 w-24 rounded-full overflow-hidden">
        <img :src="user.picture_url" alt="avatar" class="h-full w-full object-cover" />
      </div>
      <div v-else class="h-24 w-24 rounded-full bg-slate-700 flex items-center justify-center text-2xl font-semibold text-white">{{ initials }}</div>
      <div>
        <h1 class="text-2xl font-semibold">{{ fullName }}</h1>
        <p class="text-sm text-slate-400">{{ user?.email }}</p>
      </div>
    </div>

    <div class="mt-6 p-4 border border-slate-800 rounded bg-surface-50">
      <p><strong>Country:</strong> {{ user?.country || '-' }}</p>
      <p><strong>City:</strong> {{ user?.city || '-' }}</p>
    </div>

    <div class="mt-6 flex gap-3">
      <NuxtLink to="/complete-profile" class="rounded px-4 py-2 bg-violet-500 text-white">Edit profile</NuxtLink>
    </div>

    <div class="mt-10 border-t border-slate-800 pt-8">
      <h2 class="text-lg font-semibold text-white">Change Password</h2>
      <form @submit.prevent="changePassword" class="mt-4 max-w-sm space-y-4">
        <div>
          <label class="block text-sm text-slate-400 mb-1">Current password</label>
          <input v-model="oldPassword" type="password" class="w-full rounded border border-slate-800 bg-surface-50 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-brand-400 focus:outline-none" placeholder="Enter current password" required />
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">New password</label>
          <input v-model="newPassword" type="password" class="w-full rounded border border-slate-800 bg-surface-50 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-brand-400 focus:outline-none" placeholder="Enter new password" required />
          <ul class="mt-2 space-y-1">
            <li v-for="c in newPasswordCriteria" :key="c.label" class="flex items-center gap-1.5 text-xs" :class="c.met ? 'text-green-400' : 'text-slate-500'">
              <span>{{ c.met ? '✓' : '○' }}</span>
              <span>{{ c.label }}</span>
            </li>
          </ul>
        </div>
        <div>
          <label class="block text-sm text-slate-400 mb-1">Confirm new password</label>
          <input v-model="confirmPassword" type="password" class="w-full rounded border border-slate-800 bg-surface-50 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-brand-400 focus:outline-none" placeholder="Confirm new password" required />
        </div>
        <p v-if="passwordError" class="text-sm text-red-400">{{ passwordError }}</p>
        <p v-if="passwordSuccess" class="text-sm text-green-400">{{ passwordSuccess }}</p>
        <button type="submit" :disabled="passwordSaving" class="rounded border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700 disabled:opacity-50">Update password</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useAuthStore } from "@/stores/auth"
import { getApiInstance } from "@/services/api"

const auth = useAuthStore()
const user = auth.user
const api = getApiInstance()
const oldPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")
const passwordError = ref("")
const passwordSuccess = ref("")
const passwordSaving = ref(false)

const newPasswordCriteria = computed(() => {
  const pw = newPassword.value
  return [
    { label: "At least 8 characters", met: pw.length >= 8 },
    { label: "One uppercase letter", met: /[A-Z]/.test(pw) },
    { label: "One lowercase letter", met: /[a-z]/.test(pw) },
    { label: "One digit", met: /\d/.test(pw) },
    { label: "One special character", met: /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\';\/`~]/.test(pw) },
  ]
})

onMounted(() => {
  if (!auth.user) auth.fetchUser()
})

function validatePassword(pw: string): string | null {
  if (pw.length < 8) return "Password must be at least 8 characters"
  if (!/[A-Z]/.test(pw)) return "Password must contain at least one uppercase letter"
  if (!/[a-z]/.test(pw)) return "Password must contain at least one lowercase letter"
  if (!/\d/.test(pw)) return "Password must contain at least one digit"
  if (!/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\';\/`~]/.test(pw)) return "Password must contain at least one special character"
  return null
}

async function changePassword() {
  passwordError.value = ""
  passwordSuccess.value = ""
  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = "New passwords do not match"
    return
  }
  const err = validatePassword(newPassword.value)
  if (err) {
    passwordError.value = err
    return
  }
  passwordSaving.value = true
  try {
    await api.patch("/auth/password", {
      old_password: oldPassword.value,
      new_password: newPassword.value,
    })
    passwordSuccess.value = "Password updated successfully"
    oldPassword.value = ""
    newPassword.value = ""
    confirmPassword.value = ""
  } catch (e: any) {
    passwordError.value = e?.response?.data?.detail || "Failed to update password"
  } finally {
    passwordSaving.value = false
  }
}

const initials = computed(() => {
  const u = auth.user
  if (!u) return ""
  if (u.first_name || u.last_name) {
    const f = u.first_name ? u.first_name.charAt(0) : ""
    const l = u.last_name ? u.last_name.charAt(0) : ""
    return (f + l).toUpperCase().slice(0, 2)
  }
  return u.email ? u.email.charAt(0).toUpperCase() : ""
})

const fullName = computed(() => {
  const u = auth.user
  if (!u) return ""
  const name = `${u.first_name || ""} ${u.last_name || ""}`.trim()
  return name || u.email || ""
})
</script>
