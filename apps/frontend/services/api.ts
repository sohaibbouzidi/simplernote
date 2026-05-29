import axios, { AxiosInstance } from "axios"
import { useRuntimeConfig } from "#app"
import { useAuthStore } from "@/stores/auth"

let apiInstance: AxiosInstance | null = null

export function getApiInstance() {
  if (!apiInstance) {
    const config = useRuntimeConfig()
    apiInstance = axios.create({
      baseURL: config.public.apiBase,
      maxRedirects: 5,
    })
    apiInstance.interceptors.request.use((config) => {
      try {
        const auth = useAuthStore()
        if (auth.token) {
          config.headers.Authorization = `Bearer ${auth.token}`
        }
      } catch {}
      return config
    })
  }
  return apiInstance
}

export function setAuthToken(token: string) {
  const api = getApiInstance()
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`
}
