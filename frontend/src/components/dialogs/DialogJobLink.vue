<template>
  <DialogBase
    :base-title-text="`Create job ${(isJobBoard) ? 'board' : 'link'}`"
    primary-button-text="Save"
    :is-valid-form-fn="isValidForm"
    @ok="saveLink"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12 q-gutter-y-sm">
          <template v-if="isJobBoard">
            <q-input
              v-model="linkName" label="Job board name"
              hint="30 characters max"
              filled lazy-rules
              :rules="[
                (val) => (val && val.length) || 'Job board name is required',
                (val) => (val && val.length <= 30) || 'Max length is 30 characters'
              ]"
            />
            <SelectLinkTag v-model="linkTags" :is-employer-mode="true" label="Job board tags"/>
          </template>
          <template v-if="!isJobBoard">
            <div class="text-bold">
              Job link filters
            </div>
            <div>
              <a :href="jobsExampleUrl" target="_blank" class="no-decoration">
                <span class="text-gray-3">
                  <q-icon name="launch"/>&nbsp;
                </span>
                View {{ dataUtil.pluralize('job', filteredJobs.length) }}
              </a>
            </div>
            <SelectJobDepartment v-model="linkFilters.department_ids" :is-emit-id="true"/>
            <SelectJobCity v-model="linkFilters.city_ids" :is-emit-id="true"/>
            <SelectJobState v-model="linkFilters.state_ids" :is-emit-id="true"/>
            <SelectJobCountry v-model="linkFilters.country_ids" :is-emit-id="true"/>
            <SelectJob v-model="linkFilters.job_ids" :employer-id="employerId"/>
          </template>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectJob from 'components/inputs/SelectJob.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import SelectLinkTag from 'components/inputs/SelectLinkTag.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'DialogJobLink',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    SelectLinkTag,
    DialogBase,
    SelectJobDepartment,
    SelectJobCity,
    SelectJobState,
    SelectJobCountry,
    SelectJob
  },
  props: {
    jobLink: [Object, null],
    employerId: Number,
    isJobBoard: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      linkName: null,
      linkTags: [],
      linkFilters: {
        department_ids: [],
        city_ids: [],
        state_ids: [],
        country_ids: [],
        job_ids: []
      },
      filteredJobs: [],
      filteredJobsCache: {},
      user: null,
      employerStore: null,
      socialStore: null,
      dataUtil
    }
  },
  computed: {
    jobsExampleUrl () {
      if (!this.user) {
        return ''
      }
      return socialUtil.getJobLinkUrl(
        null, { filters: this.linkFilters, employerId: this.user.employer_id }
      )
    }
  },
  watch: {
    linkFilters: {
      async handler () {
        await this.getFilteredJobs()
      },
      deep: true
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async getFilteredJobs () {
      const params = { employer_id: this.user.employer_id, ...this.linkFilters }
      const cacheKey = JSON.stringify(params)
      const cachedFilteredJobs = this.filteredJobsCache[cacheKey]
      if (cachedFilteredJobs) {
        this.filteredJobs = cachedFilteredJobs
      } else {
        const jobResp = await this.$api.get('employer/job/', { params })
        this.filteredJobs = jobResp.data
        this.filteredJobsCache[cacheKey] = jobResp.data
      }
    },
    async saveLink () {
      const data = Object.assign({}, this.linkFilters, { employer_id: this.user.employer_id })
      if (!this.isJobBoard) {
        data.owner_id = this.user.id
      } else {
        data.link_tags = this.linkTags
        data.link_name = this.linkName
      }
      let requestMethod = this.$api.post
      if (this?.jobLink?.id) {
        requestMethod = this.$api.put
        data.link_filter_id = this.jobLink.id
      }
      await requestMethod('social-link-filter/', getAjaxFormData(data))

      if (!this.isJobBoard) {
        await this.socialStore.setSocialLinkFilters(this.user.id, true)
      } else {
        await this.employerStore.setEmployerSocialLinks(this.user.employer_id, true)
      }
      this.$emit('ok')
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    await authStore.setUser()
    const { user } = storeToRefs(authStore)
    this.user = user
    this.socialStore = useSocialStore()
    this.employerStore = useEmployerStore()
    if (this.jobLink) {
      [
        ['department_ids', 'departments'],
        ['city_ids', 'cities'],
        ['state_ids', 'states'],
        ['country_ids', 'countries'],
        ['job_ids', 'jobs']
      ].forEach(([formKey, linkKey]) => {
        this.linkFilters[formKey] = dataUtil.getForceArray(this.jobLink[linkKey]).map((v) => v.id)
      })
      this.linkTags = dataUtil.getForceArray(this.jobLink.tags).map((tag) => tag.name)
      this.linkName = this.jobLink.link_name
    }
    await this.getFilteredJobs()
  }
}
</script>
