<template>
  <DialogBase
    :base-title-text="(!this.bonusRule.id) ? 'Create new bonus rule' : 'Update bonus rule'"
    :primary-button-text="(!this.bonusRule.id) ? 'Create' : 'Update'"
    width="700px"
    @ok="saveBonusRule"
  >
    <div class="q-gutter-y-md q-mt-sm">
      <div class="row">
        <div class="col-12 col-md-6 q-pr-md-sm">
          <MoneyInput
            label="Base bonus amount"
            v-model:money-value="formData.base_bonus_amount"
            v-model:currency-name="formData.bonus_currency"
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
              <CustomTooltip>
                The number of days required for a new hire to work after which time
                the referring employee will be eligible to receive the referral bonus.
              </CustomTooltip>
            </template>
          </q-input>
        </div>
      </div>
      <CriteriaSection :form-data="formData.inclusion_criteria" :is-inclusion="true"/>
      <CriteriaSection :form-data="formData.exclusion_criteria" :is-inclusion="false"/>
      <div class="row q-gutter-y-sm">
        <div class="col-12">
          <SeparatorWithText>
            <q-btn color="primary" @click="addBonusRuleModifier">
              <q-icon name="add"/>
              Add bonus modifier
              <CustomTooltip icon_color_class="text-white" icon_size="24px" :is_include_space="true">
                Bonus modifiers are used to increase the bonus amount based on a time period
                after the job is posted. This can be used to increase employee referrals for
                hard to fill jobs.
              </CustomTooltip>
            </q-btn>
          </SeparatorWithText>
        </div>
        <div class="col-12 q-gutter-y-md">
          <q-list separator>
            <q-item v-for="(modifier, idx) in formData.modifiers">
              <template v-if="modifier.isSelected">
                <q-item-section class="q-gutter-y-md">
                  <q-select
                    filled emit-value map-options
                    label="Modifier type"
                    :options="[
                    { val: MODIFIER_TYPES.NOMINAL, label: 'Dollar increase' },
                    { val: MODIFIER_TYPES.PERCENT, label: 'Percent increase' }
                  ]"
                    v-model="modifier.type"
                    option-label="label"
                    option-value="val"
                  />
                  <MoneyInput
                    v-if="modifier.type === MODIFIER_TYPES.NOMINAL"
                    :is-include-currency-selection="false"
                    v-model:money-value="modifier.amount"
                    v-model:currency-name="formData.bonus_currency"
                    label="Increase amount"
                  >
                    <template v-slot:after>
                      <CustomTooltip>
                        The dollar amount increase from the base bonus amount. The currency denomination
                        is based on the denomination from the base bonus amount.
                      </CustomTooltip>
                    </template>
                  </MoneyInput>
                  <q-input
                    v-else
                    filled
                    v-model.number="modifier.amount"
                    mask="#%" fill-mask="0"
                    unmasked-value reverse-fill-mask
                    label="Increase %"
                  >
                    <template v-slot:after>
                      <CustomTooltip>
                        The percentage amount increase from the base bonus amount
                      </CustomTooltip>
                    </template>
                  </q-input>
                  <q-input
                    v-model.number="modifier.start_days_after_post"
                    label="Effective days after post"
                    type="number"
                    filled
                  >
                    <template v-slot:after>
                      <CustomTooltip>
                        The number of days after the job is posted at which time the bonus
                        modifier takes effect.
                      </CustomTooltip>
                    </template>
                  </q-input>
                </q-item-section>
                <q-item-section avatar top>
                  <q-btn
                    title="confirm" dense ripple flat padding="4px"
                    class="bg-positive q-mb-sm" icon="check"
                    @click="confirmBonusRuleModifier(modifier)"
                  />
                  <q-btn
                    title="delete" dense ripple flat padding="4px"
                    class="bg-negative" icon="delete"
                    @click="removeBonusRuleModifier(idx)"
                  />
                </q-item-section>
              </template>
              <template v-else>
                <q-item-section>
                  <div v-html="bonusUtil.getModifierSummaryHtml(
                    modifier, formData.base_bonus_amount, formData.bonus_currency
                    )"/>
                </q-item-section>
                <q-item-section avatar>
                  <q-btn
                    title="edit" dense ripple flat padding="4px"
                    class="bg-grey-4" icon="edit"
                    @click="modifier.isSelected = true"
                  />
                </q-item-section>
              </template>
            </q-item>
          </q-list>
        </div>
      </div>
    </div>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import CriteriaSection from 'components/dialogs/dialog-bonus-rule/CriteriaSection.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SeparatorWithText from 'components/SeparatorWithText.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import bonusUtil, { MODIFIER_TYPES } from 'src/utils/bonus.js'
import dataUtil from 'src/utils/data.js'
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

const bonusRuleModifierTemplate = {
  type: MODIFIER_TYPES.NOMINAL,
  amount: 0,
  start_days_after_post: 30,
  isSelected: true
}

export default {
  name: 'DialogBonusRule',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CustomTooltip, CriteriaSection, MoneyInput, DialogBase, SeparatorWithText },
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
        bonus_currency: 'USD',
        inclusion_criteria: {},
        exclusion_criteria: {},
        modifiers: []
      },
      bonusUtil,
      MODIFIER_TYPES
    }
  },
  methods: {
    addBonusRuleModifier () {
      this.formData.modifiers.push(dataUtil.deepCopy(bonusRuleModifierTemplate))
      dataUtil.sortBy(this.formData.modifiers, 'start_days_after_post', true)
    },
    confirmBonusRuleModifier (modifier) {
      modifier.isSelected = false
      dataUtil.sortBy(this.formData.modifiers, 'start_days_after_post', true)
    },
    removeBonusRuleModifier (modifierIdx) {
      dataUtil.removeItemFromList(this.formData.modifiers, { listIdx: modifierIdx })
    },
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
      await this.employerStore.setEmployerJobs(this.user.employer_id, true)
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
  },
  mounted () {
    Object.assign(this.formData, dataUtil.deepCopy(this.bonusRule))
    this.formData.bonus_currency = this.formData.bonus_currency.name
  }
}
</script>
