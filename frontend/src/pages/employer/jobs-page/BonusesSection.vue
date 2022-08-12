<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <q-btn
        label="Add bonus rule"
        color="primary" ripple
        @click="openBonusRuleDialog"
      />
    </div>
  </div>
</template>

<script>
import DialogBonusRule from 'components/dialogs/dialog-bonus-rule/DialogBonusRule.vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'BonusesSection',
  methods: {
    openBonusRuleDialog (bonusRule) {
      return this.q.dialog({
        component: DialogBonusRule,
        componentProps: { bonusRule }
      })
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
