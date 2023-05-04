<template>
  <div v-if="isLoaded" class="row q-gutter-y-md" style="min-width: 500px;">
    <div>
      Only one bonus rule applies to each job, even if multiple rules match a specific job. If multiple rules can
      apply to a job, the highest ranked rule applies. You can adjust the rank of the rules by dragging and dropping
      a rule above or below other rules.
    </div>
    <div class="col-12 col-md-6 q-pr-md-sm">
      <MoneyInput
        label="Default bonus amount"
        v-model:money-value="employerBonusDefaults.default_bonus_amount"
        v-model:currency-name="employerBonusDefaults.default_bonus_currency"
        @blur="saveBonusDefaults"
      >
        <template v-slot:after>
          <CustomTooltip>
            This is the bonus amount that will be applied to any job that does not match
            any of the bonus rules listed below.
          </CustomTooltip>
        </template>
      </MoneyInput>
    </div>
    <div class="col-12 col-md-6 q-pl-md-sm">
      <InputDaysAfterHire
        v-model.number="employerBonusDefaults.days_after_hire_payout"
        @blur="saveBonusDefaults"
      />
    </div>
    <div class="col-12">
      <q-btn
        label="Add bonus rule"
        color="primary" ripple
        @click="openBonusRuleDialog"
      />
      <div
        v-if="jobs.filter((j) => !j.bonus_rule).length"
        class="q-mt-sm q-py-xs q-pl-sm"
        :style="{
          backgroundColor: colorUtil.changeAlpha(colorUtil.getPaletteColor('warning'), 0.7),
          borderRadius: '4px'
        }"
      >
        <a href="#" @click="showJobMatches($event)">
          {{ dataUtil.pluralize('job', jobs.filter((j) => !j.bonus_rule).length) }}
        </a>
        without bonus rule
      </div>
    </div>
    <div class="col-12">
      <DroppableItem class="row" @order-change="saveBonusRuleOrder($event)" :items="bonusRules">
        <template v-slot:default="{ items }">
          <DraggableItem v-for="(bonusRule, idx) in items" class="col-12" :item-id="bonusRule.id">
            <q-card class="rule-card q-mb-md">
              <div class="row q-pa-sm bg-grey-3 border-bottom-1-gray-300 items-center">
                <div class="text-bold">
                  Bonus rule #{{ idx + 1 }} |
                  Amount:
                  {{
                    dataUtil.formatCurrency(bonusRule.base_bonus_amount, { currency: bonusRule.bonus_currency.name })
                  }}
                  |
                  Job matches:
                  <a
                    v-if="bonusUtil.getFilteredJobsFromRule(jobs, bonusRule).length"
                    href="#"
                    @click="showJobMatches($event, bonusRule)"
                  >
                    {{ bonusUtil.getFilteredJobsFromRule(jobs, bonusRule).length }}
                  </a>
                  <span v-else>0</span>
                </div>
                <q-space/>
                <div class="rule-btns q-gutter-x-sm">
                  <q-btn
                    title="edit" dense ripple flat padding="4px"
                    class="bg-grey-5" icon="edit"
                    @click="openBonusRuleDialog(bonusRule)"
                  />
                  <q-btn
                    title="copy" dense ripple flat padding="4px"
                    class="bg-grey-5" icon="content_copy"
                    @click="copyBonusRule(bonusRule)"
                  />
                  <q-btn
                    title="delete" dense ripple flat padding="4px"
                    class="bg-negative" icon="delete"
                    @click="deleteBonusRule(bonusRule)"
                  />
                </div>
              </div>
              <q-card-section class="q-pb-sm">
                <div class="row">
                  <div class="col-6 border-right-1-gray-100 q-pr-sm">
                    <template
                      v-if="!hasAnyCriteria(bonusRule.inclusion_criteria) && !hasAnyCriteria(bonusRule.exclusion_criteria)">
                      <div class="text-bold">Applies to all jobs</div>
                    </template>
                    <template v-if="hasAnyCriteria(bonusRule.inclusion_criteria)">
                      <div class="text-bold">Applies to all jobs with:</div>
                      <ul>
                        <template v-for="(criteriaVal, criteriaKey) in bonusRule.inclusion_criteria">
                          <li v-if="hasCriteria(criteriaVal)">
                            <span v-if="criteriaKey !== 'job_titles_regex'">
                              {{ dataUtil.capitalize(criteriaKey) }}: {{ criteriaVal.map(v => v.name).join(', ') }}
                            </span>
                            <span v-else>
                              Job titles matching: {{ criteriaVal }}
                            </span>
                          </li>
                        </template>
                      </ul>
                    </template>
                    <template v-if="hasAnyCriteria(bonusRule.exclusion_criteria)">
                      <div class="text-bold">
                        <span v-if="hasAnyCriteria(bonusRule.inclusion_criteria)">And not with:</span>
                        <span v-else>Applies to all jobs except those with:</span>
                      </div>
                      <ul>
                        <template v-for="(criteriaVal, criteriaKey) in bonusRule.exclusion_criteria">
                          <li v-if="hasCriteria(criteriaVal)">
                      <span v-if="criteriaKey !== 'job_titles_regex'">
                        {{ dataUtil.capitalize(criteriaKey) }}: {{ criteriaVal.map(v => v.name).join(', ') }}
                      </span>
                            <span v-else>
                        Job titles matching: {{ criteriaVal }}
                      </span>
                          </li>
                        </template>
                      </ul>
                    </template>
                  </div>
                  <div class="col-6 q-px-sm">
                    <div class="text-bold">
                      Time modifiers
                      <CustomTooltip icon_size="16px">
                        Time modifiers increase the amount of the referral bonus if the job has not been filled within
                        the specified number of days after the job was posted. This only applies to new applications
                        after the specified number of days. If an application was submitted prior to the time
                        modifier,
                        the previous referral bonus will apply.
                      </CustomTooltip>
                    </div>
                    <ul v-if="bonusRule.modifiers.length">
                      <li v-for="modifier in bonusRule.modifiers">
                        <span
                          v-html="bonusUtil.getModifierSummaryHtml(modifier, bonusRule.base_bonus_amount, bonusRule?.bonus_currency?.name)"/>
                      </li>
                    </ul>
                    <span v-else>None</span>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </DraggableItem>
        </template>
      </DroppableItem>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBonusRule, { loadDialogBonusRuleFn } from 'components/dialogs/dialog-bonus-rule/DialogBonusRule.vue'
import DraggableItem from 'components/drag-drop/DraggableItem.vue'
import DroppableItem from 'components/drag-drop/DroppableItem.vue'
import InputDaysAfterHire from 'components/inputs/InputDaysAfterHire.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import bonusUtil from 'src/utils/bonus.js'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'BonusesSection',
  components: { InputDaysAfterHire, CustomTooltip, DraggableItem, DroppableItem, MoneyInput },
  data () {
    return {
      isLoaded: false,
      bonusUtil,
      colorUtil,
      dataUtil,
      employerBonusDefaults: {}
    }
  },
  computed: {
    bonusRules () {
      return this.employerStore.getEmployerBonusRules(this.user.employer_id)
    },
    jobs () {
      return this.employerStore.getEmployerJobs(this.user.employer_id)
    }
  },
  methods: {
    hasCriteria: bonusUtil.hasCriteria.bind(bonusUtil),
    hasAnyCriteria: bonusUtil.hasAnyCriteria.bind(bonusUtil),
    getEmployerBonusDefaults () {
      const employer = this.employerStore.getEmployer(this.user.employer_id)
      return {
        default_bonus_amount: employer.default_bonus_amount,
        default_bonus_currency: employer.default_bonus_currency?.name,
        days_after_hire_payout: employer.days_after_hire_payout
      }
    },
    showJobMatches (e, bonusRule) {
      e.preventDefault()
      this.$router.push({
        name: this.$route.name,
        params: this.$route.params,
        query: { ruleId: (bonusRule) ? bonusRule.id : -1, tab: 'job' }
      })
    },
    async updateData (isForceRefresh) {
      await this.employerStore.setEmployer(this.user.employer_id, isForceRefresh)
      await this.employerStore.setEmployerBonusRules(this.user.employer_id, isForceRefresh)
      await this.employerStore.setEmployerJobs(this.user.employer_id, { isForceRefresh })
    },
    async copyBonusRule (bonusRule) {
      bonusRule.order_idx = this.employerStore.getEmployerBonusRules(this.user.employer_id).length
      await this.$api.post('employer/bonus/rule/', getAjaxFormData(bonusRule))
      await this.updateData(true)
    },
    async deleteBonusRule (bonusRule) {
      await this.$api.delete(`employer/bonus/rule/${bonusRule.id}/`)
      await this.updateData(true)
    },
    async openBonusRuleDialog (bonusRule) {
      await loadDialogBonusRuleFn()
      return this.q.dialog({
        component: DialogBonusRule,
        componentProps: { bonusRule }
      })
    },
    async saveBonusDefaults () {
      // Do nothing if no data has changed
      if (dataUtil.isDeepEqual(this.getEmployerBonusDefaults(), this.employerBonusDefaults)) {
        return
      }
      await this.$api.put('employer/bonus/default/', getAjaxFormData({
        employer_id: this.user.employer_id,
        ...this.employerBonusDefaults
      }))
      await this.updateData(true)
    },
    async saveBonusRuleOrder (ruleIds) {
      await this.$api.put('employer/bonus/rule/order/', getAjaxFormData({
        employer_id: this.user.employer_id,
        rule_ids: ruleIds
      }))
      await this.updateData(true)
    }
  },
  async mounted () {
    await this.updateData(false)
    this.employerBonusDefaults = this.getEmployerBonusDefaults()
    this.isLoaded = true
  },
  setup () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const q = useQuasar()

    return { employerStore, authStore, q, user }
  }
}
</script>

<style lang="scss" scoped>
.rule-btns {
  visibility: hidden;
}

.rule-card:hover {
  .rule-btns {
    visibility: visible;
  }
}
</style>
