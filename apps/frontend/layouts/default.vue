<template>
  <div class="min-h-screen bg-surface text-white">
    <header class="border-b border-slate-800 bg-surface-50 px-4">
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <NuxtLink to="/dashboard" class="flex items-center gap-2">
            <span class="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-violet-500 to-fuchsia-500 text-xs font-bold text-white">S</span>
            <span class="hidden text-base font-semibold tracking-tight text-white sm:inline">Simplernote</span>
          </NuxtLink>
          <div class="relative hidden md:block">
            <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input v-model="searchQuery" @keydown.enter="handleSearch" placeholder="Search projects..." class="w-64 rounded-lg border border-slate-800 bg-surface py-1.5 pl-10 pr-3 text-sm text-white placeholder-slate-400 focus:border-brand-500 focus:outline-none" />
          </div>
        </div>

        <nav class="flex items-center gap-1 text-sm">
              <NuxtLink v-for="link in navLinks" :key="link.to" :to="link.to" class="rounded-md px-3 py-2 text-slate-400 transition-all hover:bg-slate-800 hover:text-white" active-class="!text-white !bg-slate-800">{{ link.label }}</NuxtLink>
              <div class="mx-2 h-5 w-px bg-slate-800" />
              <div ref="menuRef" class="relative">
                <button @click.stop="toggleMenu" :aria-expanded="menuOpen" class="flex items-center gap-1.5 rounded-md px-3 py-2 text-sm">
                  <div v-if="auth.user?.picture_url" class="h-8 w-8 rounded-full overflow-hidden">
                    <img :src="auth.user.picture_url" alt="avatar" class="h-full w-full object-cover" />
                  </div>
                  <div v-else class="h-8 w-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-semibold text-white">{{ initials }}</div>
                </button>
                <transition name="fade">
                  <div v-if="menuOpen" class="absolute right-0 mt-2 w-40 rounded-md bg-surface-50 border border-slate-800 shadow-lg z-50">
                    <NuxtLink to="/profile" class="block px-4 py-2 text-sm text-slate-200 hover:bg-slate-800">Profile</NuxtLink>
                    <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-slate-800">Sign out</button>
                  </div>
                </transition>
              </div>
            </nav>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6">
      <slot />
    </main>
    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from "vue"
import { useRouter } from "#app"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const router = useRouter()
const searchQuery = ref("")

const menuOpen = ref(false)
const menuRef = ref<HTMLElement | null>(null)

const handleClickOutside = (e: MouseEvent) => {
  if (!menuRef.value) return
  if (!(menuRef.value as HTMLElement).contains(e.target as Node)) {
    menuOpen.value = false
  }
}

onMounted(() => document.addEventListener("click", handleClickOutside))
onBeforeUnmount(() => document.removeEventListener("click", handleClickOutside))

const navLinks = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Projects", to: "/projects" },
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
  menuOpen.value = false
  auth.clear()
  router.push("/")
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

const initials = computed(() => {
  const user = auth.user
  if (!user) return ""
  if (user.first_name || user.last_name) {
    const f = user.first_name ? user.first_name.charAt(0) : ""
    const l = user.last_name ? user.last_name.charAt(0) : ""
    return (f + l).toUpperCase().slice(0, 2)
  }
  return user.email ? user.email.charAt(0).toUpperCase() : ""
})
</script>
