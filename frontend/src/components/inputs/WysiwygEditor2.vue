<template>
  <div>
    <div v-if="editor" class="tip-editor-menu scrollbar-narrow" style="max-width: 100%">
      <div class="row no-wrap scroll-x">
        <div class="flex items-center no-wrap border-right-1-gray-300 q-px-xs">
          <q-btn
            flat dense icon="align_horizontal_left" title="Align left"
            :class="{ 'tip-is-active': editor.isActive({ textAlign: 'left' }) }"
            @click="editor.chain().focus().setTextAlign('left').run()"
          />
          <q-btn
            flat dense icon="align_horizontal_center" title="Align center"
            :class="{ 'tip-is-active': editor.isActive({ textAlign: 'center' }) }"
            @click="editor.chain().focus().setTextAlign('center').run()"
          />
          <q-btn
            flat dense icon="align_horizontal_right" title="Align right"
            :class="{ 'tip-is-active': editor.isActive({ textAlign: 'right' }) }"
            @click="editor.chain().focus().setTextAlign('right').run()"
          />
        </div>
        <div class="flex items-center no-wrap border-right-1-gray-300 q-px-xs" style="flex-wrap: nowrap;">
          <q-btn
            flat dense icon="format_list_bulleted" title="Bullet list"
            :class="{ 'tip-is-active': editor.isActive('bulletList') }"
            @click="editor.chain().focus().toggleBulletList().run()"
          />
          <q-btn
            flat dense icon="format_list_numbered" title="Number list"
            :class="{ 'tip-is-active': editor.isActive('orderedList') }"
            @click="editor.chain().focus().toggleOrderedList().run()"
          />
          <q-btn
            flat dense icon="format_indent_increase" title="Increase indent"
            :disabled="!editor.can().sinkListItem('listItem')"
            @click="editor.chain().focus().sinkListItem('listItem').run()"
          />
          <q-btn
            flat dense icon="format_indent_decrease" title="Decrease indent"
            :disabled="!editor.can().liftListItem('listItem')"
            @click="editor.chain().focus().liftListItem('listItem').run()"
          />
          <q-btn
            flat dense icon="format_quote" title="Quote"
            :class="{ 'tip-is-active': editor.isActive('blockquote') }"
            @click="editor.chain().focus().toggleBlockquote().run()"
          />
          <q-btn
            flat dense icon="horizontal_rule" title="Horizontal rule"
            @click="editor.chain().focus().setHorizontalRule().run()"
          />
        </div>
        <div class="flex items-center no-wrap border-right-1-gray-300 q-px-xs" style="flex-wrap: nowrap;">
          <q-btn
            flat dense label="H1" title="Heading 1" size="16px" style="width: 32px;"
            :class="{ 'tip-is-active': editor.isActive('heading', { level: 4 }) }"
            @click="editor.chain().focus().toggleHeading({ level: 4 }).run()"
          />
          <q-btn
            flat dense label="H2" title="Heading 2" size="16px" style="width: 32px;"
            :class="{ 'tip-is-active': editor.isActive('heading', { level: 5 }) }"
            @click="editor.chain().focus().toggleHeading({ level: 5 }).run()"
          />
          <q-btn
            flat dense label="H3" size="16px" title="Heading 3" style="width: 32px;"
            :class="{ 'tip-is-active': editor.isActive('heading', { level: 6 }) }"
            @click="editor.chain().focus().toggleHeading({ level: 6 }).run()"
          />
          <q-btn
            flat dense label="P" title="Paragraph" size="16px" style="width: 32px;"
            :class="{ 'tip-is-active': editor.isActive('paragraph') }"
            @click="editor.chain().focus().setParagraph().run()"
          />
        </div>
        <div class="flex items-center no-wrap q-px-xs" style="flex-wrap: nowrap;">
          <q-btn
            flat dense icon="undo" title="Undo"
            @click="editor.chain().focus().undo().run()"
            :disabled="!editor.can().undo()"
          />
          <q-btn
            flat dense icon="redo" title="Redo"
            @click="editor.chain().focus().redo().run()"
            :disabled="!editor.can().redo()"
          />
        </div>
      </div>
    </div>
    <editor-content :editor="editor" class="tip-editor"/>
    <bubble-menu
      :editor="editor"
      :tippy-options="{ duration: 100 }"
      v-if="editor"
    >
      <button @click="editor.chain().focus().toggleBold().run()" :class="{ 'tip-is-active': editor.isActive('bold') }">
        Bold
      </button>
      <button @click="editor.chain().focus().toggleItalic().run()"
              :class="{ 'tip-is-active': editor.isActive('italic') }">
        Italic
      </button>
      <button @click="editor.chain().focus().toggleUnderline().run()"
              :class="{ 'tip-is-active': editor.isActive('underline') }">
        Underline
      </button>
    </bubble-menu>
  </div>
</template>

<script>
import { BubbleMenu, Editor, EditorContent, mergeAttributes } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import HorizontalRule from '@tiptap/extension-horizontal-rule'
import Paragraph from '@tiptap/extension-paragraph'
import Placeholder from '@tiptap/extension-placeholder'
import TextAlign from '@tiptap/extension-text-align'
import Underline from '@tiptap/extension-underline'

const textAlignClassMap = {
  left: 'text-left',
  center: 'text-center',
  right: 'text-right'
}

export const CustomParagraph = Paragraph.extend({
  renderHTML ({ node, HTMLAttributes }) {
    const textAlignmentStyle = node.attrs.textAlign
    const textAlignmentClass = (textAlignmentStyle) ? textAlignClassMap[textAlignmentStyle] : textAlignClassMap.left

    return [
      'p',
      mergeAttributes(this.options.HTMLAttributes, HTMLAttributes, {
        class: textAlignmentClass
      }), 0
    ]
  }
})

export default {
  name: 'WysiwygEditor2',
  components: {
    BubbleMenu,
    EditorContent
  },
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Start typing...'
    }
  },
  data () {
    return {
      editor: null
    }
  },
  watch: {
    modelValue (value) {
      // HTML
      const isSame = this.editor.getHTML() === value

      // JSON
      // const isSame = JSON.stringify(this.editor.getJSON()) === JSON.stringify(value)

      if (isSame) {
        return
      }
      this.editor.commands.setContent(value, false)
    }
  },

  mounted () {
    this.editor = new Editor({
      extensions: [
        StarterKit.configure({
          heading: {
            levels: [4, 5, 6]
          },
          paragraph: false
        }),
        CustomParagraph,
        HorizontalRule,
        TextAlign.configure({
          types: ['heading', 'paragraph'],
          alignments: ['left', 'center', 'right']
        }),
        Underline,
        Placeholder.configure({
          placeholder: this.placeholder
        })
      ],
      content: this.modelValue,
      onUpdate: () => {
        // HTML
        this.$emit('update:modelValue', this.editor.getHTML())

        // JSON
        // this.$emit('update:modelValue', this.editor.getJSON())
      }
    })
  },

  beforeUnmount () {
    this.editor.destroy()
  }
}
</script>

<style lang="scss">
.tip-editor {
  width: 100%;
  border-radius: 0 0 6px 6px;
  border: 1px solid $grey-4;

  .ProseMirror {
    padding: 8px 16px;
    border: 0;

    &-focused {
      outline: none;
    }

    p.is-editor-empty:first-child::before {
      content: attr(data-placeholder);
      float: left;
      color: #adb5bd;
      pointer-events: none;
      height: 0;
    }
  }
}

.tip-editor-menu {
  border: 1px solid $grey-4;
  border-radius: 6px 6px 0 0;
  background-color: $grey-2;

  .row {
    padding: 6px;
  }
}

.tip-is-active {
  background-color: $gray-500;
  color: $white;
}
</style>
