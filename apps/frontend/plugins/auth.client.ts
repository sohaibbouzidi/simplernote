import { useAuthStore } from "@/stores/auth"

export default defineNuxtPlugin(() => {
  const auth = useAuthStore()
  auth.init()
  if (auth.token) {
    auth.fetchUser()
  }
})