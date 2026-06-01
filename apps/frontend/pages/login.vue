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
          <div v-if="showConfirmationBanner" class="mb-6 rounded-lg bg-violet-500/10 px-4 py-3 text-sm text-violet-300">
            <p class="font-medium">Account created!</p>
            <p class="mt-1">Check your email for a confirmation link. Some features may require email verification.</p>
          </div>
          <template v-if="showTotpChallenge">
            <h1 class="mb-1 font-display text-2xl font-semibold text-white">Two-Factor Authentication</h1>
            <p class="mb-8 text-sm text-slate-400">Enter the code from your authenticator app.</p>
            <form @submit.prevent="submitTotp" class="space-y-5">
              <div>
                <label class="mb-2 block text-sm font-medium text-slate-300">Authentication code</label>
                <input v-model="totpCode" type="text" inputmode="numeric" autocomplete="one-time-code" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-center text-2xl tracking-[0.5em] text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" placeholder="000000" maxlength="6" />
              </div>
              <div v-if="totpError" class="rounded-lg bg-red-500/10 px-4 py-3 text-sm text-red-400">
                <p>{{ totpError }}</p>
              </div>
              <button type="submit" :disabled="totpSubmitting" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed">
                {{ totpSubmitting ? 'Verifying...' : 'Verify' }}
              </button>
              <button type="button" @click="showTotpChallenge = false; totpCode = ''; totpError = ''" class="w-full text-center text-sm text-slate-500 hover:text-slate-400 transition-colors">Back to login</button>
            </form>
          </template>
          <template v-else>
          <h1 class="mb-1 font-display text-2xl font-semibold text-white">Welcome back</h1>
          <p class="mb-8 text-sm text-slate-400">Sign in to your account to continue.</p>
          <form @submit.prevent="submit" class="space-y-5">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Email</label>
              <input v-model="email" @input="clearFieldError('email')" type="email" autocomplete="email" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.email ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="you@example.com" />
              <p v-if="fieldErrors.email" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.email }}</p>
            </div>
            <div>
              <div class="mb-2 flex items-center justify-between">
                <label class="block text-sm font-medium text-slate-300">Password</label>
                <NuxtLink to="/forgot-password" class="text-xs font-medium text-violet-400 transition-colors hover:text-violet-300">Forgot password?</NuxtLink>
              </div>
              <input v-model="password" @input="clearFieldError('password')" type="password" autocomplete="current-password" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.password ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="Enter your password" />
              <p v-if="fieldErrors.password" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.password }}</p>
            </div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="rememberMe" type="checkbox" class="rounded border-slate-700 bg-surface text-violet-500 focus:ring-violet-500/20" />
              <span class="text-sm text-slate-400">Keep me signed in for 30 days</span>
            </label>
            <div v-if="formError" class="rounded-lg bg-red-500/10 px-4 py-3 text-sm text-red-400">
              <p>{{ formError }}</p>
              <button v-if="showResend" @click="resendConfirmation" :disabled="resending" class="mt-2 text-violet-400 underline hover:text-violet-300 disabled:opacity-50">
                {{ resending ? "Sending..." : "Resend confirmation email" }}
              </button>
            </div>
            <button type="submit" :disabled="submitting" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed">
              {{ submitting ? 'Signing in...' : 'Sign in' }}
            </button>
            <p class="text-center text-sm text-slate-500">
              Don't have an account?
              <NuxtLink :to="'/register' + (redirect ? '?redirect=' + encodeURIComponent(redirect) : '')" class="font-medium text-violet-400 transition-colors hover:text-violet-300">Register</NuxtLink>
            </p>
          </form>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import { useRouter, useRoute } from "#app"
import { useAuthStore } from "@/stores/auth"
import { useToast } from "@/composables/useToast"
import { getApiInstance } from "@/services/api"

definePageMeta({ layout: false })

const api = getApiInstance()
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()

const email = ref("")
const password = ref("")
const redirect = (route.query.redirect as string) || ""
const showConfirmationBanner = route.query.registered === "1"
const submitting = ref(false)
const formError = ref("")
const fieldErrors = reactive<{ email?: string; password?: string }>({})
const rememberMe = ref(false)
const showResend = ref(false)
const resending = ref(false)
const showTotpChallenge = ref(false)
const totpCode = ref("")
const totpError = ref("")
const totpSubmitting = ref(false)
const tempToken = ref("")

function clearFieldError(field: "email" | "password") {
  fieldErrors[field] = undefined
  formError.value = ""
}

const submit = async () => {
  fieldErrors.email = undefined
  fieldErrors.password = undefined
  formError.value = ""

  if (!email.value.trim()) {
    fieldErrors.email = "Email is required"
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    fieldErrors.email = "Enter a valid email address"
    return
  }
  if (!password.value) {
    fieldErrors.password = "Password is required"
    return
  }

  submitting.value = true
  try {
    const result = await auth.login(email.value, password.value, rememberMe.value)
    if (result.totp_required) {
      tempToken.value = result.temp_token
      showTotpChallenge.value = true
      return
    }
    await router.push(redirect || "/dashboard")
  } catch (error: any) {
    const status = error?.response?.status
    const detail = error?.response?.data?.detail

    if (!error.response) {
      formError.value = "Connection error. Please check your network and try again."
    } else if (status === 429) {
      formError.value = "Too many login attempts. Please wait a moment and try again."
    } else if (status === 401) {
      formError.value = "Invalid email or password."
      showResend.value = false
    } else if (status === 403) {
      if (detail === "Account is disabled") {
        formError.value = "This account has been disabled. Contact an administrator."
        showResend.value = false
      } else {
        formError.value = detail || "Please confirm your email before logging in."
        showResend.value = true
      }
    } else if (status === 422 && Array.isArray(detail)) {
      detail.forEach((err: any) => {
        const field = err.loc?.at(-1)
        if (field === "email") fieldErrors.email = err.msg
        else if (field === "password") fieldErrors.password = err.msg
      })
      if (!fieldErrors.email && !fieldErrors.password) {
        formError.value = "Please check your input and try again."
      }
    } else {
      formError.value = typeof detail === "string" ? detail : "Login failed. Please try again."
    }
  } finally {
    submitting.value = false
  }
}

async function submitTotp() {
  totpError.value = ""
  if (totpCode.value.length !== 6 || !/^\d{6}$/.test(totpCode.value)) {
    totpError.value = "Enter a 6-digit code"
    return
  }
  totpSubmitting.value = true
  try {
    const res = await api.post("/auth/login/totp", { temp_token: tempToken.value, code: totpCode.value })
    auth.setToken(res.data.access_token)
    auth.refreshToken = res.data.refresh_token
    await auth.fetchUser()
    auth._persist()
    await router.push(redirect || "/dashboard")
  } catch (e: any) {
    totpError.value = e?.response?.data?.detail || "Invalid code. Try again."
  } finally {
    totpSubmitting.value = false
  }
}

async function resendConfirmation() {
  resending.value = true
  try {
    await api.post("/auth/resend-confirmation", { email: email.value })
    formError.value = "Confirmation email sent. Check your inbox."
    showResend.value = false
  } catch (e: any) {
    formError.value = e?.response?.data?.detail || "Failed to resend. Try again later."
  } finally {
    resending.value = false
  }
}
</script>
