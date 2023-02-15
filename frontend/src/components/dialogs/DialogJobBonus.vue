<template>
  <DialogBase
    base-title-text="Update job bonus"
    primary-button-text="Update"
    @ok="saveJobBonus"
  >
    <template v-slot:subTitle>
      <span v-if="jobs.length > 1">{{ dataUtil.pluralize('job', jobs.length) }} selected.</span>
      Adding a referral bonus directly to a job
      will override all referral bonus rules that may apply, including time based modifiers
    </template>
    <div class="q-gutter-y-md q-mt-sm">
      <div class="row">
        <div class="col-12">
          <MoneyInput
            v-model:money-value="formData.referral_bonus"
            v-model:currency-name="formData.referral_bonus_currency"
            label="Referral bonus"
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
        referral_bonus_currency: 'USD'
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
      await this.$api.put('employer/job/bonus/', getAjaxFormData({
        job_ids: this.jobs.map((job) => job.id),
        ...this.formData
      }))
      this.$emit('ok')
    }
  },
  mounted () {
    this.employerStore = useEmployerStore()
    this.authStore = useAuthStore()
    if (this.jobs.length === 1) {
      const job = this.jobs[0]
      this.formData.referral_bonus = job.referral_bonus
      this.formData.referral_bonus_currency = job.referral_bonus_currency?.name
    }
  }
}
</script>
