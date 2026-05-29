<template>
  <Teleport to="body">
    <div class="pointer-events-none fixed inset-0 z-[9999] flex flex-col items-end justify-end gap-3 p-4 sm:p-6">
      <TransitionGroup name="toast" tag="div" class="flex w-full max-w-sm flex-col gap-3">
        <div v-for="t in toasts" :key="t.id" :class="[
          'pointer-events-auto flex items-start gap-3 rounded-lg border px-4 py-3 text-sm shadow-xl backdrop-blur-md',
          typeClasses[t.type],
        ]">
          <span v-html="icons[t.type]" class="mt-0.5 h-4 w-4 shrink-0" />
          <p class="flex-1 text-sm font-medium">{{ t.message }}</p>
          <button @click="remove(t.id)" class="shrink-0 opacity-50 hover:opacity-100 transition-opacity">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToast } from "@/composables/useToast"

const { toasts, remove } = useToast()

const icons: Record<string, string> = {
  success: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4 text-green-400"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
  error: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4 text-red-400"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
  info: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4 text-brand-400"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
  warning: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4 text-amber-400"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>',
}

const typeClasses: Record<string, string> = {
  success: "border-green-500/30 bg-green-500/10 text-green-200",
  error: "border-red-500/30 bg-red-500/10 text-red-200",
  info: "border-brand-500/30 bg-brand-500/10 text-brand-200",
  warning: "border-amber-500/30 bg-amber-500/10 text-amber-200",
}
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.3s ease-out;
}
.toast-leave-active {
  transition: all 0.25s ease-in;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(1rem) scale(0.96);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.96);
}
</style>
