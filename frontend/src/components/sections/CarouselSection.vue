<template>
  <div class="row q-gutter-y-md">
    <div v-if="isLoaded" class="col-12">
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
import dataUtil from 'src/utils/data.js'
import { ref } from 'vue'
import { useEmployerStore } from 'stores/employer-store'

export default {
  name: 'CarouselSection',
  props: {
    pictureIds: {
      type: [Array, null],
      default: () => []
    },
    isAllowAutoplay: {
      type: Boolean,
      default: false
    },
    employerId: {
      type: Number
    }
  },
  computed: {
    pictures () {
      const files = this.employerStore.getEmployerFiles(this.employerId)
      const pictureIds = dataUtil.getForceArray(this.pictureIds)
      return files.filter((f) => pictureIds.includes(f.id))
    }
  },
  async mounted () {
    await this.employerStore.setEmployerFiles(this.employerId)
    this.isLoaded = true
  },
  setup () {
    return {
      slide: ref(1),
      autoplay: ref(true),
      isLoaded: ref(false),
      employerStore: useEmployerStore()
    }
  }
}
</script>
