<template>
  <DialogBase
    :base-title-text="title"
    :is-include-buttons="false"
    width="700px"
  >
    <div class="q-pa-md">
      <q-carousel
        v-model="slide"
        transition-prev="slide-right"
        transition-next="slide-left"
        animated
        control-color="primary"
        class="rounded-borders"
      >
        <q-carousel-slide v-for="(imageSrc, idx) in imageSrcs" :name="idx + 1" class="column no-wrap">
          <q-img :src="imageSrc" width="600px" style="max-width: 70vw"/>
        </q-carousel-slide>
      </q-carousel>

      <div class="row justify-center">
        <q-btn-toggle
          v-model="slide"
          :options="btnOptions"
        />
      </div>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogImgCarousel',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase },
  props: {
    title: String,
    imageSrcs: Array
  },
  data () {
    return {
      slide: 1
    }
  },
  computed: {
    btnOptions () {
      return this.imageSrcs.map((_v, idx) => {
        const opt = idx + 1
        return { label: opt, value: opt }
      })
    }
  }
}
</script>
