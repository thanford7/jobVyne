<template>
  <q-table
    dense flat
    :hide-bottom="true"
    :columns="placeholderTableColumns"
    :rows="placeholders"
  >
    <template v-slot:body-cell-action="props">
      <q-td>
        <q-btn
          unelevated dense label="Add" color="grey-6"
          @click="$emit('addContent', props.row.placeholder)"
        />
      </q-td>
    </template>
  </q-table>
</template>

<script>
export default {
  name: 'EmailPlaceholderTable',
  props: {
    placeholders: Array
  },
  data () {
    return {
      placeholderTableColumns: [
        { name: 'action', field: 'action', align: 'center' },
        { name: 'name', field: 'name', align: 'left', label: 'Name' },
        { name: 'placeholder', field: 'placeholder', align: 'left', label: 'Placeholder' },
        { name: 'example', field: 'example', align: 'left', label: 'Example', style: 'white-space: pre-line;' }
      ]
    }
  }
}
</script>
