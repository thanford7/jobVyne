<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div v-if="isLoaded">
    <EmployerFilesSelector
      :ref="`employerFilesSelector-${sectionIdx}`"
      :file-type-keys="[FILE_TYPES.IMAGE.key]"
      :is-emit-id-only="true"
      v-model="section.item_parts[0].picture_ids"
    >
      <template v-slot:after>
        <q-btn
          unelevated ripple color="primary"
          class="h-100"
          @click="openEmployerFileModal(sectionIdx)"
        >Add new image
        </q-btn>
      </template>
    </EmployerFilesSelector>
    <q-toggle
      v-model="section.item_parts[0].is_allow_autoplay"
      label="Auto-scroll"
    >
      <CustomTooltip>
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
import EmployerFilesSelector from 'components/inputs/EmployerFilesSelector.vue'
import LiveView from 'components/sections/LiveView.vue'
import SectionHeader from 'components/sections/SectionHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { FILE_TYPES } from 'src/utils/file'
import DialogEmployerFile, { loadDialogEmployerFileDataFn } from 'components/dialogs/DialogEmployerFile.vue'
import { useAuthStore } from 'stores/auth-store'
import { useEmployerStore } from 'stores/employer-store'
import { useQuasar } from 'quasar'

export default {
  name: 'CarouselSectionCfg',
  components: { SectionHeader, CarouselSection, CustomTooltip, EmployerFilesSelector, LiveView },
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
  methods: {
    async openEmployerFileModal (sectionIdx) {
      await loadDialogEmployerFileDataFn()
      const cfg = {
        component: DialogEmployerFile,
        componentProps: { fileTypeKeys: [FILE_TYPES.IMAGE.key] }
      }
      return this.q.dialog(cfg).onOk((pictureId) => {
        const pictureFile = this.employerStore.getEmployerFiles(
          this.user.employer_id, pictureId
        )
        const refKey = `employerFilesSelector-${sectionIdx}`
        this.$refs[refKey].addFile(pictureFile)
      })
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
