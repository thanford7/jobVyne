<template>
  <q-intersection once style="min-height: 150px" transition="scale" :threshold="0.8"
                  transition-duration="700">
    <q-card>
      <q-card-section>
        <div class="rfs-h4 font-primary text-center text-bold text-secondary">
          {{ stat }}
        </div>
        <div class="rfs-h6 text-center">
          {{ description }}
        </div>
      </q-card-section>
    </q-card>
  </q-intersection>
</template>

<script>
export default {
  name: 'BenefitItem',
  props: {
    stat: String,
    description: String
  }
}
</script>

<style scoped>

</style>
