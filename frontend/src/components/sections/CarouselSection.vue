<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <q-carousel
        swipeable padding animated thumbnails infinite
        :autoplay="isAllowAutoplay && autoplay"
        transition-prev="slide-right"
        transition-next="slide-left"
        @mouseenter="autoplay = false"
        @mouseleave="autoplay = true"
        v-model="slide"
        class="q-carousel--no-stretch"
      >
        <q-carousel-slide
          v-for="(picture, idx) in pictures"
          :name="idx + 1"
          :img-src="picture.url"
        />
      </q-carousel>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CarouselSection',
  props: {
    pictures: {
      type: [Array, null],
      default: () => []
    },
    isAllowAutoplay: {
      type: Boolean,
      default: false
    }
  },
  setup () {
    return {
      slide: ref(1),
      autoplay: ref(true)
    }
  }
}
</script>
