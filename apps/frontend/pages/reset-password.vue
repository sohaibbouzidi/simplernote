<template>
  <div class="flex min-h-screen bg-surface">
    <div class="hidden w-1/2 flex-col items-center justify-center bg-gradient-to-br from-surface-50 via-surface to-surface p-12 lg:flex">
      <div class="max-w-md animate-fade-in-up">
        <NuxtLink to="/" class="mb-8 inline-flex items-center gap-3">
          <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-fuchsia-400 text-lg font-bold leading-none text-white shadow-lg shadow-violet-500/20">S</span>
          <span class="font-display text-2xl font-semibold tracking-tight text-white">Simplernote</span>
        </NuxtLink>
        <h2 class="mt-12 font-display text-3xl font-semibold leading-tight text-white">Your AI-ready<br />note &amp; task hub</h2>
        <p class="mt-4 text-base leading-relaxed text-slate-400">Organize projects, manage tasks, and give your AI agents persistent memory — all in one place.</p>
        <div class="mt-10 space-y-5">
          <div class="flex items-start gap-3 text-sm text-slate-400">
            <span class="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500/20 text-xs text-violet-400">✓</span>
            <span>Structured notes with types, tags, and metadata</span>
          </div>
          <div class="flex items-start gap-3 text-sm text-slate-400">
            <span class="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500/20 text-xs text-violet-400">✓</span>
            <span>Kanban-style task management with 8 status lanes</span>
          </div>
          <div class="flex items-start gap-3 text-sm text-slate-400">
            <span class="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500/20 text-xs text-violet-400">✓</span>
            <span>Project-scoped API keys for AI agent integration</span>
          </div>
        </div>
      </div>
    </div>
    <div class="flex w-full items-center justify-center px-6 lg:w-1/2">
      <div class="w-full max-w-md animate-fade-in-up">
        <div class="mb-8 text-center lg:hidden">
          <NuxtLink to="/" class="inline-flex items-center gap-2.5">
            <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-fuchsia-400 text-sm font-bold leading-none text-white shadow-lg shadow-violet-500/20">S</span>
            <span class="font-display text-xl font-semibold tracking-tight text-white">Simplernote</span>
          </NuxtLink>
        </div>
        <div class="rounded-2xl border border-slate-800/60 bg-surface-50 p-8 shadow-2xl shadow-black/40">
          <template v-if="resetDone">
            <div class="text-center">
              <div class="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full bg-green-500/20">
                <svg class="h-7 w-7 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
              </div>
              <h1 class="mb-2 font-display text-2xl font-semibold text-white">Password reset</h1>
              <p class="mb-6 text-sm text-slate-400">Your password has been reset successfully.</p>
              <NuxtLink to="/login" class="inline-block rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110">Sign in</NuxtLink>
            </div>
          </template>
          <template v-else>
            <h1 class="mb-1 font-display text-2xl font-semibold text-white">Set new password</h1>
            <p class="mb-8 text-sm text-slate-400">Choose a strong password for your account.</p>
            <form @submit.prevent="submit" class="space-y-5">
              <div>
                <label class="mb-2 block text-sm font-medium text-slate-300">New password</label>
                <input v-model="newPassword" @input="clearError" type="password" autocomplete="new-password" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', error ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="New password" />
                <ul class="mt-2 space-y-1">
                  <li v-for="c in criteria" :key="c.label" class="flex items-center gap-1.5 text-xs" :class="c.met ? 'text-green-400' : 'text-slate-500'">
                    <span>{{ c.met ? '✓' : '○' }}</span>
                    <span>{{ c.label }}</span>
                  </li>
                </ul>
              </div>
              <div>
                <label class="mb-2 block text-sm font-medium text-slate-300">Confirm password</label>
                <input v-model="confirmPassword" @input="clearError" type="password" autocomplete="new-password" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', confirmError ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="Confirm new password" />
                <p v-if="confirmError" class="mt-1.5 text-xs text-red-400">{{ confirmError }}</p>
              </div>
              <p v-if="formError" class="rounded-lg bg-red-500/10 px-4 py-3 text-sm text-red-400">{{ formError }}</p>
              <button type="submit" :disabled="submitting" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed">
                {{ submitting ? 'Resetting...' : 'Reset password' }}
              </button>
            </form>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import { useRoute } from "#app"
import { getApiInstance } from "@/services/api"

definePageMeta({ layout: false })

const route = useRoute()
const token = (route.query.token as string) || ""

const newPassword = ref("")
const confirmPassword = ref("")
const submitting = ref(false)
const error = ref("")
const confirmError = ref("")
const formError = ref("")
const resetDone = ref(false)

function clearError() {
  error.value = ""
  confirmError.value = ""
  formError.value = ""
}

const criteria = computed(() => {
  const pw = newPassword.value
  return [
    { label: "At least 8 characters", met: pw.length >= 8 },
    { label: "One uppercase letter", met: /[A-Z]/.test(pw) },
    { label: "One lowercase letter", met: /[a-z]/.test(pw) },
    { label: "One digit", met: /\d/.test(pw) },
    { label: "One special character", met: /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\';\/`~]/.test(pw) },
  ]
})

const submit = async () => {
  error.value = ""
  confirmError.value = ""
  formError.value = ""

  if (!newPassword.value) {
    error.value = "Password is required"
    return
  }
  if (newPassword.value.length < 8) {
    error.value = "Password must be at least 8 characters"
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    confirmError.value = "Passwords do not match"
    return
  }

  submitting.value = true
  try {
    const api = getApiInstance()
    await api.post("/auth/reset-password", { token, new_password: newPassword.value })
    resetDone.value = true
  } catch (err: any) {
    const status = err?.response?.status
    const detail = err?.response?.data?.detail
    if (status === 429) {
      formError.value = "Too many attempts. Please wait a moment and try again."
    } else if (status === 400) {
      formError.value = typeof detail === "string" ? detail : "Invalid or expired reset link."
    } else {
      formError.value = "Something went wrong. Please try again."
    }
  } finally {
    submitting.value = false
  }
}
</script>
