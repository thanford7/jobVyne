<template>
  <div v-if="isLoaded" class="scroll">
    <q-page-sticky position="top" :offset="[0, 10]">
      <q-btn-group rounded>
        <template v-for="(section, idx) in sections">
          <q-btn
            v-if="section.header"
            rounded
            :label="section.header"
            :style="getNavStyle()"
            @click="scrollToEl(idx)"
          />
        </template>
      </q-btn-group>
    </q-page-sticky>
    <div
      v-for="(section, idx) in sections"
      class="row justify-center q-px-xl"
      :class="(idx === 0) ? 'q-pt-lg' : ''"
      :style="sectionUtil.getBackgroundStyle(section)"
    >
      <ResponsiveWidth class="q-pb-xl" :is-small="true">
        <SectionHeader
          :section="section"
          :section-idx="idx"
          :is-include-el-id="true"
          class="q-pt-xl"
        />
        <TextSection
          v-if="section.type === SECTION_TYPES.TEXT.key"
          :section="section"
          :employer-id="employerId"
        />
        <AccordionSection
          v-if="section.type === SECTION_TYPES.ACCORDION.key"
          :section="section"
        />
        <CarouselSection
          v-if="section.type === SECTION_TYPES.CAROUSEL.key"
          :picture-ids="section.item_parts[0].picture_ids"
          :is-allow-autoplay="section.item_parts[0].is_allow_autoplay"
          :employer-id="employerId"
        />
        <IconSection
          v-if="section.type === SECTION_TYPES.ICON.key"
          :section="section"
        />
      </ResponsiveWidth>
    </div>
  </div>
</template>

<script>
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import SectionHeader from 'components/sections/SectionHeader.vue'
import sectionUtil, { SECTION_TYPES } from 'components/sections/sectionTypes.js'
import TextSection from 'components/sections/TextSection.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import colorUtil from 'src/utils/color.js'
import scrollUtil from 'src/utils/scroll.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import AccordionSection from 'components/sections/AccordionSection.vue'
import CarouselSection from 'components/sections/CarouselSection.vue'
import IconSection from 'components/sections/IconSection.vue'

export default {
  name: 'EmployerProfile',
  components: { ResponsiveWidth, TextSection, SectionHeader, AccordionSection, CarouselSection, IconSection },
  props: {
    employerId: Number
  },
  data () {
    return {
      tab: 'tab-0',
      isLoaded: false,
      employer: null,
      employerPage: null,
      sections: null,
      sectionUtil,
      SECTION_TYPES
    }
  },
  methods: {
    getNavStyle () {
      const primaryColor = this.employer.color_primary
      const backgroundColor = primaryColor || colorUtil.getPaletteColor('primary')
      const color = colorUtil.getInvertedColor(backgroundColor)
      return { backgroundColor, color }
    },
    scrollToEl (sectionIdx) {
      const el = document.getElementById(`employer-${sectionIdx}`)
      scrollUtil.scrollToElement(el)
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployer(this.employerId),
        this.employerStore.setEmployerPage(this.employerId)
      ])
    })
    this.employer = this.employerStore.getEmployer(this.employerId)
    this.employerPage = this.employerStore.getEmployerPage(this.employerId)
    this.sections = this.employerPage.sections
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
