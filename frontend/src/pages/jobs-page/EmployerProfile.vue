<template>
  <div v-if="isLoaded" class="scroll q-mt-md">
    <q-page-sticky position="top" :offset="[0, 10]">
      <q-btn-group rounded>
        <template v-for="(section, idx) in sections">
          <q-btn v-if="section.header" color="primary" rounded :label="section.header" @click="scrollToEl(idx)"/>
        </template>
      </q-btn-group>
    </q-page-sticky>
    <div v-for="(section, idx) in sections" class="q-mb-xl q-py-md">
      <SectionHeader :section="section" :section-idx="idx" :is-include-el-id="true"/>
      <div v-if="section.type === SECTION_TYPES.TEXT.key" v-html="section.item_parts[0].html_content"/>
      <AccordionSection
        v-if="section.type === SECTION_TYPES.ACCORDION.key"
        :section="section"
      />
      <CarouselSection
        v-if="section.type === SECTION_TYPES.CAROUSEL.key"
        :picture-ids="section.item_parts[0].picture_ids"
        :is-allow-autoplay="section.item_parts[0].is_allow_autoplay"
      />
      <IconSection
        v-if="section.type === SECTION_TYPES.ICON.key"
        :section="section"
      />
    </div>
  </div>
</template>

<script>
import SectionHeader from 'components/sections/SectionHeader.vue'
import { SECTION_TYPES } from 'components/sections/sectionTypes.js'
import { storeToRefs } from 'pinia/dist/pinia'
import scrollUtil from 'src/utils/scroll.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import AccordionSection from 'components/sections/AccordionSection.vue'
import CarouselSection from 'components/sections/CarouselSection.vue'
import IconSection from 'components/sections/IconSection.vue'

export default {
  name: 'EmployerProfile',
  components: { SectionHeader, AccordionSection, CarouselSection, IconSection },
  data () {
    return {
      tab: 'tab-0',
      isLoaded: false,
      SECTION_TYPES
    }
  },
  computed: {
    employerPage () {
      return this.employerStore.getEmployerPage(this.user.employer_id)
    },
    sections () {
      return (this.employerPage) ? this.employerPage.sections : []
    }
  },
  methods: {
    scrollToEl (sectionIdx) {
      const el = document.getElementById(`employer-${sectionIdx}`)
      scrollUtil.scrollToElement(el)
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployerPage(this.user.employer_id)
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
      user
    }
  }
}
</script>
