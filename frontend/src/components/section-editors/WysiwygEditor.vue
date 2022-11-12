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
              'h4',
              'h5',
              'h6',
              'p'
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
import formUtil from 'src/utils/form.js'

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
  methods: {
    updateSanitizeHtml () {
      const sanitizedHtml = formUtil.sanitizeHtml(this.modelValue)
      this.$emit('update:modelValue', sanitizedHtml)
    }
  }
}
</script>
