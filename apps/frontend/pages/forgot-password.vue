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
          <template v-if="sent">
            <div class="text-center">
              <div class="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full bg-violet-500/20">
                <svg class="h-7 w-7 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
              </div>
              <h1 class="mb-2 font-display text-2xl font-semibold text-white">Check your email</h1>
              <p class="mb-2 text-sm text-slate-400">If an account with that email exists, we've sent a password reset link.</p>
              <p class="text-sm text-slate-500">It may take a few minutes to arrive. Don't forget to check your spam folder.</p>
              <NuxtLink to="/login" class="mt-8 inline-block text-sm font-medium text-violet-400 transition-colors hover:text-violet-300">Back to sign in</NuxtLink>
            </div>
          </template>
          <template v-else>
            <h1 class="mb-1 font-display text-2xl font-semibold text-white">Forgot password</h1>
            <p class="mb-8 text-sm text-slate-400">Enter your email and we'll send you a reset link.</p>
            <form @submit.prevent="submit" class="space-y-5">
              <div>
                <label class="mb-2 block text-sm font-medium text-slate-300">Email</label>
                <input v-model="email" @input="clearError" type="email" autocomplete="email" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', error ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="you@example.com" />
                <p v-if="error" class="mt-1.5 text-xs text-red-400">{{ error }}</p>
              </div>
              <p v-if="formError" class="rounded-lg bg-red-500/10 px-4 py-3 text-sm text-red-400">{{ formError }}</p>
              <button type="submit" :disabled="submitting" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed">
                {{ submitting ? 'Sending...' : 'Send reset link' }}
              </button>
              <p class="text-center text-sm text-slate-500">
                Remember your password?
                <NuxtLink to="/login" class="font-medium text-violet-400 transition-colors hover:text-violet-300">Sign in</NuxtLink>
              </p>
            </form>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { getApiInstance } from "@/services/api"

definePageMeta({ layout: false })

const email = ref("")
const submitting = ref(false)
const error = ref("")
const formError = ref("")
const sent = ref(false)

function clearError() {
  error.value = ""
  formError.value = ""
}

const submit = async () => {
  error.value = ""
  formError.value = ""

  if (!email.value.trim()) {
    error.value = "Email is required"
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    error.value = "Enter a valid email address"
    return
  }

  submitting.value = true
  try {
    const api = getApiInstance()
    await api.post("/auth/forgot-password", { email: email.value })
    sent.value = true
  } catch (err: any) {
    const status = err?.response?.status
    if (status === 429) {
      formError.value = "Too many attempts. Please wait a moment and try again."
    } else {
      formError.value = "Something went wrong. Please try again later."
    }
  } finally {
    submitting.value = false
  }
}
</script>
