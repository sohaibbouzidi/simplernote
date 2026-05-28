<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">API Keys</h1>
        <p class="text-slate-400">Create and manage keys for external agents.</p>
      </div>
      <button class="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-400">Create key</button>
    </div>
    <div class="space-y-4">
      <div v-for="key in keys" :key="key.id" class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
        <div class="flex items-center justify-between gap-4">
          <div>
            <h2 class="text-lg font-semibold text-white">{{ key.name }}</h2>
            <p class="text-slate-400">Permissions: {{ Object.keys(key.permissions).join(", ") }}</p>
          </div>
          <span class="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">{{ key.created_at }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const keys = ref([])

onMounted(async () => {
  try {
    const api = getApiInstance()
    const response = await api.get("/api-keys")
    keys.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>
