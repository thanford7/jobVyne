<template>
  <div class="row q-pb-sm border-bottom-2-gray-300">
    <div class="col-12">
      <h5 class="text-gray-900">{{ title }}</h5>
    </div>
    <div class="col-12">
      <p class="text-gray-500 q-mt-none">
        <slot/>
      </p>
    </div>
    <div class="col-12">
      <slot name="bottom"/>
    </div>
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
