import axios, { AxiosInstance } from "axios"
import { useRuntimeConfig } from "#app"

let apiInstance: AxiosInstance | null = null

export function getApiInstance() {
  if (!apiInstance) {
    const config = useRuntimeConfig()
    apiInstance = axios.create({
      baseURL: config.public.apiBase,
      headers: {
        "Content-Type": "application/json",
      },
    })
  }
  return apiInstance
}

export function setAuthToken(token: string) {
  const api = getApiInstance()
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`
}
