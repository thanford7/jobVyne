<template>
  <q-select
    filled multiple emit-value map-options clearable use-chips
    :options="options"
    autocomplete="name"
    option-value="id"
    :label="label"
    :rules="rules"
  >
    <template v-slot:option="{ itemProps, opt, selected, toggleOption }">
      <q-expansion-item
        expand-separator
        :default-opened="true"
        header-class="text-bold"
        :label="userTypeUtil.getUserTypeNameFromBit(opt.user_type_bit)"
      >
        <q-item
          v-for="child in opt.child_options"
          v-bind="getOptionProps(itemProps)"
          :active="selected"
          class="background-hover"
          @click="toggleOption(child)"
        >
          <q-item-section>
            {{ child.name }}
          </q-item-section>
        </q-item>
      </q-expansion-item>
    </template>
    <template v-slot:selected-item="{ opt, toggleOption }">
      <q-chip removable @remove="toggleOption(opt)">{{ getOptionLabel(opt) }}</q-chip>
    </template>
  </q-select>
</template>

<script>
import { useEmployerStore } from 'stores/employer-store'
import dataUtil from 'src/utils/data'
import userTypeUtil from 'src/utils/user-types'

export default {
  name: 'SelectPermissionGroup',
  props: {
    label: {
      type: String,
      default: 'Permission group'
    },
    isRequired: {
      type: Boolean,
      default: true
    },
    rulesOverride: {
      type: [Array, null]
    }
  },
  data () {
    return {
      userTypeUtil
    }
  },
  computed: {
    options () {
      const groupedPermissions = dataUtil.groupBy(this.employerStore.permissionGroups, 'user_type_bit')
      return Object.entries(groupedPermissions).map(([userTypeBit, childOptions]) => {
        return {
          user_type_bit: userTypeBit,
          child_options: childOptions
        }
      })
    },
    rules () {
      if (this.rulesOverride) {
        return this.rulesOverride
      }
      return (this.isRequired) ? [(val) => (val && val.length > 0) || 'At least one permission group is required'] : []
    }
  },
  methods: {
    log (val) {
      return console.log(val)
    },
    getOptionProps (itemProps) {
      return dataUtil.omit(itemProps, ['id', 'onClick', 'onMousemove'])
    },
    getOptionLabel (groupId) {
      return this.employerStore.permissionGroups.find((pg) => pg.id === parseInt(groupId)).name
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    return employerStore.setEmployerPermissions()
  },
  setup () {
    return { employerStore: useEmployerStore() }
  }
}
</script>
