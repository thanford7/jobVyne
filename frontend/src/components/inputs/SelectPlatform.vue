<template>
  <q-select
    v-if="isLoaded"
    filled
    :options="socialStore.platforms"
    autocomplete="name"
    option-value="name"
    option-label="name"
    label="Platform"
  >
    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps">
        <q-item-section avatar>
          <img :src="scope.opt.logo" alt="Logo" style="max-height: 20px">
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ scope.opt.name }}</q-item-label>
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'SelectPlatform',
  data () {
    return {
      isLoaded: false,
      socialStore: null
    }
  },
  async mounted () {
    this.socialStore = useSocialStore()
    await this.socialStore.setPlatforms()
    this.isLoaded = true
  }
}
</script>
