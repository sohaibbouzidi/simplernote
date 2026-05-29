<template>
  <div class="max-w-3xl mx-auto">
    <div class="flex items-center gap-4">
      <div v-if="user?.picture_url" class="h-24 w-24 rounded-full overflow-hidden">
        <img :src="user.picture_url" alt="avatar" class="h-full w-full object-cover" />
      </div>
      <div v-else class="h-24 w-24 rounded-full bg-slate-700 flex items-center justify-center text-2xl font-semibold text-white">{{ initials }}</div>
      <div>
        <h1 class="text-2xl font-semibold">{{ fullName }}</h1>
        <p class="text-sm text-slate-400">{{ user?.email }}</p>
      </div>
    </div>

    <div class="mt-6 p-4 border border-slate-800 rounded bg-surface-50">
      <p><strong>Country:</strong> {{ user?.country || '-' }}</p>
      <p><strong>City:</strong> {{ user?.city || '-' }}</p>
    </div>

    <div class="mt-6">
      <NuxtLink to="/complete-profile" class="rounded px-4 py-2 bg-violet-500 text-white">Edit profile</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const user = auth.user

onMounted(() => {
  if (!auth.user) auth.fetchUser()
})

const initials = computed(() => {
  const u = auth.user
  if (!u) return ""
  if (u.first_name || u.last_name) {
    const f = u.first_name ? u.first_name.charAt(0) : ""
    const l = u.last_name ? u.last_name.charAt(0) : ""
    return (f + l).toUpperCase().slice(0, 2)
  }
  return u.email ? u.email.charAt(0).toUpperCase() : ""
})

const fullName = computed(() => {
  const u = auth.user
  if (!u) return ""
  const name = `${u.first_name || ""} ${u.last_name || ""}`.trim()
  return name || u.email || ""
})
</script>
