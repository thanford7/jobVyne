<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <q-carousel
        swipeable animated thumbnails infinite
        v-model="slide"
      >
        <q-carousel-slide :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg"/>
        <q-carousel-slide :name="2" img-src="https://cdn.quasar.dev/img/parallax1.jpg"/>
        <q-carousel-slide :name="3" img-src="https://cdn.quasar.dev/img/parallax2.jpg"/>
        <q-carousel-slide :name="4" img-src="https://cdn.quasar.dev/img/quasar.jpg"/>
      </q-carousel>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CarouselSection',
  setup () {
    return {
      slide: ref(1)
    }
  }
}
</script>
