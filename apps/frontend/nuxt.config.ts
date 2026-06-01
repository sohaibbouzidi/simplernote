import { defineNuxtConfig } from "nuxt/config"

export default defineNuxtConfig({
  ssr: false,
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],
  css: ["@/assets/css/tailwind.css"],
  app: {
    head: {
      title: "Simpler Notes for your AI",
      link: [
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
      ],
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || "http://localhost/api",
    },
  },
})
