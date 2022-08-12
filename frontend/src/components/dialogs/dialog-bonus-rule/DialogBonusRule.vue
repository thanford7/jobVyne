<template>
  <DialogBase
    :base-title-text="(!this.bonusRule.id) ? 'Create new bonus rule' : 'Update bonus rule'"
    :primary-button-text="(!this.bonusRule.id) ? 'Create' : 'Update'"
    width="700px"
    @ok="saveBonusRule"
  >
    <div class="q-gutter-y-md">
      <MoneyInput
        label="Base bonus amount"
        :default-currency="bonusForm?.bonus_currency?.name"
        v-model="bonusForm.base_bonus_amount"
        @update-currency="bonusForm.bonus_currency = $event"
      />
      <CriteriaSection :form-data="inclusionForm" label="Add inclusion criteria"/>
      <CriteriaSection :form-data="exclusionForm" label="Add exlusion criteria"/>
    </div>
  </DialogBase>
</template>

<script>
import CriteriaSection from 'components/dialogs/dialog-bonus-rule/CriteriaSection.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'

export default {
  name: 'DialogBonusRule',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CriteriaSection, MoneyInput, DialogBase },
  props: {
    bonusRule: {
      type: Object,
      default: () => {
      }
    }
  },
  data () {
    return {
      bonusForm: {
        base_bonus_amount: 0,
        bonus_currency: null
      },
      inclusionForm: {},
      exclusionForm: {}
    }
  },
  methods: {
    saveBonusRule () {
      //
    }
  }
}
</script>
