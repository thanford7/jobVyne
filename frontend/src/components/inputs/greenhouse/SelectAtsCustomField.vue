<template>
  <q-select
    filled emit-value map-options
    :options="fields"
    option-value="name_key"
    option-label="name"
    :label="label"
    :loading="!isLoaded"
  >
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import dataUtil from 'src/utils/data.js'

export default {
  name: 'SelectAtsCustomField',
  props: {
    ats_id: Number,
    label: String
  },
  data () {
    return {
      isLoaded: false,
      fields: []
    }
  },
  async mounted () {
    const resp = await this.$api.get('ats/custom-fields/', {
      params: { ats_id: this.ats_id }
    })
    this.fields = dataUtil.sortBy(
      dataUtil.uniqBy(resp.data.map((s) => ({ name: s.name, name_key: s.name_key })), 'name_key'),
      'name',
      true)
    this.isLoaded = true
  }
}
</script>
