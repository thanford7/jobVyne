<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Profile page">
        This content is displayed on every jobs page from employee social links.
        <div class="col-12 q-mt-sm">
          <q-btn
            type="a"
            color="primary"
            :to="{ name: 'jobs-link-example', params: { employerId: user.employer_id} }"
            target="_blank"
          >
            <q-icon name="launch"/>
            &nbsp;Live site view
          </q-btn>
          <q-toggle
            v-if="canEdit"
            v-model="isViewable"
            color="primary"
            @update:model-value="savePage"
          >
            Is viewable
            <CustomTooltip :is_include_space="false">
              When off, the employer page will not be shown on any job pages. It is recommended to turn on page viewing
              so job seekers can learn more about your company. Turn off if the page is still a work in progress.
            </CustomTooltip>
          </q-toggle>
        </div>
      </PageHeader>
      <div v-if="canEdit" class="row q-mt-md q-gutter-x-sm">
        <q-btn-dropdown icon="add" label="Add section" color="primary">
          <q-list>
            <q-item
              v-for="section in Object.values(sectionTypes)"
              clickable v-close-popup @click="addSectionItem(section.key)"
            >
              <q-item-section>
                <q-item-label>
                  {{ section.label }}
                </q-item-label>
              </q-item-section>
              <q-item-section avatar>
                <CustomTooltip>
                  <div class="q-mb-sm text-bold">Ideal for:</div>
                  <ul>
                    <li v-for="item in section.usedFor">
                      {{ item }}
                    </li>
                  </ul>
                  <template v-if="section.exampleImagePath">
                    <div class="q-mb-sm text-bold">Example:</div>
                    <div class="flex justify-center">
                      <img :src="section.exampleImagePath" alt="Example for section type" style="max-height: 150px">
                    </div>
                  </template>
                </CustomTooltip>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
        <q-space/>
        <q-btn
          v-if="sections.length && hasSectionsChanged"
          ripple label="Undo" color="grey-6" icon="undo"
          @click="undoChanges"
        />
        <q-btn
          v-if="sections.length && hasSectionsChanged"
          ripple label="Save" color="accent" icon="save"
          @click="savePage"
        />
      </div>
      <div v-if="canEdit" class="row q-mt-md">
        <div v-for="(section, sectionIdx) in sections" class="col-12 border-bottom-1-gray-100 border-top-1-gray-100">
          <q-expansion-item
            group="group-sections"
            expand-separator
            :default-opened="sectionIdx === sections.length - 1"
            :header-class="['bg-grey-7', 'text-white']"
            expand-icon-class="text-white"
          >
            <template v-slot:header>
              <span class="text-h6">{{ section.header || sectionTypes[section.type].label }}</span>
              <q-space/>
              <div class="q-px-sm q-mx-md border-left-1-white border-right-1-white">
                <q-btn
                  v-if="sectionIdx !== 0"
                  flat dense icon="arrow_upward"
                  @click="moveSectionItem(sectionIdx, true)"
                />
                <q-btn
                  v-if="sectionIdx !== sections.length - 1"
                  flat dense icon="arrow_downward"
                  @click="moveSectionItem(sectionIdx, false)"
                />
                <q-btn flat dense icon="delete" text-color="negative" @click="removeSectionItem(sectionIdx)"/>
              </div>
            </template>
            <div class="row q-gutter-y-md q-mt-xs q-mb-md">
              <div class="col-12 q-gutter-y-sm">
                <div class="row">
                  <div class="col-12 col-md-6">
                    <q-input filled v-model="section.header" label="Section header" class="w-100">
                      <template v-slot:append>
                        <CustomTooltip>
                          Optional. When populated the header will be displayed at the top of the section and
                          also included as a link which will scroll to this section when clicked.
                        </CustomTooltip>
                      </template>
                    </q-input>
                  </div>
                </div>
                <div class="row q-gutter-x-sm">
                  <ColorPicker
                    v-model="section.config.background_color"
                    label="Background color"
                    :is-include-employer-colors="true"
                    class="q-pb-sm"
                  />
                  <ColorPicker
                    v-model="section.config.header_color"
                    label="Header color"
                    :is-include-employer-colors="true"
                    class="q-pb-sm"
                  />
                  <ColorPicker
                    v-model="section.config.text_color"
                    label="Text color"
                    :is-include-employer-colors="true"
                    class="q-pb-sm"
                  />
                  <template v-if="section.type === sectionTypes.ACCORDION.key">
                    <ColorPicker
                      v-model="section.config.accordion_background_color"
                      label="Accordion background color"
                      :is-include-employer-colors="true"
                      class="q-pb-sm"
                    />
                    <ColorPicker
                      v-model="section.config.accordion_header_color"
                      label="Accordion header color"
                      :is-include-employer-colors="true"
                      class="q-pb-sm"
                    />
                  </template>
                </div>
              </div>
              <TextSectionCfg
                v-if="section.type === sectionTypes.TEXT.key"
                :section="section"
              />
              <IconSectionCfg
                v-if="section.type === sectionTypes.ICON.key"
                :section="section"
                :section-idx="sectionIdx"
                class="col-12"
                @moveUp="moveSectionPart(sectionIdx, $event, true)"
                @moveDown="moveSectionPart(sectionIdx, $event, false)"
                @remove="removeSectionPart(sectionIdx, $event)"
                @add="addSectionPart(sectionIdx)"
              />
              <CarouselSectionCfg
                v-if="section.type === sectionTypes.CAROUSEL.key"
                :section="section"
                :section-idx="sectionIdx"
                class="col-12"
              />
              <AccordionSectionCfg
                v-if="section.type === sectionTypes.ACCORDION.key"
                :section="section"
                :section-idx="sectionIdx"
                class="col-12"
                @moveUp="moveSectionPart(sectionIdx, $event, true)"
                @moveDown="moveSectionPart(sectionIdx, $event, false)"
                @remove="removeSectionPart(sectionIdx, $event)"
                @add="addSectionPart(sectionIdx)"
              />
            </div>
          </q-expansion-item>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import ColorPicker from 'components/inputs/ColorPicker.vue'
import PageHeader from 'components/PageHeader.vue'
import sectionUtil, { SECTION_TYPES } from 'components/sections/sectionTypes.js'
import TextSectionCfg from 'components/sections/TextSectionCfg.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data'
import IconSectionCfg from 'components/sections/IconSectionCfg.vue'
import { Loading, useMeta } from 'quasar'
import { FILE_TYPES } from 'src/utils/file'
import CustomTooltip from 'components/CustomTooltip.vue'
import { useAuthStore } from 'stores/auth-store'
import { useEmployerStore } from 'stores/employer-store'
import AccordionSectionCfg from 'components/sections/AccordionSectionCfg.vue'
import { getAjaxFormData } from 'src/utils/requests'
import CarouselSectionCfg from 'components/sections/CarouselSectionCfg.vue'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'EmployerProfileCfgPage',
  components: {
    TextSectionCfg,
    ColorPicker,
    CarouselSectionCfg,
    AccordionSectionCfg,
    CustomTooltip,
    IconSectionCfg,
    PageHeader
  },
  computed: {
    canEdit () {
      return this.$route.meta.canEdit
    },
    hasSectionsChanged () {
      return !dataUtil.isDeepEqual(this.currentSections, this.sections)
    }
  },
  data () {
    return {
      // Update this when sections is saved. Used to determine if there have been changes
      isViewable: this.getEmployerPageData().is_viewable || false,
      currentSections: this.getSectionsCopy(),
      sections: this.getSectionsCopy(),
      sectionTypes: SECTION_TYPES,
      FILE_TYPES
    }
  },
  methods: {
    addSectionItem (sectionType) {
      sectionUtil.addSectionItem(this.sections, sectionType)
    },
    removeSectionItem (sectionIdx) {
      dataUtil.removeItemFromList(this.sections, { listIdx: sectionIdx })
    },
    moveSectionItem (sectionIdx, isUp) {
      const newIdx = sectionIdx + ((isUp) ? -1 : 1)
      const section = dataUtil.deepCopy(this.sections[sectionIdx])
      this.removeSectionItem(sectionIdx)
      this.sections.splice(newIdx, 0, section)
    },
    addSectionPart (sectionIdx) {
      const sectionType = this.sections[sectionIdx].type
      this.sections[sectionIdx].item_parts.push(
        dataUtil.deepCopy(this.sectionTypes[sectionType].sectionPartConfig)
      )
    },
    removeSectionPart (sectionIdx, partIdx) {
      dataUtil.removeItemFromList(this.sections[sectionIdx].item_parts, { listIdx: partIdx })
    },
    moveSectionPart (sectionIdx, partIdx, isUp) {
      const newIdx = partIdx + (isUp) ? -1 : 1
      const part = dataUtil.deepCopy(this.sections[sectionIdx].item_parts[partIdx])
      this.removeSectionPart(sectionIdx, partIdx)
      this.sections[sectionIdx].item_parts.splice(newIdx, 0, part)
    },
    getEmployerPageData () {
      return this.employerStore.getEmployerPage(this.user.employer_id) || {}
    },
    getSectionsCopy () {
      const employerPage = this.getEmployerPageData()
      return (dataUtil.isEmptyOrNil(employerPage)) ? [] : dataUtil.deepCopy(employerPage.sections)
    },
    async savePage () {
      const data = {
        is_viewable: this.isViewable,
        sections: this.sections,
        employer_id: this.user.employer_id
      }
      await this.$api.put('employer/page/', getAjaxFormData(data))
      await this.employerStore.setEmployerPage(this.user.employer_id, true)
      this.sections = this.getSectionsCopy()
      this.currentSections = this.getSectionsCopy()
    },
    undoChanges () {
      this.sections = dataUtil.deepCopy(this.currentSections)
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployerPage(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Profile Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore,
      employerStore: useEmployerStore(),
      user
    }
  }
}
</script>

<style scoped>

</style>
