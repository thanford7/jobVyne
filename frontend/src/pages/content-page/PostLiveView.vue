<template>
  <div v-if="isLoaded" :style="(isHidden) ? 'display: none;' : ''">
    <div class="border-1-gray-100 border-rounded q-mt-md">
      <div class="text-bold bg-gray-300 q-pa-sm border-top-rounded">
        Live view
        <CustomTooltip icon_size="16px">
          This is approximately how the post will look once posted. There will be slight differences based on the social
          platform you post to.
        </CustomTooltip>
      </div>
      <div class="q-pa-sm" style="white-space: pre-line; max-height: 250px; overflow-x: scroll">
        <span v-if="formattedContent.length">
          {{ formattedContent }}
        </span>
        <span v-else class="text-gray-500">
          Add content to see live view...
        </span>
        <div v-if="file" class="q-mt-lg">
          <img
            v-if="fileUtil.isImage(file.url)"
            :src="file.url" :alt="file.title"
            style="width: 30%;"
          >
          <video
            v-if="fileUtil.isVideo(file.url)"
            style="width: 30%;"
          >
            <source :src="file.url">
          </video>
        </div>
      </div>
    </div>
    <div class="text-small text-gray-500 q-pl-sm q-pt-xs" :class="(isCharacterLimitExceeded) ? 'text-negative' : ''">
      <q-icon v-if="isCharacterLimitExceeded" name="dangerous"/>
      {{ characterLengthText }}
      <span v-if="maxCharCount"> of {{ maxCharCount }} limit</span>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data.js'
import emailUtil from 'src/utils/email.js'
import fileUtil from 'src/utils/file.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'PostLiveView',
  components: { CustomTooltip },
  props: {
    isEmployer: Boolean,
    socialLink: [Object, null],
    content: [String, null],
    file: [Object, null],
    maxCharCount: [Number, null],
    isHidden: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      employer: null,
      user: null,
      jobs: [],
      socialStore: null,
      fileUtil
    }
  },
  computed: {
    formattedContent () {
      if (!this.content) {
        return ''
      }
      let formattedContent = this.content
        .replaceAll(emailUtil.PLACEHOLDER_EMPLOYER_NAME.placeholder, this.employer?.name)
      if (this.socialLink) {
        const formattedJobs = this.jobs.map((j) => `🏢 Employer: ${j.employer_name}\n💼 Job: ${j.job_title}\n📍 Locations: ${j.locations_text}\n💰 Salary: ${j.salary_text}\n🔗 Apply: ${this.socialLink.url}`).join('\n\n')

        formattedContent = formattedContent
          .replaceAll(emailUtil.PLACEHOLDER_JOB_LINK.placeholder, this.socialLink.url)
          .replaceAll(emailUtil.PLACEHOLDER_JOBS_LIST.placeholder, formattedJobs)
      }
      return formattedContent
    },
    characterLengthText () {
      const charLength = this.formattedContent.length
      return `${dataUtil.pluralize('character', charLength)}`
    },
    isCharacterLimitExceeded () {
      if (!this.maxCharCount) {
        return false
      }
      return this.formattedContent.length > this.maxCharCount
    }
  },
  watch: {
    socialLink () {
      this.setJobsFromLink(false)
    },
    formattedContent () {
      this.$emit('content-update', this.formattedContent)
    }
  },
  methods: {
    async setJobsFromLink (isForceRefresh) {
      if (!this.socialLink) {
        return
      }
      const params = (this.isEmployer) ? { employerId: this.user.employer_id } : { userId: this.user.id }
      params.isForceRefresh = isForceRefresh
      params.socialLinkId = this.socialLink.id
      params.socialChannel = socialUtil.SOCIAL_CHANNEL_LINKEDIN_JOB // The channel doesn't matter since this is just showing an example
      await this.socialStore.setSocialLinkPostJobs(params)
      this.jobs = this.socialStore.getSocialLinkPostJobs(params)
    }
  },
  async mounted () {
    const { user } = storeToRefs(useAuthStore())
    const employerStore = useEmployerStore()
    this.socialStore = useSocialStore()
    await employerStore.setEmployer(user.employer_id)
    this.employer = employerStore.getEmployer(user.employer_id)
    this.user = user
    await this.setJobsFromLink(false)
    this.isLoaded = true
  }
}
</script>
