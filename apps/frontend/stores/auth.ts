import { defineStore } from "pinia"
import { getApiInstance, setAuthToken } from "@/services/api"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: "",
    refreshToken: "",
    user: null as
      | null
      | {
          id: string
          email: string
          role: string
          first_name?: string | null
          last_name?: string | null
          country?: string | null
          city?: string | null
          picture?: string | null
          picture_url?: string | null
        },
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === "admin",
    isProfileComplete: (state) =>
      !!(
        state.user &&
        state.user.first_name &&
        state.user.last_name &&
        state.user.country &&
        state.user.city
      ),
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
        // if user has a picture (S3 key), request a presigned URL
        try {
          if (this.user?.picture) {
            const r2 = await api.get("/users/me/picture-url")
            this.user.picture_url = r2.data.url
          }
        } catch {}
        this._persist()
      } catch {
        this.clear()
      }
    },
    async updateProfile(payload: {
      first_name?: string | null
      last_name?: string | null
      country?: string | null
      city?: string | null
      picture?: string | null
    }) {
      const api = getApiInstance()
      const res = await api.patch("/users/me", payload)
      // this.token = res.data.access_token
      // this.refreshToken = res.data.refresh_token
      this.user = res.data
      // refresh presigned URL if picture key changed
      try {
        if (this.user?.picture) {
          const r2 = await api.get("/users/me/picture-url")
          this.user.picture_url = r2.data.url
        } else {
          this.user.picture_url = null
        }
      } catch {}
      this._persist()
      return res.data
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
    async register(email: string, password: string, profile: { first_name: string; last_name: string; country: string; city: string }) {
      const api = getApiInstance()
      const response = await api.post("/auth/register", { email, password, ...profile })
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
