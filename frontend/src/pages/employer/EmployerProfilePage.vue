<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Profile page">
        This content is displayed on every jobs page from employee social links.
      </PageHeader>
      <div class="row q-mt-md">
        <div class="col-12 col-md-4 col-lg-3">
          <q-btn-dropdown icon="add" label="Add section" color="primary">
            <q-list>
              <q-item
                v-for="section in [
                  {name: sectionTypes.TEXT.label, value: sectionTypes.TEXT.key},
                  {name: sectionTypes.ICON.label, value: sectionTypes.ICON.key},
                  {name: sectionTypes.CAROUSEL.label, value: sectionTypes.CAROUSEL.key},
                  {name: sectionTypes.ACCORDION.label, value: sectionTypes.ACCORDION.key}
                ]"
                clickable v-close-popup @click="addSectionItem(section.value)"
              >
                <q-item-section>
                  <q-item-label>{{ section.name }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </div>
      <div class="row q-mt-md">
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
              <div class="col-12">
                <div class="row">
                  <div class="col-12 col-md-6">
                    <q-input filled v-model="section.header" label="Section header" class="w-100"/>
                  </div>
                </div>
              </div>
              <div v-if="section.type === sectionTypes.TEXT.key" class="col-12">
                <WysiwygEditor
                  v-model="section.section_parts[0].html_content"
                  placeholder="Section text..."
                />
              </div>
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
              <div v-if="section.type === sectionTypes.CAROUSEL.key" class="col-12">
                <div class="row">
                  <div class="col-12">
                    <EmployerFilesSelector
                      :ref="`employerFilesSelector-${sectionIdx}`"
                      :file-type-keys="[FILE_TYPES.IMAGE.key]"
                      v-model="section.section_parts[0].pictures"
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
                      v-model="section.section_parts[0].isAllowAutoplay"
                      label="Auto-scroll"
                    >
                      <CustomTooltip>
                        When on, pictures will automatically scroll from one to the next
                      </CustomTooltip>
                    </q-toggle>
                  </div>
                  <div class="col-12">
                    <LiveView>
                      <CarouselSection
                        :pictures="section.section_parts[0].pictures"
                        :is-allow-autoplay="section.section_parts[0].isAllowAutoplay"
                      />
                    </LiveView>
                  </div>
                </div>
              </div>
            </div>
          </q-expansion-item>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import WysiwygEditor from 'components/section-editors/WysiwygEditor.vue'
import dataUtil from 'src/utils/data'
import IconSectionCfg from 'components/sections/IconSectionCfg.vue'
import LiveView from 'components/sections/LiveView.vue'
import CarouselSection from 'components/sections/CarouselSection.vue'
import DialogEmployerFile, { loadDialogEmployerFileDataFn } from 'components/dialogs/DialogEmployerFile.vue'
import { useQuasar } from 'quasar'
import { FILE_TYPES } from 'src/utils/file'
import CustomTooltip from 'components/CustomTooltip.vue'
import EmployerFilesSelector from 'components/inputs/EmployerFilesSelector.vue'
import { useAuthStore } from 'stores/auth-store'
import { useEmployerStore } from 'stores/employer-store'

export default {
  name: 'EmployerProfilePage',
  components: {
    EmployerFilesSelector,
    CustomTooltip,
    CarouselSection,
    LiveView,
    IconSectionCfg,
    PageHeader,
    WysiwygEditor
  },
  data () {
    return {
      sections: [],
      sectionTypes: {
        TEXT: {
          key: 'TEXT',
          label: 'Text section',
          defaultData: { html_content: '' }
        },
        ICON: {
          key: 'ICON',
          label: 'Icons section',
          defaultData: { header: null, html_content: '', icon: null }
        },
        CAROUSEL: {
          key: 'CAROUSEL',
          label: 'Picture carousel section',
          defaultData: { header: null, pictures: [], isAllowAutoplay: false }
        },
        ACCORDION: {
          key: 'ACCORDION',
          label: 'Accordion list section',
          defaultData: { header: null, html_content: '' }
        }
      },
      FILE_TYPES
    }
  },
  methods: {
    addSectionItem (sectionType) {
      this.sections.push({
        type: sectionType,
        header: null,
        section_parts: [
          dataUtil.deepCopy(this.sectionTypes[sectionType].defaultData)
        ]
      })
    },
    removeSectionItem (sectionIdx) {
      dataUtil.removeItemFromList(this.sections, { listIdx: sectionIdx })
    },
    moveSectionItem (sectionIdx, isUp) {
      const newIdx = sectionIdx + (isUp) ? -1 : 1
      const section = dataUtil.deepCopy(this.sections[sectionIdx])
      this.removeSectionItem(sectionIdx)
      this.sections.splice(newIdx, 0, section)
    },
    addSectionPart (sectionIdx) {
      const sectionType = this.sections[sectionIdx].type
      this.sections[sectionIdx].section_parts.push(
        dataUtil.deepCopy(this.sectionTypes[sectionType].defaultData)
      )
    },
    removeSectionPart (sectionIdx, partIdx) {
      dataUtil.removeItemFromList(this.sections[sectionIdx].section_parts, { listIdx: partIdx })
    },
    moveSectionPart (sectionIdx, partIdx, isUp) {
      const newIdx = partIdx + (isUp) ? -1 : 1
      const part = dataUtil.deepCopy(this.sections[sectionIdx].section_parts[partIdx])
      this.removeSectionPart(sectionIdx, partIdx)
      this.sections[sectionIdx].section_parts.splice(newIdx, 0, part)
    },
    async openEmployerFileModal (sectionIdx) {
      await loadDialogEmployerFileDataFn()
      const cfg = {
        component: DialogEmployerFile,
        componentProps: { fileTypeKeys: [FILE_TYPES.IMAGE.key] }
      }
      return this.q.dialog(cfg).onOk((pictureId) => {
        const pictureFile = this.employerStore.getEmployerFiles(
          this.authStore.propUser.employer_id, pictureId
        )
        const refKey = `employerFilesSelector-${sectionIdx}`
        this.$refs[refKey][0].addFile(pictureFile)
      })
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      q: useQuasar()
    }
  }
}
</script>

<style scoped>

</style>
