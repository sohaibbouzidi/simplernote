<template>
  <div class="flex min-h-screen items-center justify-center bg-surface px-4">
    <div class="w-full max-w-md animate-fade-in-up">
      <div class="mb-8 text-center">
        <NuxtLink to="/" class="mb-6 inline-flex items-center gap-2.5">
          <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-fuchsia-400 text-sm font-bold leading-none text-white shadow-lg shadow-violet-500/20">S</span>
          <span class="font-display text-xl font-semibold tracking-tight text-white">Simplernote</span>
        </NuxtLink>
      </div>
      <div class="rounded-2xl border border-slate-800/60 bg-surface-50 p-8 shadow-2xl shadow-black/40">
        <h1 class="mb-1 font-display text-2xl font-semibold text-white">Complete your profile</h1>
        <p class="mb-8 text-sm text-slate-400">Please provide the required information to continue.</p>
        <form @submit.prevent="submit" class="space-y-5">
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">First name</label>
            <input v-model="first_name" type="text" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Last name</label>
            <input v-model="last_name" type="text" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Country</label>
            <input v-model="country" type="text" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">City</label>
            <input v-model="city" type="text" class="w-full rounded-xl border border-slate-700/50 bg-surface px-4 py-3 text-sm text-white outline-none transition-all placeholder:text-slate-600 focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/20" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Picture</label>
            <input @change="onFileChange" type="file" accept="image/*" class="w-full text-sm text-white" />
            <div v-if="previewUrl" class="mt-3">
              <img :src="previewUrl" alt="preview" class="h-24 w-24 rounded-full object-cover" />
            </div>
            <div v-if="isUploading" class="mt-2">
              <div class="h-2 w-full rounded bg-slate-700">
                <div :style="`width: ${uploadProgress}%`" class="h-2 rounded bg-violet-500"></div>
              </div>
              <p class="mt-1 text-xs text-slate-400">Uploading... {{ uploadProgress }}%</p>
            </div>
          </div>
          <button :disabled="isUploading" type="submit" class="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition-all hover:shadow-xl hover:shadow-violet-500/30 hover:brightness-110 disabled:opacity-60">
            <span v-if="isUploading">Uploading…</span>
            <span v-else>Save profile</span>
          </button>
          <NuxtLink to="/profile" class="mt-3 block w-full rounded-xl border border-slate-700/50 px-4 py-3 text-center text-sm font-medium text-slate-400 transition-all hover:border-slate-600 hover:text-white">Cancel</NuxtLink>
        </form>
      </div>
    </div>
    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter, useRoute } from "#app"
import { useAuthStore } from "@/stores/auth"
import { useToast } from "@/composables/useToast"
import { getApiInstance } from "@/services/api"

definePageMeta({ layout: false })

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()

const first_name = ref(auth.user?.first_name || "")
const last_name = ref(auth.user?.last_name || "")
const country = ref(auth.user?.country || "")
const city = ref(auth.user?.city || "")
const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(auth.user?.picture_url || null)
const uploadProgress = ref(0)
const isUploading = ref(false)

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
const MAX_BYTES = 5 * 1024 * 1024 // 5 MB

async function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (!target.files || !target.files[0]) return
  const file = target.files[0]
  // client-side validations
  if (!ALLOWED_TYPES.includes(file.type)) {
    toast.error("Invalid image type. Allowed: JPG, PNG, WEBP")
    selectedFile.value = null
    previewUrl.value = null
    return
  }
  if (file.size > MAX_BYTES) {
    toast.error("Image too large (max 5MB)")
    selectedFile.value = null
    previewUrl.value = null
    return
  }
  selectedFile.value = file
  try {
    previewUrl.value = URL.createObjectURL(file)
  } catch (err) {
    console.error(err)
    toast.error("Failed to read picture file")
  }
}

const submit = async () => {
  if (!first_name.value || !last_name.value || !country.value || !city.value) {
    toast.error("Please fill all required fields.")
    return
  }

  try {
    const api = getApiInstance()
    // upload picture first if present
    if (selectedFile.value) {
      const form = new FormData()
      form.append("file", selectedFile.value)
      isUploading.value = true
      uploadProgress.value = 0
      const res = await api.post("/users/me/picture", form, {
        onUploadProgress: (progressEvent: ProgressEvent) => {
          if (progressEvent.lengthComputable) {
            uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          }
        },
      })
      // update local user with returned data (picture is stored as S3 key)
      auth.user = res.data
      // fetch presigned URL for the newly uploaded picture
      try {
        const r2 = await api.get('/users/me/picture-url')
        auth.user.picture_url = r2.data.url
        previewUrl.value = r2.data.url
      } catch (e) {
        previewUrl.value = null
      }
      isUploading.value = false
      uploadProgress.value = 0
    }

    await auth.updateProfile({
      first_name: first_name.value,
      last_name: last_name.value,
      country: country.value,
      city: city.value,
    })
    toast.success("Profile updated")
    const redirect = (route.query.redirect as string) || "/dashboard"
    await router.push(redirect)
  } catch (err) {
    console.error(err)
    isUploading.value = false
    uploadProgress.value = 0
    toast.error("Failed to update profile. Try again.")
  }
}
</script>
