<template>
  <div class="rich-text-editor rounded-md border border-slate-700 bg-surface overflow-hidden">
    <div class="flex flex-wrap items-center gap-0.5 border-b border-slate-700 bg-surface-50 px-2 py-1.5">
      <button type="button" @click="editor?.chain().focus().toggleBold().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('bold') && 'bg-slate-700 text-white']" title="Bold">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M15.6 10.79c.97-.67 1.65-1.77 1.65-2.79 0-2.26-1.75-4-4-4H8v14h7.04c2.09 0 3.71-1.7 3.71-3.79 0-1.52-.86-2.82-2.15-3.42zM10 6.5h3c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5h-3v-3zm3.5 9H10v-3h3.5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().toggleItalic().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('italic') && 'bg-slate-700 text-white']" title="Italic">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M10 4v3h2.21l-3.42 8H6v3h8v-3h-2.21l3.42-8H18V4z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().toggleStrike().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('strike') && 'bg-slate-700 text-white']" title="Strikethrough">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M10 19h4v-3h-4v3zM5 4v3h5v3h4V7h5V4H5zM3 14h18v-2H3v2z"/></svg>
      </button>
      <span class="mx-1 h-5 w-px bg-slate-700" />
      <button type="button" @click="editor?.chain().focus().toggleHeading({ level: 1 }).run()" :class="['rounded p-1.5 text-xs font-bold text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('heading', { level: 1 }) && 'bg-slate-700 text-white']" title="Heading 1">H1</button>
      <button type="button" @click="editor?.chain().focus().toggleHeading({ level: 2 }).run()" :class="['rounded p-1.5 text-xs font-semibold text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('heading', { level: 2 }) && 'bg-slate-700 text-white']" title="Heading 2">H2</button>
      <button type="button" @click="editor?.chain().focus().toggleHeading({ level: 3 }).run()" :class="['rounded p-1.5 text-xs font-medium text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('heading', { level: 3 }) && 'bg-slate-700 text-white']" title="Heading 3">H3</button>
      <span class="mx-1 h-5 w-px bg-slate-700" />
      <button type="button" @click="editor?.chain().focus().toggleBulletList().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('bulletList') && 'bg-slate-700 text-white']" title="Bullet list">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M4 10.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm0-6c-.83 0-1.5.67-1.5 1.5S3.17 7.5 4 7.5 5.5 6.83 5.5 6 4.83 4.5 4 4.5zm0 12c-.83 0-1.5.68-1.5 1.5s.68 1.5 1.5 1.5 1.5-.68 1.5-1.5-.67-1.5-1.5-1.5zM7 19h14v-2H7v2zm0-6h14v-2H7v2zm0-8v2h14V5H7z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().toggleOrderedList().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('orderedList') && 'bg-slate-700 text-white']" title="Ordered list">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M2 17h2v.5H3v1h1v.5H2v1h3v-4H2v1zm1-9h1V4H2v1h1v3zm-1 3h1.8L2 13.1v.9h3v-1H3.2L5 10.9V10H2v1zm5-6v2h14V5H7zm0 14h14v-2H7v2zm0-6h14v-2H7v2z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().toggleBlockquote().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('blockquote') && 'bg-slate-700 text-white']" title="Blockquote">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().toggleCodeBlock().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('codeBlock') && 'bg-slate-700 text-white']" title="Code block">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().toggleCode().run()" :class="['rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors', editor?.isActive('code') && 'bg-slate-700 text-white']" title="Inline code">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M14.6 16.6l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4zm-5.2 0L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4z"/></svg>
      </button>
      <span class="mx-1 h-5 w-px bg-slate-700" />
      <button type="button" @click="editor?.chain().focus().undo().run()" class="rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors" title="Undo">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z"/></svg>
      </button>
      <button type="button" @click="editor?.chain().focus().redo().run()" class="rounded p-1.5 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors" title="Redo">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M11.5 8c-4.65 0-8.58 3.03-9.97 7.22l2.37.78C5.95 12.31 8.96 10 12.5 10c1.96 0 3.73.72 5.12 1.88L14 15.5h9v-9l-3.62 3.62C17.55 8.99 15.15 8 12.5 8z"/></svg>
      </button>
    </div>
    <editor-content :editor="editor" class="prose prose-invert max-w-none px-4 py-3 text-sm text-white min-h-[160px] focus:outline-none" />
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from "@tiptap/vue-3"
import StarterKit from "@tiptap/starter-kit"
import Placeholder from "@tiptap/extension-placeholder"
import { computed, watch } from "vue"

const props = defineProps<{ modelValue: string; placeholder?: string }>()
const emit = defineEmits<{ (e: "update:modelValue", v: string): void }>()

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      heading: { levels: [1, 2, 3] },
    }),
    Placeholder.configure({
      placeholder: props.placeholder || "Start writing...",
    }),
  ],
  onUpdate: ({ editor }) => {
    emit("update:modelValue", editor.getHTML())
  },
})

watch(() => props.modelValue, (val) => {
  if (editor.value && val !== editor.value.getHTML()) {
    editor.value.commands.setContent(val, false)
  }
})
</script>

<style>
.rich-text-editor .ProseMirror {
  outline: none;
  min-height: 160px;
}
.rich-text-editor .ProseMirror p.is-editor-empty:first-child::before {
  color: #64748b;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}
.rich-text-editor .ProseMirror pre {
  background: #1e293b;
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  overflow-x: auto;
}
.rich-text-editor .ProseMirror code {
  background: #1e293b;
  border-radius: 0.25rem;
  padding: 0.125rem 0.375rem;
  font-size: 0.875rem;
}
.rich-text-editor .ProseMirror blockquote {
  border-left: 3px solid #334155;
  padding-left: 1rem;
  color: #94a3b8;
  font-style: italic;
}
.rich-text-editor .ProseMirror ul,
.rich-text-editor .ProseMirror ol {
  padding-left: 1.5rem;
}
.rich-text-editor .ProseMirror h1 {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.3;
}
.rich-text-editor .ProseMirror h2 {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.35;
}
.rich-text-editor .ProseMirror h3 {
  font-size: 1.125rem;
  font-weight: 500;
  line-height: 1.4;
}
</style>
