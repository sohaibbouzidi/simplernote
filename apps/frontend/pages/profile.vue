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

    <div class="mt-10 border-t border-slate-800 pt-8">
      <h2 class="text-lg font-semibold text-white">Two-Factor Authentication</h2>
      <p class="mt-1 text-sm text-slate-400">Add an extra layer of security to your account using an authenticator app.</p>

      <template v-if="isTotpEnabled">
        <div class="mt-4 rounded-lg bg-green-900/20 border border-green-800/40 px-4 py-3 text-sm text-green-400">
          2FA is currently enabled.
        </div>
        <form @submit.prevent="disableTotp" class="mt-4 max-w-sm space-y-4">
          <div>
            <label class="block text-sm text-slate-400 mb-1">Enter your password to disable</label>
            <input v-model="disableTotpPassword" type="password" class="w-full rounded border border-slate-800 bg-surface-50 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-brand-400 focus:outline-none" placeholder="Your password" required />
          </div>
          <p v-if="totpMessage" class="text-sm" :class="totpMessageType">{{ totpMessage }}</p>
          <button type="submit" :disabled="totpSaving" class="rounded border border-red-800/50 bg-red-900/20 px-4 py-2 text-sm text-red-400 hover:bg-red-900/30 disabled:opacity-50">Disable 2FA</button>
        </form>
      </template>

      <template v-else>
        <template v-if="totpSetupData">
          <div class="mt-4 p-4 rounded-lg bg-slate-800/30 border border-slate-700/50">
            <p class="text-sm text-slate-400 mb-3">Scan this QR code with your authenticator app (e.g. Google Authenticator, Authy):</p>
            <div class="flex justify-center mb-4">
              <img :src="totpSetupData.qr_svg" alt="TOTP QR Code" class="rounded-lg" />
            </div>
            <p class="text-xs text-slate-500 mb-2">Or enter this key manually: <code class="text-violet-400 bg-slate-800 px-2 py-0.5 rounded select-all">{{ totpSetupData.secret }}</code></p>
            <form @submit.prevent="verifyTotpSetup" class="mt-4 space-y-4">
              <div>
                <label class="block text-sm text-slate-400 mb-1">Verify the code from your app</label>
                <input v-model="totpVerifyCode" type="text" inputmode="numeric" class="w-full rounded border border-slate-800 bg-surface-50 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-brand-400 focus:outline-none" placeholder="000000" maxlength="6" required />
              </div>
              <p v-if="totpMessage" class="text-sm" :class="totpMessageType">{{ totpMessage }}</p>
              <div class="flex gap-3">
                <button type="submit" :disabled="totpSaving" class="rounded border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700 disabled:opacity-50">Verify &amp; Enable</button>
                <button type="button" @click="cancelTotpSetup" class="rounded border border-slate-800 px-4 py-2 text-sm text-slate-400 hover:text-white disabled:opacity-50">Cancel</button>
              </div>
            </form>
          </div>
        </template>
        <button v-else @click="setupTotp" :disabled="totpSaving" class="mt-4 rounded border border-slate-800 bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-700 disabled:opacity-50">Enable 2FA</button>
      </template>
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
const isTotpEnabled = computed(() => auth.totpEnabled)
const totpSetupData = ref<{ secret: string; provisioning_uri: string; qr_svg: string } | null>(null)
const totpVerifyCode = ref("")
const disableTotpPassword = ref("")
const totpMessage = ref("")
const totpMessageType = ref("")
const totpSaving = ref(false)

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

function cancelTotpSetup() {
  totpSetupData.value = null
  totpVerifyCode.value = ""
  totpMessage.value = ""
}

async function setupTotp() {
  totpSaving.value = true
  totpMessage.value = ""
  try {
    const res = await api.post("/auth/totp/setup")
    totpSetupData.value = res.data
  } catch (e: any) {
    totpMessage.value = e?.response?.data?.detail || "Failed to start 2FA setup"
    totpMessageType.value = "text-red-400"
  } finally {
    totpSaving.value = false
  }
}

async function verifyTotpSetup() {
  totpSaving.value = true
  totpMessage.value = ""
  try {
    await api.post("/auth/totp/verify", { code: totpVerifyCode.value })
    totpSetupData.value = null
    totpVerifyCode.value = ""
    totpMessage.value = "2FA enabled successfully"
    totpMessageType.value = "text-green-400"
    if (auth.user) (auth.user as any).totp_enabled = true
    auth.totpEnabled = true
  } catch (e: any) {
    totpMessage.value = e?.response?.data?.detail || "Invalid code"
    totpMessageType.value = "text-red-400"
  } finally {
    totpSaving.value = false
  }
}

async function disableTotp() {
  totpSaving.value = true
  totpMessage.value = ""
  try {
    await api.post("/auth/totp/disable", { password: disableTotpPassword.value })
    disableTotpPassword.value = ""
    totpMessage.value = "2FA disabled successfully"
    totpMessageType.value = "text-green-400"
    if (auth.user) (auth.user as any).totp_enabled = false
    auth.totpEnabled = false
  } catch (e: any) {
    totpMessage.value = e?.response?.data?.detail || "Failed to disable"
    totpMessageType.value = "text-red-400"
  } finally {
    totpSaving.value = false
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
