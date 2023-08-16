<template>
  <DialogBase
    :base-title-text="`Job details: ${job.job_title}`"
    :is-include-buttons="false"
    width="700px"
  >
    <q-btn-toggle
      v-if="jobSections?.length > 1"
      v-model="showSection"
      toggle-color="grey-7"
      class="q-mb-md border-1-gray-300"
      :options="jobSections"
      spread size="md" ripple
    />
    <div v-if="isHtml" v-html="sectionValue"/>
    <div v-else-if="isText">
      {{ sectionValue }}
    </div>
    <div v-else>
      <ul>
        <li v-for="val in sectionValue">
          {{ dataUtil.capitalize(val) }}
        </li>
      </ul>
    </div>
  </DialogBase>
</template>
<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import dataUtil from 'src/utils/data.js'

const JOB_SECTION_REQUIREMENTS = 'responsibilities'
const JOB_SECTION_QUALIFICATIONS = 'qualifications'
const JOB_SECTION_TECH_QUALIFICATIONS = 'technical_qualifications'
const JOB_DESCRIPTION_SUMMARY = 'job_description_summary'
const JOB_DESCRIPTION = 'job_description'

const JOB_SECTIONS = [
  { value: JOB_SECTION_REQUIREMENTS, label: 'Requirements' },
  { value: JOB_SECTION_QUALIFICATIONS, label: 'Qualifications' },
  { value: JOB_SECTION_TECH_QUALIFICATIONS, label: 'Technical qualifications' },
  { value: JOB_DESCRIPTION_SUMMARY, label: 'Short job description' },
  { value: JOB_DESCRIPTION, label: 'Full job description' }
]

export default {
  name: 'DialogJobRequirements',
  components: { DialogBase },
  props: {
    job: Object
  },
  data () {
    const jobSections = JOB_SECTIONS.filter((section) => section.value === JOB_DESCRIPTION || this.job[section.value]?.length)
    return {
      showSection: jobSections[0].value,
      jobSections,
      dataUtil
    }
  },
  computed: {
    sectionValue () {
      return this.job[this.showSection]
    },
    isHtml () {
      return this.showSection === JOB_DESCRIPTION
    },
    isText () {
      return this.showSection === JOB_DESCRIPTION_SUMMARY
    }
  }
}
</script>
