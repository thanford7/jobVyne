<template>
  <DialogBase
    base-title-text="Create job board"
    primary-button-text="Save"
    :is-valid-form-fn="isValidForm"
    @ok="saveLink"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12 q-gutter-y-sm">
          <q-input
            v-model="linkName" label="Job board name"
            hint="30 characters max"
            autofocus filled lazy-rules
            :rules="[
                (val) => (val && val.length) || 'Job board name is required',
                (val) => (val && val.length <= 30) || 'Max length is 30 characters'
              ]"
          />
          <SelectJobSubscription v-if="!isEmployerOrgType" v-model="jobSubscriptions" :is-employer="isEmployer"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import SelectJobSubscription from 'components/inputs/SelectJobSubscription.vue'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import employerTypeUtil from 'src/utils/employer-types.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useJobSubscriptionStore } from 'stores/job-subscription-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'DialogJobLink',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    SelectJobSubscription,
    DialogBase
  },
  props: {
    jobLink: [Object, null],
    employerId: Number
  },
  data () {
    return {
      isEmployerOrgType: false,
      linkName: null,
      jobSubscriptions: [],
      filteredJobs: [],
      user: null,
      socialStore: null,
      dataUtil
    }
  },
  computed: {
    isEmployer () {
      return Boolean(this.employerId)
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveLink () {
      const data = Object.assign({}, this.linkFilters, {
        employer_id: this.employerId,
        link_name: this.linkName,
        job_subscriptions: this.jobSubscriptions
      })
      if (!this.employerId) {
        data.owner_id = this.user.id
      }
      let requestMethod = this.$api.post
      if (this?.jobLink?.id) {
        requestMethod = this.$api.put
        data.link_filter_id = this.jobLink.id
      }
      await requestMethod('social-link/', getAjaxFormData(data))
      const params = (this.employerId) ? { employerId: this.employerId } : { userId: this.user.id }
      await this.socialStore.setSocialLinks({ ...params, isForceRefresh: true })
      this.$emit('ok')
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    await authStore.setUser()
    const { user } = storeToRefs(authStore)
    this.user = user
    this.socialStore = useSocialStore()
    if (this.employerId) {
      const employerStore = useEmployerStore()
      await employerStore.setEmployer(this.employerId)
      const employer = employerStore.getEmployer(this.employerId)
      if (employerTypeUtil.isTypeEmployer(employer.organization_type)) {
        this.isEmployerOrgType = true
        const jobSubscriptionStore = useJobSubscriptionStore()
        const params = { employerId: this.user.employer_id }
        await jobSubscriptionStore.setJobSubscription(params)
        const jobSubscriptions = jobSubscriptionStore.getJobSubscription(params)
        const employerSubscription = jobSubscriptions.filter((js) => js.is_single_employer).map((js) => js.id)
        if (!this.jobLink) {
          this.jobSubscriptions = employerSubscription
        }
      }
    }
    if (this.jobLink) {
      this.linkName = this.jobLink.link_name
      this.jobSubscriptions = this.jobLink.job_subscriptions
    }
  }
}
</script>
