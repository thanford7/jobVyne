<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <q-input
    v-if="isLoaded"
    filled
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    :label="label"
    lazy-rules
    :rules="rules"
    style="width: 250px;"
  >
    <template v-slot:prepend>
      <div v-if="modelValue" class="h-75" :style="colorStyle"></div>
    </template>
    <template v-slot:append>
      <q-icon name="colorize">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-color
            :model-value="modelValue"
            @update:model-value="$emit('update:model-value', $event)"
            :default-view="(isIncludeEmployerColors) ? 'palette' : 'spectrum'"
            :palette="[...employerColors, ...defaultColors]"
          />
        </q-popup-proxy>
      </q-icon>
    </template>
    <q-tooltip class="bg-info" style="font-size: 14px;" max-width="300px">
      Input a hex color (e.g. #ffffff) or click the
      <q-icon name="colorize" size="sm"/>
      icon to
      select from a color palette
    </q-tooltip>
  </q-input>
</template>

<script>
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

// https://github.com/quasarframework/quasar/blob/dev/ui/src/utils/patterns.js
const hexRegex = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/

export default {
  name: 'ColorPicker',
  props: {
    modelValue: {
      type: [String, null]
    },
    label: String,
    isIncludeEmployerColors: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      defaultColors: [
        '#2a2b2b',
        '#696e6e',
        '#f2f5f5'
      ]
    }
  },
  computed: {
    colorStyle () {
      return {
        width: '25px',
        borderRadius: '25px',
        border: '1px solid gray',
        backgroundColor: this.modelValue || '#ffffff'
      }
    },
    employerColors () {
      const employer = this.employerStore.getEmployer(this.user.employer_id)
      if (dataUtil.isNil(employer)) {
        return []
      }
      return ['color_primary', 'color_secondary', 'color_accent'].reduce((colors, colorKey) => {
        const color = employer[colorKey]
        if (color) {
          colors.push(color)
        }
        return colors
      }, [])
    },
    rules () {
      const rules = []
      if (this.isRequired) {
        rules.push((v) => v || 'A color value is required')
      }
      const isValidHexFn = (v) => !v || hexRegex.test(v) || 'Value must be formatted as a hex (e.g. #ffffff)'
      rules.push(isValidHexFn)
      return rules
    }
  },
  async mounted () {
    if (this.isIncludeEmployerColors) {
      await this.authStore.setUser().then(() => {
        return Promise.all([
          this.employerStore.setEmployer(this.user.employer_id)
        ])
      })
    }
    this.isLoaded = true
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      authStore,
      employerStore: useEmployerStore(),
      user
    }
  }
}
</script>
