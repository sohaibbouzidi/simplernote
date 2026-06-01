<template>
  <div class="min-h-screen bg-surface text-slate-100">
    <header class="fixed inset-x-0 top-0 z-50">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <NuxtLink to="/" class="flex items-center gap-2.5">
          <LogoIcon :size="32" />
          <span class="font-display text-lg font-semibold tracking-tight text-white">Simplernote</span>
        </NuxtLink>
        <div class="flex items-center gap-4">
          <NuxtLink
            v-if="!auth.isAuthenticated"
            to="/login"
            class="rounded-xl border border-slate-700/50 px-5 py-2.5 text-sm font-medium text-slate-300 transition-all hover:border-slate-600 hover:text-white"
          >
            Sign in
          </NuxtLink>
          <button
            @click="handleOpenApp"
            class="rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-medium text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110"
          >
            {{ auth.isAuthenticated ? "Dashboard" : "Get started" }}
          </button>
        </div>
      </div>
    </header>
    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "#app"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const router = useRouter()

function handleOpenApp() {
  if (auth.isAuthenticated) {
    router.push("/dashboard")
  } else {
    router.push("/login?redirect=/dashboard")
  }
}
</script>