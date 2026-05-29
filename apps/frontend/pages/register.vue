<template>
  <div class="flex min-h-screen items-center justify-center bg-surface px-4">
    <div class="w-full max-w-md animate-fade-in-up">
      <div class="mb-8 text-center">
        <NuxtLink to="/" class="mb-6 inline-flex items-center gap-2.5">
          <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-fuchsia-400 text-sm font-bold leading-none text-white shadow-lg shadow-violet-500/20">S</span>
          <span class="font-display text-xl font-semibold tracking-tight text-white">Simplernote</span>
        </NuxtLink>
      </div>
      <div class="rounded-2xl border border-slate-800/60 bg-surface-50 p-8 shadow-2xl shadow-black/40">
        <h1 class="mb-1 font-display text-2xl font-semibold text-white">Create account</h1>
        <p class="mb-8 text-sm text-slate-400">Start your journey with Simplernote.</p>
        <form @submit.prevent="submit" class="space-y-5">
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Email</label>
            <input v-model="email" type="email" autocomplete="email" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" placeholder="you@example.com" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Password</label>
            <input v-model="password" type="password" autocomplete="new-password" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" placeholder="Create a password" />
          </div>
          <button type="submit" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110">
            Create account
          </button>
          <p class="text-center text-sm text-slate-500">
            Already have an account?
            <NuxtLink :to="'/login' + (redirect ? '?redirect=' + encodeURIComponent(redirect) : '')" class="font-medium text-violet-400 transition-colors hover:text-violet-300">Sign in</NuxtLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter, useRoute } from "#app"
import { useAuthStore } from "@/stores/auth"

definePageMeta({ layout: false })

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref("")
const password = ref("")
const redirect = (route.query.redirect as string) || ""

const submit = async () => {
  try {
    await auth.register(email.value, password.value)
    await router.push("/login" + (redirect ? "?redirect=" + encodeURIComponent(redirect) : ""))
  } catch (error) {
    console.error(error)
    alert("Registration failed. Please try again.")
  }
}
</script>
