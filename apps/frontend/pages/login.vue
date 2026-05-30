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
            <p v-if="formError" class="rounded-lg bg-red-500/10 px-4 py-3 text-sm text-red-400">{{ formError }}</p>
            <button type="submit" :disabled="submitting" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed">
              {{ submitting ? 'Signing in...' : 'Sign in' }}
            </button>
            <p class="text-center text-sm text-slate-500">
              Don't have an account?
              <NuxtLink :to="'/register' + (redirect ? '?redirect=' + encodeURIComponent(redirect) : '')" class="font-medium text-violet-400 transition-colors hover:text-violet-300">Register</NuxtLink>
            </p>
          </form>
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

definePageMeta({ layout: false })

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
    await auth.login(email.value, password.value)
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
</script>
