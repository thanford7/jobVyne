<template>
  <div class="row">
    <div class="col-12 col-md-4">
      <div class="h-100 flex justify-center items-center">
        <slot name="icon"/>
      </div>
    </div>
    <div class="col-12 col-md-8 q-mt-lg q-mt-md-none">
      <div class="rfs-h6">
        {{ header }}
      </div>
      <q-list class="q-mt-md">
        <q-item v-for="benefit in benefits">
          <q-item-section avatar>
            <q-icon name="thumb_up_alt" color="primary"/>
          </q-item-section>
          <q-item-section>
            {{ benefit }}
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HowItWorksItem',
  props: {
    header: String,
    benefits: Array
  }
}
</script>

<style scoped>

</style>
