<template>
  <DialogBase
    :base-title-text="titleText"
    :primary-button-text="buttonText"
    @ok="saveLink"
  >
    <div class="q-gutter-y-md">
      <SelectPlatform v-if="!this.platform" v-model="formData.platform"/>
      <div>
        <span class="text-bold">Job filters</span>
        <CustomTooltip icon_size="16px">
          Leave blank if you wish to display all jobs. Keep in mind that your link will perform better if the
          filtered jobs are relevant to your connections/audience
        </CustomTooltip>
        <div class="text-small">{{dataUtil.pluralize('job', filteredJobsCount)}} match the current filters</div>
      </div>
      <SelectJobDepartment v-model="formData.departments"/>
      <SelectJobCity v-model="formData.cities"/>
      <SelectJobState v-model="formData.states"/>
      <SelectJobCountry v-model="formData.countries"/>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import SelectPlatform from 'components/inputs/SelectPlatform.vue'
import dataUtil from 'src/utils/data.js'
import jobsUtil from 'src/utils/jobs.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'

export const loadDialogSocialLinkFn = () => {
  const authStore = useAuthStore()
  const employerStore = useEmployerStore()
  return authStore.setUser().then(() => {
    return Promise.all([
      employerStore.setEmployer(authStore.propUser.employer_id),
      employerStore.setEmployerJobs(authStore.propUser.employer_id)
    ])
  })
}

export default {
  name: 'DialogSocialLink',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase, SelectPlatform, SelectJobDepartment, SelectJobCity, SelectJobState, SelectJobCountry },
  props: {
    socialLink: [Object, null],
    platform: [Object, null]
  },
  data () {
    return {
      formData: {},
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      socialStore: useSocialStore(),
      dataUtil
    }
  },
  computed: {
    buttonText () {
      return (!this.formData.id) ? 'Create' : 'Update'
    },
    titleText () {
      let text = this.buttonText
      if (this.platform) {
        text += ` ${this.platform.name}`
      }
      text += ' social link'
      return text
    },
    jobs () {
      return this.employerStore.getEmployerJobs(this.authStore.propUser.employer_id)
    },
    filteredJobsCount () {
      return jobsUtil.filterJobs(this.formData, this.jobs).length
    }
  },
  watch: {
    socialLink () {
      Object.assign(this.formData, this.socialLink || {})
    }
  },
  methods: {
    async saveLink () {
      const user = this.authStore.propUser
      const data = {
        owner_id: user.id,
        employer_id: user.employer_id,
        platform_id: this.formData?.platform?.id,
        department_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.departments?.map((dept) => dept.id)),
        cities: dataUtil.getArrayWithValuesOrNone(this.formData.cities),
        state_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.states?.map((state) => state.id)),
        country_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.countries?.map((country) => country.id))
      }
      await this.$api.post('social-link-filter/', getAjaxFormData(data))
      await this.socialStore.setSocialLinkFilters(user.id, true)
    }
  },
  mounted () {
    this.formData.platform = this.platform
  }
}
</script>
