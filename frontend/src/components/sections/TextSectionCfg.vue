<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="col-12 col-md-8">
    <SelectFiles
      :file-type-keys="[FILE_TYPES.IMAGE.key, FILE_TYPES.VIDEO.key]"
      :is-emit-id-only="true"
      :is-employer="true"
      :is-multi-select="false"
      label-override="Select content"
      v-model:employer-file-ids="section.item_parts[0].file_id"
    />
  </div>
  <div class="col-12 col-md-4 q-pl-md-sm">
    <q-select
      filled emit-value map-options
      label="Content placement"
      :options="[
        { val: 'left', label: 'Left' },
        { val: 'right', label: 'Right' }
      ]"
      v-model="section.item_parts[0].file_placement"
      option-label="label"
      option-value="val"
    />
  </div>
  <div class="col-12">
    <WysiwygEditor2
      v-model="section.item_parts[0].html_content"
      placeholder="Section text..."
    />
  </div>
  <LiveView :section="section">
      <SectionHeader :section="section"/>
      <TextSection :section="section" :employer-id="user.employer_id"/>
  </LiveView>
</template>

<script>
import SelectFiles from 'components/inputs/SelectFiles.vue'
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'
import LiveView from 'components/sections/LiveView.vue'
import SectionHeader from 'components/sections/SectionHeader.vue'
import TextSection from 'components/sections/TextSection.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { FILE_TYPES } from 'src/utils/file.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'TextSectionCfg',
  props: {
    section: Object
  },
  components: { SelectFiles, TextSection, LiveView, SectionHeader, WysiwygEditor2 },
  data () {
    return {
      FILE_TYPES
    }
  },
  async mounted () {
    await this.authStore.setUser()
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      authStore,
      user
    }
  }
}
</script>
