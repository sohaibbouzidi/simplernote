import { defineStore } from "pinia"
import { getApiInstance, setAuthToken } from "@/services/api"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: "",
    refreshToken: "",
    user: null as null | { id: string; email: string },
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    setToken(token: string) {
      this.token = token
      setAuthToken(token)
    },
    clear() {
      this.token = ""
      this.refreshToken = ""
      this.user = null
    },
    async login(email: string, password: string) {
      const api = getApiInstance()
      const response = await api.post("/auth/login", { email, password })
      this.token = response.data.access_token
      this.refreshToken = response.data.refresh_token
      setAuthToken(this.token)
    },
    async register(email: string, password: string) {
      const api = getApiInstance()
      const response = await api.post("/auth/register", { email, password })
      this.user = response.data
      return response.data
    },
  },
})
