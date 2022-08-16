<template>
  <DialogBase
    base-title-text="Bonus rule"
    :is-include-buttons="false"
  >
    <div class="q-gutter-y-md">
      <table class="table q-table q-table--bordered q-table--horizontal-separator">
        <tbody>
          <tr>
            <td class="text-bold bg-grey-3" style="min-width: 150px;">Bonus amount</td>
            <td>
              {{ dataUtil.formatCurrency(bonusRule.base_bonus_amount, { currency: bonusRule.bonus_currency.name }) }}
            </td>
          </tr>
          <tr>
            <td class="text-bold bg-grey-3">Inclusion criteria</td>
            <td>
              <template v-for="(criteriaVal, criteriaKey) in bonusRule.inclusion_criteria">
                <div v-if="bonusUtil.hasCriteria(criteriaVal)">
                  <span v-if="criteriaKey !== 'job_titles_regex'">
                    {{ dataUtil.capitalize(criteriaKey) }}: {{ criteriaVal.map(v => v.name).join(', ') }}
                  </span>
                  <span v-else>
                    Job titles matching: {{ criteriaVal }}
                  </span>
                </div>
              </template>
            </td>
          </tr>
          <tr>
            <td class="text-bold bg-grey-3">Exclusion criteria</td>
            <td>
              <template v-for="(criteriaVal, criteriaKey) in bonusRule.exclusion_criteria">
                <div v-if="bonusUtil.hasCriteria(criteriaVal)">
                  <span v-if="criteriaKey !== 'job_titles_regex'">
                    {{ dataUtil.capitalize(criteriaKey) }}: {{ criteriaVal.map(v => v.name).join(', ') }}
                  </span>
                  <span v-else>
                    Job titles matching: {{ criteriaVal }}
                  </span>
                </div>
              </template>
            </td>
          </tr>
          <tr>
            <td class="text-bold bg-grey-3">Time modifiers</td>
            <td>
              <ul v-if="bonusRule.modifiers.length">
                <li v-for="modifier in bonusRule.modifiers">
                  <span v-html="bonusUtil.getModifierSummaryHtml(
                      modifier,
                      bonusRule.base_bonus_amount,
                      bonusRule?.bonus_currency?.name
                    )"
                  />
                </li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import bonusUtil from 'src/utils/bonus.js'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'DialogShowBonusRule',
  components: { DialogBase },
  props: {
    bonusRule: Object
  },
  data () {
    return {
      bonusUtil,
      dataUtil
    }
  }
}
</script>
