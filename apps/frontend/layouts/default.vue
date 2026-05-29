<template>
  <div class="min-h-screen bg-surface text-slate-100">
    <header class="border-b border-slate-800/50 bg-surface-50/80 backdrop-blur-md">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-3.5">
        <NuxtLink to="/dashboard" class="flex items-center gap-2.5">
          <span class="flex h-7 w-7 items-center justify-center rounded-md bg-gradient-to-br from-violet-400 to-fuchsia-400 text-[9px] font-bold leading-none text-white">S</span>
          <span class="font-display text-base font-semibold tracking-tight text-white">Simplernote</span>
        </NuxtLink>
        <nav class="flex items-center gap-1 text-sm">
          <NuxtLink v-for="link in navLinks" :key="link.to" :to="link.to" class="rounded-lg px-3.5 py-2 text-slate-400 transition-all hover:bg-slate-800/40 hover:text-white" active-class="bg-slate-800/60 text-white">{{ link.label }}</NuxtLink>
          <div class="ml-2 h-5 w-px bg-slate-700/50" />
          <button @click="handleLogout" class="rounded-lg px-3.5 py-2 text-sm text-slate-500 transition-all hover:bg-slate-800/40 hover:text-red-400">
            Logout
          </button>
        </nav>
      </div>
    </header>
    <main class="mx-auto max-w-7xl px-6 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "#app"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const router = useRouter()

const navLinks = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Notes", to: "/notes" },
  { label: "Tasks", to: "/tasks" },
  { label: "Projects", to: "/projects" },
  { label: "API Keys", to: "/api-keys" },
  { label: "Activity", to: "/activity-logs" },
]

if (auth.isAdmin) {
  navLinks.push({ label: "Admin", to: "/admin" })
}

function handleLogout() {
  auth.clear()
  router.push("/")
}
</script>
