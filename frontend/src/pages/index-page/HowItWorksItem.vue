<template>
  <div class="row">
    <div class="col-12 col-md-4">
      <div class="h-100 flex justify-center items-center">
        <slot name="icon"/>
      </div>
    </div>
    <div class="col-12 col-md-8 q-mt-lg q-mt-md-none">
      <div class="rfs-h5">
        {{ header }}
      </div>
      <ListIcon class="q-mt-md rfs-h6"
        :items="benefits"
        color="primary"
        icon-name="thumb_up_alt" icon-size="50px"
      />
    </div>
  </div>
</template>

<script>
import ListIcon from 'components/ListIcon.vue'

export default {
  name: 'HowItWorksItem',
  components: { ListIcon },
  props: {
    header: String,
    benefits: Array
  }
}
</script>

<style scoped>

</style>
