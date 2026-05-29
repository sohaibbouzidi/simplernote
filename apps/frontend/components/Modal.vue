<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="close">
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="close" />
    <div class="relative w-full max-w-lg rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-white">{{ title }}</h2>
        <button @click="close" class="rounded-xl p-2 text-slate-400 hover:bg-slate-800 hover:text-white">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ modelValue: boolean; title: string }>()
const emit = defineEmits<{ (e: "update:modelValue", v: boolean): void }>()
function close() { emit("update:modelValue", false) }
</script>
