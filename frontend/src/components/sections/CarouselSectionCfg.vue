<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div v-if="isLoaded">
    <SelectFiles
      :file-type-keys="[FILE_TYPES.IMAGE.key]"
      :is-emit-id-only="true"
      :is-employer="true"
      :is-multi-select="true"
      v-model:employer-file-ids="section.item_parts[0].picture_ids"
    />
    <q-toggle
      v-model="section.item_parts[0].is_allow_autoplay"
      label="Auto-scroll"
    >
      <CustomTooltip :is_include_space="true">
        When on, pictures will automatically scroll from one to the next
      </CustomTooltip>
    </q-toggle>
    <LiveView :section="section">
      <SectionHeader :section="section"/>
      <CarouselSection
        :picture-ids="section.item_parts[0].picture_ids"
        :is-allow-autoplay="section.item_parts[0].is_allow_autoplay"
        :employer-id="user.employer_id"
      />
    </LiveView>
  </div>
</template>

<script>
import CarouselSection from 'components/sections/CarouselSection.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectFiles from 'components/inputs/SelectFiles.vue'
import LiveView from 'components/sections/LiveView.vue'
import SectionHeader from 'components/sections/SectionHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { FILE_TYPES } from 'src/utils/file'
import { useAuthStore } from 'stores/auth-store'
import { useEmployerStore } from 'stores/employer-store'
import { useQuasar } from 'quasar'

export default {
  name: 'CarouselSectionCfg',
  components: { SectionHeader, CarouselSection, CustomTooltip, SelectFiles, LiveView },
  props: {
    section: Object,
    sectionIdx: Number
  },
  data () {
    return {
      isLoaded: false,
      FILE_TYPES
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployerFiles(this.user.employer_id)
      ])
    })
    this.isLoaded = true
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      authStore,
      employerStore: useEmployerStore(),
      q: useQuasar(),
      user
    }
  }
}
</script>
