<template>
  <div>
    <section class="relative flex min-h-screen items-center justify-center overflow-hidden px-6 pt-24">
      <div class="pointer-events-none absolute inset-0 bg-grid opacity-40" />
      <div class="pointer-events-none absolute left-1/2 top-1/3 -translate-x-1/2 -translate-y-1/2">
        <div class="h-[600px] w-[600px] animate-pulse-glow rounded-full bg-gradient-to-br from-violet-500/20 via-fuchsia-500/10 to-transparent blur-3xl" />
      </div>
      <div class="pointer-events-none absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-surface to-transparent" />
      <div class="relative z-10 mx-auto max-w-4xl text-center">
        <div class="mb-8 animate-fade-in-up opacity-0" style="animation-delay: 0.1s">
          <span class="inline-block rounded-full border border-violet-500/20 bg-violet-500/10 px-4 py-1.5 text-xs font-semibold tracking-widest text-violet-300 uppercase">AI-Native Memory Platform</span>
        </div>
        <h1 class="animate-fade-in-up font-display text-balance text-5xl font-semibold leading-tight tracking-tight text-white opacity-0 sm:text-6xl md:text-7xl lg:text-8xl" style="animation-delay: 0.2s">
          Your notes, your tasks,
          <br />
          <span class="bg-gradient-to-r from-violet-400 via-fuchsia-400 to-amber-400 bg-clip-text text-transparent">your AI. Unified.</span>
        </h1>
        <p class="animate-fade-in-up mx-auto mt-6 max-w-2xl text-balance text-lg leading-relaxed text-slate-400 opacity-0 sm:text-xl" style="animation-delay: 0.3s">
          Simplernote brings together note-taking, task management, and AI agent memory into one seamless platform. Built for teams and AI agents alike.
        </p>
        <div class="animate-fade-in-up mt-10 flex flex-wrap items-center justify-center gap-4 opacity-0" style="animation-delay: 0.4s">
          <button
            @click="handleGetStarted"
            class="group inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-8 py-4 text-base font-semibold text-white shadow-2xl shadow-violet-500/25 transition-all hover:shadow-3xl hover:shadow-violet-500/40 hover:brightness-110"
          >
            Get started
            <svg class="h-4 w-4 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
          </button>
          <a
            href="#features"
            class="inline-flex items-center gap-2 rounded-xl border border-slate-700/50 px-8 py-4 text-base font-medium text-slate-300 transition-all hover:border-slate-600 hover:text-white"
          >
            See how it works
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" /></svg>
          </a>
        </div>
      </div>
    </section>

    <section id="features" class="relative px-6 py-32">
      <div class="mx-auto max-w-6xl">
        <div class="mb-4 text-center">
          <span class="inline-block rounded-full border border-violet-500/20 bg-violet-500/10 px-4 py-1.5 text-xs font-semibold tracking-widest text-violet-300 uppercase">Why Simplernote</span>
        </div>
        <h2 class="text-balance text-center font-display text-4xl font-semibold leading-tight text-white sm:text-5xl">Built for what comes next</h2>
        <p class="mx-auto mt-4 max-w-xl text-center text-slate-400">Everything you need to manage knowledge and workflows, with AI-native integrations from day one.</p>
        <div class="mt-16 grid gap-6 md:grid-cols-3">
          <div
            v-for="(f, i) in features"
            :key="f.title"
            class="group animate-fade-in-up rounded-2xl border border-slate-800/50 bg-surface-50/50 p-8 opacity-0 transition-all hover:border-violet-500/20 hover:bg-surface-50 hover:shadow-2xl hover:shadow-violet-500/5"
            :style="{ animationDelay: `${0.5 + i * 0.15}s` }"
          >
            <div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 text-xl">
              {{ f.icon }}
            </div>
            <h3 class="mb-3 font-display text-xl font-semibold text-white">{{ f.title }}</h3>
            <p class="text-sm leading-relaxed text-slate-400">{{ f.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="relative px-6 py-32">
      <div class="pointer-events-none absolute inset-0 bg-grid opacity-20" />
      <div class="relative mx-auto max-w-6xl">
        <div class="mb-4 text-center">
          <span class="inline-block rounded-full border border-violet-500/20 bg-violet-500/10 px-4 py-1.5 text-xs font-semibold tracking-widest text-violet-300 uppercase">How It Works</span>
        </div>
        <h2 class="text-balance text-center font-display text-4xl font-semibold leading-tight text-white sm:text-5xl">Three steps to clarity</h2>
        <p class="mx-auto mt-4 max-w-xl text-center text-slate-400">From idea to execution in minutes, not days.</p>
        <div class="mt-20 grid gap-12 md:grid-cols-3">
          <div
            v-for="(step, i) in steps"
            :key="step.title"
            class="animate-fade-in-up relative text-center opacity-0"
            :style="{ animationDelay: `${0.5 + i * 0.2}s` }"
          >
            <div class="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 text-2xl font-bold text-violet-300 shadow-lg shadow-violet-500/10">
              {{ step.num }}
            </div>
            <h3 class="mb-3 font-display text-xl font-semibold text-white">{{ step.title }}</h3>
            <p class="mx-auto max-w-xs text-sm leading-relaxed text-slate-400">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="relative px-6 py-32">
      <div class="mx-auto max-w-4xl text-center">
        <div class="relative rounded-3xl border border-slate-800/60 bg-gradient-to-b from-surface-50 to-surface px-12 py-20 shadow-2xl shadow-black/30">
          <div class="pointer-events-none absolute inset-0 overflow-hidden rounded-3xl">
            <div class="absolute -left-20 -top-20 h-80 w-80 animate-float rounded-full bg-violet-500/10 blur-3xl" />
            <div class="absolute -bottom-20 -right-20 h-80 w-80 animate-float rounded-full bg-fuchsia-500/10 blur-3xl" style="animation-delay: -3s" />
          </div>
          <div class="relative z-10">
            <h2 class="text-balance font-display text-4xl font-semibold leading-tight text-white sm:text-5xl">Ready to simplify your workflow?</h2>
            <p class="mx-auto mt-4 max-w-lg text-balance text-slate-400">Join the platform where your notes, tasks, and AI work together seamlessly.</p>
            <button
              @click="handleGetStarted"
              class="mt-10 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-8 py-4 text-base font-semibold text-white shadow-2xl shadow-violet-500/25 transition-all hover:shadow-3xl hover:shadow-violet-500/40 hover:brightness-110"
            >
              Open Simplernote
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <footer class="border-t border-slate-800/50 px-6 py-10">
      <div class="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 sm:flex-row">
        <div class="flex items-center gap-2.5 text-sm text-slate-500">
          <span class="flex h-6 w-6 items-center justify-center rounded-md bg-gradient-to-br from-violet-400 to-fuchsia-400 text-[8px] font-bold text-white">S</span>
          Simplernote
        </div>
        <p class="text-sm text-slate-600">&copy; {{ new Date().getFullYear() }} Simplernote. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "#app"
import { useAuthStore } from "@/stores/auth"

definePageMeta({ layout: "landing" })

const auth = useAuthStore()
const router = useRouter()

const features = [
  {
    icon: "\u270D\uFE0F",
    title: "Smart Notes",
    description: "Write and organize with rich text, tags, projects, and full-text search. Your knowledge base, always accessible.",
  },
  {
    icon: "\uD83D\uDCCB",
    title: "Task Kanban",
    description: "Visual workflow management with drag-and-drop boards, priority badges, and real-time status tracking across lanes.",
  },
  {
    icon: "\uD83E\uDD16",
    title: "AI Memory",
    description: "Built-in API for AI agents to read, write, and search context. Your platform speaks the language of LLMs natively.",
  },
]

const steps = [
  { num: "01", title: "Create", description: "Start writing notes or tasks instantly. Everything syncs in real time across your workspace." },
  { num: "02", title: "Organize", description: "Tag, categorize, and filter. Build a structured knowledge graph that grows with your work." },
  { num: "03", title: "Automate", description: "Connect AI agents via our API. Automate workflows, extract insights, and never lose context." },
]

function handleGetStarted() {
  if (auth.isAuthenticated) {
    router.push("/dashboard")
  } else {
    router.push("/login?redirect=/dashboard")
  }
}
</script>