import { ref } from "vue"

export type ToastType = "success" | "error" | "info" | "warning"

export interface Toast {
  id: number
  message: string
  type: ToastType
}

const toasts = ref<Toast[]>([])
let nextId = 0

function add(message: string, type: ToastType) {
  const id = nextId++
  toasts.value.push({ id, message, type })
  setTimeout(() => remove(id), 4000)
}

function remove(id: number) {
  const idx = toasts.value.findIndex(t => t.id === id)
  if (idx !== -1) toasts.value.splice(idx, 1)
}

export function useToast() {
  return {
    toasts,
    success: (msg: string) => add(msg, "success"),
    error: (msg: string) => add(msg, "error"),
    info: (msg: string) => add(msg, "info"),
    warning: (msg: string) => add(msg, "warning"),
    remove,
  }
}
