<template>
  <div v-if="isLoaded" :style="(isHidden) ? 'display: none;' : ''">
    <div class="border-1-gray-100 border-rounded q-mt-md">
      <div class="text-bold bg-gray-300 q-pa-sm border-top-rounded">
        Live view
        <CustomTooltip icon_size="16px" :is_include_space="false">
          This is roughly how the post will look once posted. There will be slight differences based on the social
          platform
          you post to.
        </CustomTooltip>
      </div>
      <div class="q-pa-sm" style="white-space: pre-line;">
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
import { SOCIAL_CONTENT_PLACEHOLDERS } from 'components/dialogs/DialogSocialContent.vue'
import dataUtil from 'src/utils/data.js'
import fileUtil from 'src/utils/file.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'PostLiveView',
  components: { CustomTooltip },
  props: {
    content: [String, null],
    jobLink: [Object, null],
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
      authStore: null,
      employerStore: null,
      socialStore: null,
      user: null,
      jobs: [],
      fileUtil
    }
  },
  computed: {
    employer () {
      if (!this.user) {
        return {}
      }
      return this.employerStore.getEmployer(this.user.employer_id)
    },
    jobTitles () {
      const jobTitles = dataUtil.uniqArray(this.jobs.map((j) => j.job_title))
      jobTitles.sort()
      return jobTitles
    },
    formattedContent () {
      if (!this.content) {
        return ''
      }
      let formattedContent = this.content
        .replaceAll(SOCIAL_CONTENT_PLACEHOLDERS.EMPLOYER, this.employer.name)
      if (this.jobLink) {
        formattedContent = formattedContent
          .replaceAll(SOCIAL_CONTENT_PLACEHOLDERS.JOB_LINK, `${window.location.origin}/jobs-link/${this.jobLink.id}`)
          .replaceAll(SOCIAL_CONTENT_PLACEHOLDERS.JOBS_LIST, this.jobTitles.map((j) => `- ${j}`).join('\n'))
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
    jobLink () {
      this.setJobsFromLink()
    },
    formattedContent () {
      this.$emit('content-update', this.formattedContent)
    }
  },
  methods: {
    async setJobsFromLink () {
      if (!this.jobLink) {
        this.jobs = []
        return
      }
      const resp = await this.$api.get(`social-link-jobs/${this.jobLink.id}`)
      this.jobs = resp.data.jobs
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.employerStore = useEmployerStore()
    this.socialStore = useSocialStore()
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployer(this.authStore.propUser.employer_id),
        this.socialStore.setSocialLinkFilters(this.authStore.propUser.id)
      ])
    })
    this.user = this.authStore.propUser
    this.isLoaded = true
  }
}
</script>
