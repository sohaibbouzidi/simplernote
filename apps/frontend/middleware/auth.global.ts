import { useAuthStore } from "@/stores/auth"

export default defineNuxtRouteMiddleware((to) => {
  const publicPaths = ["/", "/login", "/register"]
  if (publicPaths.includes(to.path)) return

  const auth = useAuthStore()
  if (!auth.isAuthenticated) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  if (to.path.startsWith("/admin") && !auth.isAdmin) {
    return navigateTo("/dashboard")
  }
})