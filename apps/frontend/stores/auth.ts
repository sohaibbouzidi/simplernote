import { defineStore } from "pinia"
import { getApiInstance, setAuthToken } from "@/services/api"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: "",
    refreshToken: "",
    user: null as null | { id: string; email: string; role: string },
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === "admin",
  },
  actions: {
    init() {
      const saved = localStorage.getItem("simplernote_auth")
      if (saved) {
        try {
          const data = JSON.parse(saved)
          this.token = data.token || ""
          this.refreshToken = data.refreshToken || ""
          this.user = data.user || null
          if (this.token) setAuthToken(this.token)
        } catch {
          localStorage.removeItem("simplernote_auth")
        }
      }
    },
    setToken(token: string) {
      this.token = token
      setAuthToken(token)
      this._persist()
    },
    clear() {
      this.token = ""
      this.refreshToken = ""
      this.user = null
      setAuthToken("")
      localStorage.removeItem("simplernote_auth")
    },
    async fetchUser() {
      const api = getApiInstance()
      try {
        const res = await api.get("/auth/me")
        this.user = res.data
        this._persist()
      } catch {
        this.clear()
      }
    },
    async login(email: string, password: string) {
      const api = getApiInstance()
      const response = await api.post("/auth/login", { email, password })
      this.token = response.data.access_token
      this.refreshToken = response.data.refresh_token
      setAuthToken(this.token)
      await this.fetchUser()
      this._persist()
    },
    async register(email: string, password: string) {
      const api = getApiInstance()
      const response = await api.post("/auth/register", { email, password })
      this.user = response.data
      return response.data
    },
    _persist() {
      localStorage.setItem(
        "simplernote_auth",
        JSON.stringify({
          token: this.token,
          refreshToken: this.refreshToken,
          user: this.user,
        }),
      )
    },
  },
})
