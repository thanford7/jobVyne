<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <q-input
    filled
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    :label="label"
    lazy-rules :rules="['anyColor']"
    style="width: 250px;"
  >
    <template v-slot:prepend>
      <div class="h-75" :style="colorStyle"></div>
    </template>
    <template v-slot:append>
      <q-icon name="colorize">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-color
            :model-value="modelValue"
            @update:model-value="$emit('update:model-value', $event)"
          />
        </q-popup-proxy>
      </q-icon>
    </template>
    <q-tooltip class="bg-info" style="font-size: 14px;" max-width="300px">
      Input a hex color (e.g. #ffffff) or click the <q-icon name="colorize" size="sm"/> icon to
      select from a color palette
    </q-tooltip>
  </q-input>
</template>

<script>
export default {
  name: 'ColorPicker',
  props: {
    modelValue: {
      type: [String, null]
    },
    label: String
  },
  computed: {
    colorStyle () {
      return {
        width: '25px',
        borderRadius: '25px',
        backgroundColor: this.modelValue || '#ffffff'
      }
    }
  }
}
</script>
