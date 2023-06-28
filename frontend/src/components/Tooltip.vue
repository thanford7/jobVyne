<template>
  <q-tooltip class="border-4-info bg-white text-grey-9" style="font-size: 16px;" max-width="500px">
      <slot/>
  </q-tooltip>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Tooltip'
}
</script>
