<template>
  <div class="flex min-h-screen bg-surface">
    <div class="hidden w-1/2 flex-col items-center justify-center bg-gradient-to-br from-surface-50 via-surface to-surface p-12 lg:flex">
      <div class="max-w-md animate-fade-in-up">
        <NuxtLink to="/" class="mb-8 inline-flex items-center gap-3">
          <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-fuchsia-400 text-lg font-bold leading-none text-white shadow-lg shadow-violet-500/20">S</span>
          <span class="font-display text-2xl font-semibold tracking-tight text-white">Simplernote</span>
        </NuxtLink>
        <h2 class="mt-12 font-display text-3xl font-semibold leading-tight text-white">Your AI-ready<br />note &amp; task hub</h2>
        <p class="mt-4 text-base leading-relaxed text-slate-400">Organize projects, manage tasks, and give your AI agents persistent memory — all in one place.</p>
        <div class="mt-10 space-y-5">
          <div class="flex items-start gap-3 text-sm text-slate-400">
            <span class="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500/20 text-xs text-violet-400">✓</span>
            <span>Structured notes with types, tags, and metadata</span>
          </div>
          <div class="flex items-start gap-3 text-sm text-slate-400">
            <span class="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500/20 text-xs text-violet-400">✓</span>
            <span>Kanban-style task management with 8 status lanes</span>
          </div>
          <div class="flex items-start gap-3 text-sm text-slate-400">
            <span class="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500/20 text-xs text-violet-400">✓</span>
            <span>Project-scoped API keys for AI agent integration</span>
          </div>
        </div>
      </div>
    </div>
    <div class="flex w-full items-center justify-center px-6 lg:w-1/2">
      <div class="w-full max-w-md animate-fade-in-up">
        <div class="mb-8 text-center lg:hidden">
          <NuxtLink to="/" class="inline-flex items-center gap-2.5">
            <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-fuchsia-400 text-sm font-bold leading-none text-white shadow-lg shadow-violet-500/20">S</span>
            <span class="font-display text-xl font-semibold tracking-tight text-white">Simplernote</span>
          </NuxtLink>
        </div>
        <div class="rounded-2xl border border-slate-800/60 bg-surface-50 p-8 shadow-2xl shadow-black/40">
          <h1 class="mb-1 font-display text-2xl font-semibold text-white">Create account</h1>
          <p class="mb-8 text-sm text-slate-400">Start your journey with Simplernote.</p>
          <form @submit.prevent="submit" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">First name</label>
              <input v-model="firstName" @input="clearFieldError('first_name')" type="text" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.first_name ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="John" required />
              <p v-if="fieldErrors.first_name" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.first_name }}</p>
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Last name</label>
              <input v-model="lastName" @input="clearFieldError('last_name')" type="text" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.last_name ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="Doe" required />
              <p v-if="fieldErrors.last_name" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.last_name }}</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Country</label>
              <input v-model="country" @input="clearFieldError('country')" type="text" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.country ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="US" required />
              <p v-if="fieldErrors.country" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.country }}</p>
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">City</label>
              <input v-model="city" @input="clearFieldError('city')" type="text" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.city ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="New York" required />
              <p v-if="fieldErrors.city" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.city }}</p>
            </div>
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Email</label>
            <input v-model="email" @input="clearFieldError('email')" type="email" autocomplete="email" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.email ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="you@example.com" />
            <p v-if="fieldErrors.email" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.email }}</p>
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Password</label>
            <input v-model="password" @input="clearFieldError('password')" type="password" autocomplete="new-password" :class="['w-full rounded-xl border bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:ring-1', fieldErrors.password ? 'border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20' : 'border-slate-700/50 focus:border-violet-500/50 focus:ring-violet-500/20']" placeholder="Create a password" />
            <p v-if="fieldErrors.password" class="mt-1.5 text-xs text-red-400">{{ fieldErrors.password }}</p>
            <ul class="mt-2 space-y-1">
              <li v-for="c in criteria" :key="c.label" class="flex items-center gap-1.5 text-xs" :class="c.met ? 'text-green-400' : 'text-slate-500'">
                <span>{{ c.met ? '✓' : '○' }}</span>
                <span>{{ c.label }}</span>
              </li>
            </ul>
          </div>
          <p v-if="formError" class="rounded-lg bg-red-500/10 px-4 py-3 text-sm text-red-400">{{ formError }}</p>
          <button type="submit" :disabled="submitting" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed">
            {{ submitting ? 'Creating account...' : 'Create account' }}
          </button>
          <p class="text-center text-sm text-slate-500">
            Already have an account?
            <NuxtLink :to="'/login' + (redirect ? '?redirect=' + encodeURIComponent(redirect) : '')" class="font-medium text-violet-400 transition-colors hover:text-violet-300">Sign in</NuxtLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from "vue"
import { useRouter, useRoute } from "#app"
import { useAuthStore } from "@/stores/auth"

definePageMeta({ layout: false })

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref("")
const password = ref("")
const firstName = ref("")
const lastName = ref("")
const country = ref("")
const city = ref("")
const redirect = (route.query.redirect as string) || ""
const submitting = ref(false)
const formError = ref("")
const fieldErrors = reactive<{ first_name?: string; last_name?: string; country?: string; city?: string; email?: string; password?: string }>({})

function clearFieldError(field: string) {
  fieldErrors[field as keyof typeof fieldErrors] = undefined
  formError.value = ""
}

const criteria = computed(() => {
  const pw = password.value
  return [
    { label: "At least 8 characters", met: pw.length >= 8 },
    { label: "One uppercase letter", met: /[A-Z]/.test(pw) },
    { label: "One lowercase letter", met: /[a-z]/.test(pw) },
    { label: "One digit", met: /\d/.test(pw) },
    { label: "One special character", met: /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\';\/`~]/.test(pw) },
  ]
})

const submit = async () => {
  fieldErrors.first_name = undefined
  fieldErrors.last_name = undefined
  fieldErrors.country = undefined
  fieldErrors.city = undefined
  fieldErrors.email = undefined
  fieldErrors.password = undefined
  formError.value = ""

  if (!firstName.value.trim()) { fieldErrors.first_name = "First name is required"; return }
  if (!lastName.value.trim()) { fieldErrors.last_name = "Last name is required"; return }
  if (!country.value.trim()) { fieldErrors.country = "Country is required"; return }
  if (!city.value.trim()) { fieldErrors.city = "City is required"; return }
  if (!email.value.trim()) { fieldErrors.email = "Email is required"; return }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { fieldErrors.email = "Enter a valid email address"; return }
  if (!password.value) { fieldErrors.password = "Password is required"; return }

  const pw = password.value
  if (pw.length < 8) { fieldErrors.password = "Password must be at least 8 characters"; return }
  if (!/[A-Z]/.test(pw)) { fieldErrors.password = "Password must contain at least one uppercase letter"; return }
  if (!/[a-z]/.test(pw)) { fieldErrors.password = "Password must contain at least one lowercase letter"; return }
  if (!/\d/.test(pw)) { fieldErrors.password = "Password must contain at least one digit"; return }
  if (!/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\';\/`~]/.test(pw)) { fieldErrors.password = "Password must contain at least one special character"; return }

  submitting.value = true
  try {
    await auth.register(email.value, password.value, {
      first_name: firstName.value,
      last_name: lastName.value,
      country: country.value,
      city: city.value,
    })
    await router.push("/login" + (redirect ? "?redirect=" + encodeURIComponent(redirect) : ""))
  } catch (error: any) {
    const status = error?.response?.status
    const detail = error?.response?.data?.detail

    if (!error.response) {
      formError.value = "Connection error. Please check your network and try again."
    } else if (status === 429) {
      formError.value = "Too many attempts. Please wait a moment and try again."
    } else if (status === 409) {
      formError.value = "An account with this email already exists."
    } else if (status === 422 && Array.isArray(detail)) {
      detail.forEach((err: any) => {
        const field = err.loc?.at(-1)
        if (field === "email") fieldErrors.email = err.msg
        else if (field === "password") fieldErrors.password = err.msg
        else if (field === "first_name") fieldErrors.first_name = err.msg
        else if (field === "last_name") fieldErrors.last_name = err.msg
        else if (field === "country") fieldErrors.country = err.msg
        else if (field === "city") fieldErrors.city = err.msg
      })
      if (Object.values(fieldErrors).every(v => !v)) {
        formError.value = "Please check your input and try again."
      }
    } else {
      formError.value = typeof detail === "string" ? detail : "Registration failed. Please try again."
    }
  } finally {
    submitting.value = false
  }
}
</script>
