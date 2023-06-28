<template>
  <div>
    <q-btn-dropdown
      ref="dropdown"
      no-caps
      outline
      menu-anchor="bottom start"
      menu-self="top left"
      style="min-height: 56px"
      class="w-100"
    >
      <template v-slot:label>
        <template v-if="modelValue">
          <div class="row">
            <div class="col-12 text-small text-grey-7 text-left" style="height: 18px; margin-top: -5px">
              Selected icon
            </div>
            <div class="col-12 text-left">
              <q-icon :name="modelValue.code"/>
              {{ modelValue.name }}
            </div>
          </div>
        </template>
        <span v-else>
          Select an icon
        </span>
      </template>
      <q-input filled borderless v-model="filter" label="Search" class="w-100">
        <template v-slot:append>
          <q-icon name="search"/>
        </template>
      </q-input>
      <q-table
        flat hide-header hide-pagination
        style="max-height: 25vh"
        :bordered="false"
        :rows="rows"
        :columns="columns"
        virtual-scroll
        v-model:pagination="pagination"
        no-data-label="No icons found"
        :rows-per-page-options="[0]"
        class="border-top-1-gray-300 border-bottom-1-gray-300 border-left-1-gray-100 border-right-1-gray-100"
      >
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td
              v-for="col in props.cols"
              :key="col.field"
              :props="props"
              class="bg-hover-gray-300"
              style="cursor: pointer"
              @click="selectIcon(props.row[col.field])"
            >
              <q-icon :name="props.row[col.field]" size="md"/>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </q-btn-dropdown>
  </div>
</template>

<script>
import { MATERIAL_ICONS_MAP } from 'src/utils/material-icons-map'
import { useQuasar } from 'quasar'

export default {
  name: 'IconPicker',
  props: {
    modelValue: {
      type: [Object, null]
    }
  },
  computed: {
    columnCount () {
      const $q = useQuasar()
      if ($q.screen.lt.sm) {
        return 4
      } else if ($q.screen.lt.lg) {
        return 6
      } else {
        return 8
      }
    },
    rows () {
      const rows = []
      const filter = (this.filter) ? new RegExp(`.*?${this.filter}.*?`, 'i') : null
      MATERIAL_ICONS_MAP
        .filter((icon) => !filter || icon.name.match(filter))
        .forEach((icon, idx) => {
          const rowIdx = Math.floor(idx / this.columnCount)
          const colIdx = idx % this.columnCount
          const isNewRow = colIdx === 0
          if (isNewRow) {
            rows.push({})
          }
          rows[rowIdx][`code${colIdx}`] = icon.code
          rows[rowIdx][`name${colIdx}`] = icon.name
        })
      return rows
    },
    columns () {
      const columns = []
      for (let i = 0; i < this.columnCount; i++) {
        const key = `code${i}`
        columns.push({ name: key, field: key, align: 'center' })
      }
      return columns
    }
  },
  data () {
    return {
      filter: '',
      pagination: {
        rowsPerPage: 0
      }
    }
  },
  methods: {
    selectIcon (code) {
      const icon = MATERIAL_ICONS_MAP.find((icon) => icon.code === code)
      this.$emit('update:modelValue', icon)
      this.$refs.dropdown.hide()
    }
  }
}
</script>
