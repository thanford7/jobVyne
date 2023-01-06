<template>
  <q-card class="testimonial-card">
    <q-img class="testimonial-card__headshot" :src="headshotSrc"/>
    <q-card-section
      class="border-bottom-1-gray-500 bg-primary text-white"
      style="padding-top: 70px; border-top-left-radius: 6px; border-top-right-radius: 6px;"
    >
      <div class="text-center" style="font-size: 20px">{{ name }}</div>
      <div class="text-center">{{ jobTitle }}</div>
    </q-card-section>
    <q-card-section>
      <div class="rfs-h6 text-center"><em>{{ quote }}</em></div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'TestimonialCard',
  props: {
    headshotSrc: String,
    quote: String,
    jobTitle: String,
    name: String
  }
}
</script>

<style lang="scss" scoped>
.testimonial-card {
  position: relative;

  &__headshot {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateY(-50%) translateX(-50%);
    width: 120px;
    height: 120px;
    border: 1px solid $gray-300;
    border-radius: 150px !important;
    z-index: 50;
  }
}
</style>
