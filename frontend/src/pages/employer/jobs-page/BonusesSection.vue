<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <q-btn
        label="Add bonus rule"
        color="primary" ripple
        @click="openBonusRuleDialog"
      />
    </div>
    <div v-for="bonusRule in bonusRules" class="col-12">
      <q-card>
        <q-card-section>
          <div class="row">
            <div class="col-5 border-right-1-gray-100 q-pr-sm">
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
            <div class="col-3 border-right-1-gray-100 q-px-sm">
              <div class="text-bold">
                Time modifiers
                <CustomTooltip icon_size="16px" :is_include_space="false">
                  Time modifiers increase the amount of the referral bonus if the job has not been filled within
                  the specified number of days after the job was posted. This only applies to new applications
                  after the specified number of days. If an application was submitted prior to the time modifier,
                  the previous referral bonus will apply.
                </CustomTooltip>
              </div>
              None
            </div>
            <div class="col-2 border-right-1-gray-100 q-px-sm">
              <div class="text-bold text-center">Bonus amount</div>
              <div class="text-h6 text-center">
                {{ dataUtil.formatCurrency(bonusRule.base_bonus_amount, { currency: bonusRule.bonus_currency.name }) }}
              </div>
            </div>
            <div class="col-2 q-px-sm"></div>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBonusRule, { loadDialogBonusRuleFn } from 'components/dialogs/dialog-bonus-rule/DialogBonusRule.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'BonusesSection',
  components: { CustomTooltip },
  data () {
    return {
      dataUtil
    }
  },
  computed: {
    bonusRules () {
      return this.employerStore.getEmployerBonusRules(this.authStore.propUser.employer_id)
    }
  },
  methods: {
    async openBonusRuleDialog (bonusRule) {
      await loadDialogBonusRuleFn()
      return this.q.dialog({
        component: DialogBonusRule,
        componentProps: { bonusRule }
      })
    },
    hasCriteria (criteriaVal) {
      return criteriaVal && criteriaVal.length
    },
    hasAnyCriteria (criteriaObject) {
      for (const criteriaVal of Object.values(criteriaObject)) {
        if (this.hasCriteria(criteriaVal)) {
          return true
        }
      }
      return false
    }
  },
  setup () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const q = useQuasar()

    return { employerStore, authStore, q }
  }
}
</script>
