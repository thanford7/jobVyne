<template>
  <div class="row q-pb-sm border-bottom-2-gray-300">
    <h5 class="text-gray-900">{{ title }}</h5>
    <p class="text-gray-500 q-mt-none">
      <slot/>
    </p>
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    title: {
      type: String
    }
  }
}
</script>

<style scoped>

</style>
