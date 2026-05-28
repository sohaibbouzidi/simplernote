<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">Notes</h1>
        <p class="text-slate-400">Search, filter, and edit your structured notes.</p>
      </div>
      <button class="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-400">New note</button>
    </div>
    <div class="grid gap-6 lg:grid-cols-3">
      <div class="space-y-4" v-for="note in notes" :key="note.id">
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <div class="flex items-center justify-between gap-3">
            <h2 class="text-lg font-semibold text-white">{{ note.title }}</h2>
            <span class="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">{{ note.note_type }}</span>
          </div>
          <p class="mt-3 text-slate-400 line-clamp-3">{{ note.summary || note.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getApiInstance } from "@/services/api"

const notes = ref([])

onMounted(async () => {
  try {
    const api = getApiInstance()
    const response = await api.get("/notes")
    notes.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>
