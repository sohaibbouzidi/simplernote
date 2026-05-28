<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-3xl font-semibold text-white">Activity Logs</h1>
      <p class="text-slate-400">Track note changes, task updates, and API usage.</p>
    </div>
    <div class="space-y-4">
      <div v-for="entry in logs" :key="entry.id" class="rounded-3xl border border-slate-800 bg-slate-950 p-5">
        <div class="flex items-center justify-between gap-4">
          <p class="font-semibold text-white">{{ entry.action }}</p>
          <span class="text-sm text-slate-400">{{ entry.created_at }}</span>
        </div>
        <p class="mt-2 text-slate-400">Entity: {{ entry.entity_type }} / {{ entry.entity_id || 'N/A' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const logs = ref([])

onMounted(async () => {
  try {
    const api = getApiInstance()
    const response = await api.get("/activity-logs")
    logs.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>
