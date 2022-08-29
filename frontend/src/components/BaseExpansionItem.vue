<template>
  <q-expansion-item
    default-opened dense expand-separator
    expand-icon="expand_more"
    expanded-icon="expand_less"
    header-class="bg-gray-100"
    :class="(isIncludeSeparator) ? 'border-bottom-1-gray-100' : null"
  >
    <template v-slot:header>
      <div class="flex items-center w-100">
        <span class="text-bold">{{title}}</span>
        <slot name="header"/>
        <q-space/>
      </div>
    </template>
    <div class="q-pa-sm">
      <slot/>
    </div>
  </q-expansion-item>
</template>

<script>
export default {
  name: 'BaseExpansionItem',
  props: {
    title: String,
    isIncludeSeparator: {
      type: Boolean,
      default: true
    }
  }
}
</script>
