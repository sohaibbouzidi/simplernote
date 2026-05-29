<template>
  <div class="min-h-screen bg-[#0d1117] text-[#e6edf3]">
    <header class="border-b border-[#21262d] bg-[#161b22] px-4">
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <NuxtLink to="/dashboard" class="flex items-center gap-2">
            <span class="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-[#2ea043] to-[#56d364] text-xs font-bold text-white">S</span>
            <span class="hidden text-base font-semibold tracking-tight text-[#e6edf3] sm:inline">Simplernote</span>
          </NuxtLink>
          <div class="relative hidden md:block">
            <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#8b949e]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input v-model="searchQuery" @keydown.enter="handleSearch" placeholder="Search projects..." class="w-64 rounded-lg border border-[#21262d] bg-[#0d1117] py-1.5 pl-10 pr-3 text-sm text-[#e6edf3] placeholder-[#8b949e] focus:border-[#2ea043] focus:outline-none" />
          </div>
        </div>

        <nav class="flex items-center gap-1 text-sm">
          <NuxtLink v-for="link in navLinks" :key="link.to" :to="link.to" class="rounded-md px-3 py-2 text-[#8b949e] transition-all hover:bg-[#21262d] hover:text-[#e6edf3]" active-class="!text-[#e6edf3] !bg-[#21262d]">{{ link.label }}</NuxtLink>
          <div class="mx-2 h-5 w-px bg-[#21262d]" />
          <div class="relative" @click.outside="showMenu = false">
            <button @click="showMenu = !showMenu" class="flex h-8 w-8 items-center justify-center rounded-full bg-[#21262d] text-sm font-semibold text-[#e6edf3] hover:bg-[#30363d]">
              {{ auth.user?.email?.charAt(0).toUpperCase() || 'U' }}
            </button>
            <div v-if="showMenu" class="absolute right-0 top-10 z-50 w-56 rounded-lg border border-[#21262d] bg-[#161b22] py-1 shadow-xl">
              <div class="border-b border-[#21262d] px-4 py-2 text-sm text-[#8b949e]">
                <p class="truncate font-medium text-[#e6edf3]">{{ auth.user?.email }}</p>
                <p class="text-xs" v-if="auth.user?.role">Role: {{ auth.user?.role }}</p>
              </div>
              <button @click="handleLogout" class="flex w-full items-center gap-2 px-4 py-2 text-sm text-[#f85149] hover:bg-[#21262d]">
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                Sign out
              </button>
            </div>
          </div>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "#app"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const router = useRouter()
const showMenu = ref(false)
const searchQuery = ref("")

const navLinks = [
  { label: "Projects", to: "/projects" },
  { label: "Notes", to: "/notes" },
  { label: "Tasks", to: "/tasks" },
  { label: "Activity", to: "/activity-logs" },
]

if (auth.isAdmin) {
  navLinks.push({ label: "Admin", to: "/admin" })
}

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push(`/projects?q=${encodeURIComponent(searchQuery.value.trim())}`)
    searchQuery.value = ""
  }
}

function handleLogout() {
  auth.clear()
  router.push("/")
}
</script>
