<template>
  <DialogBase
    base-title-text="Data"
    :is-include-buttons="false"
    width="800px"
  >
    <q-table
      flat
      :rows="data"
      :columns="columns"
      :rows-per-page-options="[25,50,100]"
    >
      <template v-slot:top-right>
        <q-btn
          color="primary"
          icon-right="archive"
          label="Export to CSV"
          no-caps
          @click="exportTable"
        />
      </template>
    </q-table>
  </DialogBase>
</template>

<script>
import { exportFile, useQuasar } from 'quasar'
import DialogBase from 'components/dialogs/DialogBase.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'

function wrapCsvValue (val, formatFn, row) {
  let formatted = formatFn !== void 0
    ? formatFn(val, row)
    : val

  formatted = formatted === void 0 || formatted === null
    ? ''
    : String(formatted)

  formatted = formatted.split('"').join('""')
  return `"${formatted}"`
}

export default {
  name: 'DialogShowDataTable',
  components: { DialogBase },
  props: {
    data: Array
  },
  computed: {
    columns () {
      if (!this.data.length) {
        return []
      }
      return Object.keys(this.data[0]).map((dataKey) => {
        const isDateTime = dataKey.includes('_dt')
        return {
          name: dataKey,
          field: dataKey,
          label: dataKey.split('_').map((word) => dataUtil.capitalize(word)).join(' '),
          align: 'left',
          sortable: true,
          format: (isDateTime) ? dateTimeUtil.getDateTime.bind(dateTimeUtil) : (x) => x
        }
      })
    }
  },
  methods: {
    exportTable () {
      // naive encoding to csv format
      const content = [this.columns.map(col => wrapCsvValue(col.label))].concat(
        this.data.map(row => this.columns.map(col => wrapCsvValue(
          typeof col.field === 'function'
            ? col.field(row)
            : row[col.field === void 0 ? col.name : col.field],
          col.format,
          row
        )).join(','))
      ).join('\r\n')

      const status = exportFile(
        'table-export.csv',
        content,
        'text/csv'
      )

      if (status !== true) {
        this.q.notify({
          message: 'Browser denied file download...',
          color: 'negative',
          icon: 'warning'
        })
      }
    }
  },
  setup () {
    return { q: useQuasar() }
  }
}
</script>
