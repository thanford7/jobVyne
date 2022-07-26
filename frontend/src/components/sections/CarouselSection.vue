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
import { ref } from 'vue'
import { useAuthStore } from 'stores/auth-store'
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
    }
  },
  computed: {
    pictures () {
      const files = this.employerStore.getEmployerFiles(this.authStore.propUser.employer_id)
      return files.filter((f) => this.pictureIds.includes(f.id))
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployerFiles(this.authStore.propUser.employer_id)
      ])
    })
    this.isLoaded = true
  },
  setup () {
    return {
      slide: ref(1),
      autoplay: ref(true),
      isLoaded: ref(false),
      authStore: useAuthStore(),
      employerStore: useEmployerStore()
    }
  }
}
</script>
