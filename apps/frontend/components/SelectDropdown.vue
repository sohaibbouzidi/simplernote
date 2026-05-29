<template>
  <div ref="containerRef" class="relative">
    <button
      type="button"
      @click="open = !open"
      :disabled="disabled"
      class="flex w-full items-center justify-between gap-2 rounded-md border border-slate-700 bg-surface px-3 py-2 text-sm outline-none transition-colors disabled:cursor-not-allowed disabled:opacity-40"
      :class="open ? 'border-brand-500' : 'hover:border-slate-600'"
    >
      <span :class="selectedLabel ? 'text-white' : 'text-slate-500'">
        {{ selectedLabel || placeholder }}
      </span>
      <svg class="h-4 w-4 text-slate-400 transition-transform" :class="open && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
    </button>
    <div
      v-if="open"
      class="absolute left-0 top-full z-50 mt-1 w-full rounded-lg border border-slate-700 bg-surface-50 py-1 shadow-xl"
    >
      <button
        v-for="opt in options"
        :key="opt.value"
        type="button"
        @click="select(opt.value)"
        class="flex w-full items-center gap-2 px-3 py-2 text-left text-sm transition-colors hover:bg-slate-800"
        :class="modelValue === opt.value ? 'text-white' : 'text-slate-400'"
      >
        <span class="flex-1">{{ opt.label }}</span>
        <svg v-if="modelValue === opt.value" class="h-4 w-4 shrink-0 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
      </button>
      <div v-if="options.length === 0" class="px-3 py-4 text-center text-sm text-slate-600">
        No options
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue"

const props = defineProps<{
  modelValue: string
  options: { value: string; label: string }[]
  placeholder?: string
  disabled?: boolean
}>()

const emit = defineEmits<{ (e: "update:modelValue", v: string): void }>()

const open = ref(false)
const containerRef = ref<HTMLElement | null>(null)

const selectedLabel = computed(() => {
  const opt = props.options.find(o => o.value === props.modelValue)
  return opt ? opt.label : ""
})

function select(value: string) {
  emit("update:modelValue", value)
  open.value = false
}

function onClickOutside(e: MouseEvent) {
  if (containerRef.value && !containerRef.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener("click", onClickOutside))
onUnmounted(() => document.removeEventListener("click", onClickOutside))
</script>
