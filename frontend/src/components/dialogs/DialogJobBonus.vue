<template>
  <DialogBase
    base-title-text="Update job bonus"
    primary-button-text="Update"
    @ok="saveJobBonus"
  >
    <template v-slot:subTitle>
      {{ dataUtil.pluralize('job', jobs.length) }} selected. Adding a referral bonus directly to a job
      will override all referral bonus rules that may apply, including time based modifiers
    </template>
    <div class="q-gutter-y-md q-mt-sm">
      <div class="row">
        <div class="col-12">
          <MoneyInput
            v-model="formData.referral_bonus"
            label="Referral bonus"
            @update-currency="formData.referral_bonus_currency = $event"
          />
        </div>
      </div>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'DialogJobBonus',
  extends: DialogBase,
  inheritAttrs: false,
  components: { MoneyInput, DialogBase },
  props: {
    jobs: Array
  },
  data () {
    return {
      dataUtil,
      formData: {
        referral_bonus: null,
        referral_bonus_currency: null
      }
    }
  },
  computed: {
    titleText () {
      return `Update job bonus (${dataUtil.pluralize('job', this.jobs.length)} selected)`
    }
  },
  methods: {
    async saveJobBonus () {
      await this.$api.put('employer/job/', getAjaxFormData({
        job_ids: this.jobs.map((job) => job.id),
        ...this.formData
      }))
      await this.employerStore.setEmployerJobs(this.authStore.propUser.employer_id, true)
    }
  },
  mounted () {
    this.employerStore = useEmployerStore()
    this.authStore = useAuthStore()
  }
}
</script>
