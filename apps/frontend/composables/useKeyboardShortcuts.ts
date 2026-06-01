import { ref } from "vue"

export interface ShortcutDef {
  keys: string
  handler: () => void
  description: string
  context?: string
}

const registeredShortcuts = ref<Map<string, ShortcutDef>>(new Map())
let keySequence: string[] = []
let sequenceTimer: ReturnType<typeof setTimeout> | null = null
let listenerActive = false

function normalize(key: string): string {
  const map: Record<string, string> = {
    "/": "slash",
    "?": "question",
    escape: "esc",
  }
  return map[key.toLowerCase()] || key.toLowerCase()
}

function handleKeyDown(e: KeyboardEvent) {
  const target = e.target as HTMLElement
  const tag = target.tagName
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || target.isContentEditable) {
    if (e.key === "Escape") {
      ;(target as HTMLInputElement).blur()
      return
    }
    if (e.key !== "?" && e.key !== "/") return
  }

  const key = normalize(e.key)
  const joined = [...keySequence, key].join(" ")

  let matched: ShortcutDef | undefined
  for (const s of registeredShortcuts.value.values()) {
    if (s.keys === joined) {
      matched = s
      break
    }
    if (s.keys === key) {
      matched = s
    }
  }

  if (matched) {
    e.preventDefault()
    e.stopPropagation()
    keySequence = []
    if (sequenceTimer) clearTimeout(sequenceTimer)
    matched.handler()
    return
  }

  const partialMatch = [...registeredShortcuts.value.values()].some(
    (s) => s.keys.startsWith(joined + " ") && s.keys !== joined
  )
  if (partialMatch) {
    keySequence.push(key)
    if (sequenceTimer) clearTimeout(sequenceTimer)
    sequenceTimer = setTimeout(() => {
      keySequence = []
    }, 1000)
    e.preventDefault()
    return
  }

  keySequence = []
  if (sequenceTimer) clearTimeout(sequenceTimer)
}

let activeShortcuts: ShortcutDef[] = []

export function useKeyboardShortcuts() {
  function register(defs: ShortcutDef[]) {
    for (const d of defs) {
      registeredShortcuts.value.set(d.keys, d)
    }
    activeShortcuts.push(...defs)
  }

  function unregister(defs: ShortcutDef[]) {
    for (const d of defs) {
      registeredShortcuts.value.delete(d.keys)
    }
    activeShortcuts = activeShortcuts.filter((s) => !defs.includes(s))
  }

  function unregisterAll() {
    for (const d of activeShortcuts) {
      registeredShortcuts.value.delete(d.keys)
    }
    activeShortcuts = []
  }

  return { register, unregister, unregisterAll }
}

export function initGlobalListener() {
  if (listenerActive) return
  listenerActive = true
  if (typeof window !== "undefined") {
    window.addEventListener("keydown", handleKeyDown)
  }
}

export function destroyGlobalListener() {
  if (!listenerActive) return
  listenerActive = false
  if (typeof window !== "undefined") {
    window.removeEventListener("keydown", handleKeyDown)
  }
}

export function getAllShortcuts(): ShortcutDef[] {
  return [...registeredShortcuts.value.values()]
}
