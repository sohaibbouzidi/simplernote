<template>
  <div class="mx-auto max-w-md rounded-3xl border border-slate-800 bg-slate-900/90 p-8 shadow-xl shadow-slate-950/20">
    <h1 class="mb-6 text-3xl font-semibold text-white">Create account</h1>
    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="mb-2 block text-sm text-slate-300">Email</label>
        <input v-model="email" type="email" class="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-brand-400" />
      </div>
      <div>
        <label class="mb-2 block text-sm text-slate-300">Password</label>
        <input v-model="password" type="password" class="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-brand-400" />
      </div>
      <button class="w-full rounded-2xl bg-brand-500 px-4 py-3 text-white hover:bg-brand-400">Register</button>
      <p class="text-sm text-slate-400">Already have an account? <NuxtLink to="/login" class="text-brand-300">Login</NuxtLink></p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "#app"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const router = useRouter()
const email = ref("")
const password = ref("")

const submit = async () => {
  try {
    await auth.register(email.value, password.value)
    await router.push("/login")
  } catch (error) {
    console.error(error)
    alert("Registration failed. Please try again.")
  }
}
</script>
