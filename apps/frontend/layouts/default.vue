<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-sm">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <div>
          <NuxtLink to="/" class="text-lg font-semibold text-white">Simplernote</NuxtLink>
        </div>
        <nav class="flex items-center gap-4 text-sm text-slate-300">
          <NuxtLink to="/dashboard" class="hover:text-white">Dashboard</NuxtLink>
          <NuxtLink to="/projects" class="hover:text-white">Projects</NuxtLink>
          <NuxtLink to="/notes" class="hover:text-white">Notes</NuxtLink>
          <NuxtLink to="/tasks" class="hover:text-white">Tasks</NuxtLink>
          <NuxtLink to="/api-keys" class="hover:text-white">API Keys</NuxtLink>
          <NuxtLink to="/activity-logs" class="hover:text-white">Activity</NuxtLink>
        </nav>
      </div>
    </header>
    <main class="mx-auto max-w-7xl px-6 py-8">
      <slot />
    </main>
  </div>
</template>
