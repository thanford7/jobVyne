<template>
  <q-editor
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    @blur="updateSanitizeHtml"
    class="scrollbar-narrow"
    :placeholder="placeholder"
    toolbar-bg="grey-3"
    toolbar-text-color="grey-8"
    :dense="$q.screen.lt.md"
    :toolbar="[
        [
          {
            label: $q.lang.editor.align,
            icon: $q.iconSet.editor.align,
            fixedLabel: true,
            options: ['left', 'center', 'right', 'justify']
          }
        ],
        ['bold', 'italic', 'underline'],
        ['hr'],
        [
          {
            label: $q.lang.editor.formatting,
            icon: $q.iconSet.editor.formatting,
            list: 'no-icons',
            options: [
              'p',
              'h1',
              'h2',
              'h3',
              'h4',
              'h5',
              'h6'
            ]
          },
          'removeFormat'
        ],
        ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
        ['undo', 'redo']
      ]"
  />
</template>

<script>
import sanitizeHtml from 'sanitize-html'

// Needs to align with backend sanitization cfg (sanitize.py)
const colorMatch = [/^#(0x)?[0-9a-f]+$/i, /^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/] // Match HEX and RGB
const sizeMatch = [/^-?\d+(?:px|em|%)$/, /0/] // Match any positive/negative number with px, em, or %
const sanitizeCfg = {
  allowedAttributes: {
    '*': ['class', 'style'],
    a: ['href', 'name', 'target', 'title', 'id', 'rel']
  },
  allowedStyles: {
    '*': {
      'background-color': colorMatch,
      'border-bottom-color': colorMatch,
      'border-collapse': [/^collapse$/, /^separate$/],
      'border-color': colorMatch,
      'border-left-color': colorMatch,
      'border-right-color': colorMatch,
      'border-top-color': colorMatch,
      color: colorMatch,
      float: [/^left$/, /^right$/, /^none$/, /^inline-start$/, /^inline-end$/],
      'font-size': sizeMatch,
      'font-weight': [/^normal$/, /^bold$/, /^lighter$/, /^bolder$/],
      height: sizeMatch,
      'text-align': [/^left$/, /^right$/, /^center$/],
      'text-decoration': [/^underline$/, /^overline$/, /^none$/],
      'text-indent': sizeMatch,
      'vertical-align': [/^baseline$/, /^sub$/, /^super$/, /^text-top$/, /^text-bottom$/, /^middle$/, /^top$/, /^bottom$/],
      'white-space': [/^normal$/, /^nowrap$/, /^pre$/, /^pre-wrap$/, /^pre-line$/, /^break-spaces$/],
      width: sizeMatch
    }
  }
}

export default {
  name: 'WysiwygEditor',
  props: {
    modelValue: {
      type: [String],
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Start typing...'
    }
  },
  data () {
    return {
      sanitizeHtml
    }
  },
  methods: {
    updateSanitizeHtml () {
      const sanitizedHtml = sanitizeHtml(this.modelValue, sanitizeCfg)
      this.$emit('update:modelValue', sanitizedHtml)
    }
  }
}
</script>
