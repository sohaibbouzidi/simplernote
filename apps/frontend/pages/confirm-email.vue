<template>
  <div class="flex min-h-screen flex-col items-center justify-center bg-surface px-6">
    <div v-if="loading" class="text-center">
      <div class="mx-auto mb-6 h-10 w-10 animate-spin rounded-full border-4 border-slate-700 border-t-violet-500"></div>
      <p class="text-sm text-slate-400">Confirming your email...</p>
    </div>
    <template v-else-if="success">
      <div class="w-full max-w-md rounded-2xl border border-slate-800/60 bg-surface-50 p-8 text-center shadow-2xl shadow-black/40">
        <div class="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full bg-green-500/20">
          <svg class="h-7 w-7 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
        </div>
        <h1 class="mb-2 font-display text-2xl font-semibold text-white">Email confirmed</h1>
        <p class="mb-6 text-sm text-slate-400">Your email address has been verified. You can now use all features of Simplernote.</p>
        <NuxtLink to="/login" class="inline-block rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110">Sign in</NuxtLink>
      </div>
    </template>
    <template v-else>
      <div class="w-full max-w-md rounded-2xl border border-slate-800/60 bg-surface-50 p-8 text-center shadow-2xl shadow-black/40">
        <div class="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full bg-red-500/20">
          <svg class="h-7 w-7 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </div>
        <h1 class="mb-2 font-display text-2xl font-semibold text-white">Confirmation failed</h1>
        <p class="mb-2 text-sm text-slate-400">{{ errorMessage }}</p>
        <NuxtLink to="/login" class="mt-6 inline-block text-sm font-medium text-violet-400 transition-colors hover:text-violet-300">Back to sign in</NuxtLink>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute } from "#app"
import { getApiInstance } from "@/services/api"

definePageMeta({ layout: false })

const route = useRoute()
const token = (route.query.token as string) || ""

const loading = ref(true)
const success = ref(false)
const errorMessage = ref("Invalid or expired confirmation link.")

onMounted(async () => {
  if (!token) {
    loading.value = false
    errorMessage.value = "No confirmation token provided."
    return
  }
  try {
    const api = getApiInstance()
    await api.post("/auth/confirm-email", { token })
    success.value = true
  } catch (err: any) {
    const detail = err?.response?.data?.detail
    if (detail) errorMessage.value = detail
  } finally {
    loading.value = false
  }
})
</script>
