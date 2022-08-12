<template>
  <DialogBase
    :base-title-text="(!this.bonusRule.id) ? 'Create new bonus rule' : 'Update bonus rule'"
    :primary-button-text="(!this.bonusRule.id) ? 'Create' : 'Update'"
    width="700px"
    @ok="saveBonusRule"
  >
    <div class="q-gutter-y-md">
      <div class="row">
        <div class="col-12 col-md-6 q-pr-md-sm">
          <MoneyInput
            label="Base bonus amount"
            :default-currency="formData?.bonus_currency?.name"
            v-model="formData.base_bonus_amount"
            @update-currency="formData.bonus_currency = $event"
          />
        </div>
        <div class="col-12 col-md-6">
          <q-input
            v-model.number="formData.days_after_hire_payout"
            label="Days after hire payout"
            type="number"
            filled
          >
            <template v-slot:after>
              <CustomTooltip :is_include_space="false">
                The number of days required for a new hire to work after which time
                the referring employee will be eligible to receive the referral bonus.
              </CustomTooltip>
            </template>
          </q-input>
        </div>
      </div>
      <CriteriaSection :form-data="formData.inclusion_criteria" :is-inclusion="true"/>
      <CriteriaSection :form-data="formData.exclusion_criteria" :is-inclusion="false"/>
    </div>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import CriteriaSection from 'components/dialogs/dialog-bonus-rule/CriteriaSection.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export const loadDialogBonusRuleFn = () => {
  const authStore = useAuthStore()
  const employerStore = useEmployerStore()
  const globalStore = useGlobalStore()
  return authStore.setUser().then(() => {
    return Promise.all([
      employerStore.setEmployerBonusRules(authStore.propUser.employer_id),
      globalStore.setCurrencies()
    ])
  })
}

export default {
  name: 'DialogBonusRule',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CustomTooltip, CriteriaSection, MoneyInput, DialogBase },
  props: {
    bonusRule: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      formData: {
        days_after_hire_payout: 90,
        bonus_currency: this.globalStore.currencies.find((c) => c.name === 'USD'),
        inclusion_criteria: {},
        exclusion_criteria: {}
      }
    }
  },
  watch: {
    bonusRule () {
      Object.assign(this.formData, this.bonusRule)
    }
  },
  methods: {
    async saveBonusRule () {
      const orderIdx = this.employerStore.getEmployerBonusRules(this.user.employer_id).length
      const data = Object.assign({ employer_id: this.user.employer_id, order_idx: orderIdx },
        this.formData
      )
      const method = (this.bonusRule.id) ? this.$api.put : this.$api.post
      let url = 'employer/bonus/rule/'
      if (this.bonusRule.id) {
        url = `${url}${this.bonusRule.id}/`
      }
      await method(url, getAjaxFormData(data))
      await this.employerStore.setEmployerBonusRules(this.user.employer_id, true)
      this.$emit('ok')
    }
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      employerStore: useEmployerStore(),
      globalStore: useGlobalStore(),
      user
    }
  }
}
</script>
