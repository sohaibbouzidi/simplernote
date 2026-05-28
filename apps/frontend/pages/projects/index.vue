<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">Projects</h1>
        <p class="text-slate-400">Create and manage your AI memory workspaces.</p>
      </div>
      <button class="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-400">New project</button>
    </div>
    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6" v-for="project in projects" :key="project.id">
        <h2 class="text-xl font-semibold text-white">{{ project.name }}</h2>
        <p class="mt-2 text-slate-400">{{ project.description || 'No description provided.' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const projects = ref([])

onMounted(async () => {
  try {
    const api = getApiInstance()
    const response = await api.get("/projects")
    projects.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>
