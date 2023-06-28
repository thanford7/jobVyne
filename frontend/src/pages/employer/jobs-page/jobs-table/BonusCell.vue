<template>
  <span v-if="props.row.bonus">
    {{ dataUtil.formatCurrency(props.row.bonus.amount, { currency: props.row.bonus.currency.name }) }}
  </span>
  <span v-else>None</span>
</template>

<script>
import dataUtil from 'src/utils/data.js'

export default {
  name: 'BonusCell',
  props: {
    props: Object
  },
  data () {
    return {
      dataUtil
    }
  }
}
</script>
