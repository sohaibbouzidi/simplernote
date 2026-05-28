import { defineNuxtConfig } from "nuxt"

export default defineNuxtConfig({
  ssr: false,
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],
  css: ["@/assets/css/tailwind.css"],
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || "http://localhost:8000/api",
    },
  },
})
