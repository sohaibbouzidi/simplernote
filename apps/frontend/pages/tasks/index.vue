<template>
  <div class="space-y-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold text-white">Tasks</h1>
        <p class="text-slate-400">Organize work with status lanes and subtasks.</p>
      </div>
      <button class="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-400">Add task</button>
    </div>
    <div class="grid gap-4 lg:grid-cols-4">
      <div v-for="lane in lanes" :key="lane.name" class="rounded-3xl border border-slate-800 bg-slate-950 p-5">
        <h2 class="mb-4 text-lg font-semibold text-white">{{ lane.label }}</h2>
        <div class="space-y-4">
          <div v-for="task in lane.tasks" :key="task.id" class="rounded-2xl border border-slate-800 bg-slate-900 p-4 text-slate-200">
            <p class="font-semibold">{{ task.title }}</p>
            <p class="mt-2 text-sm text-slate-400">{{ task.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const lanes = [
  { name: "todo", label: "Todo", tasks: [{ id: "1", title: "Define schema", description: "Write note and task models." }] },
  { name: "research", label: "Research", tasks: [{ id: "2", title: "AI integration", description: "Plan API key and agent workflows." }] },
  { name: "coding", label: "Coding", tasks: [{ id: "3", title: "Build backend", description: "Implement FastAPI services." }] },
  { name: "review", label: "Review", tasks: [] },
]
</script>
