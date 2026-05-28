<template>
  <div class="space-y-8">
    <section class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
      <div class="flex items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-semibold text-white">Dashboard</h1>
          <p class="text-slate-400">Overview of your recent activity, notes, and task status.</p>
        </div>
      </div>
      <div class="mt-8 grid gap-6 sm:grid-cols-3">
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <p class="text-sm uppercase text-slate-500">Notes</p>
          <p class="mt-4 text-4xl font-semibold text-white">12</p>
        </div>
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <p class="text-sm uppercase text-slate-500">Tasks</p>
          <p class="mt-4 text-4xl font-semibold text-white">23</p>
        </div>
        <div class="rounded-3xl border border-slate-800 bg-slate-950 p-6">
          <p class="text-sm uppercase text-slate-500">Activity</p>
          <p class="mt-4 text-4xl font-semibold text-white">9</p>
        </div>
      </div>
    </section>

    <section class="grid gap-6 xl:grid-cols-2">
      <div class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
        <h2 class="text-2xl font-semibold text-white">Recent Notes</h2>
        <p class="mt-2 text-slate-400">A quick look at the latest note updates in your projects.</p>
        <div class="mt-6 space-y-4">
          <div class="rounded-3xl border border-slate-800 bg-slate-950 p-4">
            <p class="font-semibold text-white">Architecture memory</p>
            <p class="mt-1 text-slate-400">Decision research summary and next steps.</p>
          </div>
          <div class="rounded-3xl border border-slate-800 bg-slate-950 p-4">
            <p class="font-semibold text-white">Task roadmap</p>
            <p class="mt-1 text-slate-400">Kanban workflow improvements for your agents.</p>
          </div>
        </div>
      </div>
      <div class="rounded-3xl border border-slate-800 bg-slate-900/80 p-8">
        <h2 class="text-2xl font-semibold text-white">Recent Activity</h2>
        <p class="mt-2 text-slate-400">User and AI agent lifecycle events.</p>
        <ul class="mt-6 space-y-3">
          <li class="rounded-3xl border border-slate-800 bg-slate-950 p-4 text-slate-300">Task "Design API" moved to Research</li>
          <li class="rounded-3xl border border-slate-800 bg-slate-950 p-4 text-slate-300">Note "Research memory" created</li>
        </ul>
      </div>
    </section>
  </div>
</template>
