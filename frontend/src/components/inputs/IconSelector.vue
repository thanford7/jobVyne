<template>
  <q-select
    filled clearable
    v-model="selectedIcon"
    :options="MATERIAL_ICONS_MAP"
    autocomplete="name"
    option-value="code"
    option-label="name"
    label="Search icon..."
  >
    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps" @click="scope.toggleOption(scope.opt)">
        <q-item-section avatar>
          <q-icon size="md" :name="scope.opt.code"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ scope.opt.name }}</q-item-label>
        </q-item-section>
      </q-item>
    </template>
    <template v-slot:selected-item="{ opt }">
      <div>
        <q-icon size="sm" :name="opt.code"/> {{ opt.name }}
      </div>
    </template>
  </q-select>
</template>

<script>
import { MATERIAL_ICONS_MAP } from 'src/utils/material-icons-map'

export default {
  name: 'IconSelector',
  data () {
    return {
      MATERIAL_ICONS_MAP,
      selectedIcon: null
    }
  }
}
</script>
