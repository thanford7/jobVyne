<template>
<q-card class="q-px-md q-pb-sm">
    <q-card-section>
      <div class="q-pb-sm border-bottom-1-gray-300">
        <div class="rfs-h6">{{ title }}</div>
        <div>{{ subTitle }}</div>
      </div>
      <div class="q-mt-lg">
        <slot/>
      </div>
    </q-card-section>
    <q-card-actions align="right">
      <slot name="buttons"></slot>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  name: 'BaseStep',
  props: {
    title: String,
    subTitle: [String, null]
  }
}
</script>
