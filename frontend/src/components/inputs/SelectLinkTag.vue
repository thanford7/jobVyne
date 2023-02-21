<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    multiple clearable use-chips filled use-input
    map-options emit-value
    new-value-mode="add-unique"
    :options="filteredTags"
    @filter="filter"
    option-value="tag_name" option-label="tag_name"
    :label="label"
    input-debounce="0"
    @new-value="createTag"
  >
    <template v-slot:no-option="{ inputValue }">
      <q-item clickable @click="createTag(inputValue)">
        <q-item-section>
          Create "{{ inputValue }}" tag
        </q-item-section>
      </q-item>
    </template>
    <template v-slot:after>
      <CustomTooltip>
        Start typing to filter and/or create a new tag. Tags can be used
        to track the performance of job boards and links. For example, you
        can create a job board and share it on an email newsletter. To track
        the performance, you could add a "newsletter" tag.
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'
import { storeToRefs } from 'pinia/dist/pinia'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'SelectLinkTag',
  components: { CustomTooltip },
  props: {
    isEmployerMode: Boolean,
    label: {
      type: [String, null],
      default: 'Tags'
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      tags: null,
      user: null
    }
  },
  computed: {
    filteredTags () {
      if (!this.filterTxt || this.filterTxt === '') {
        return this.tags
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.tags.filter((t) => t.tag_name.match(filterRegex))
    }
  },
  methods: {
    filter (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    },
    createTag (tagName) {
      this.filterTxt = null
      this.$refs.select.updateInputValue('')
      const tags = [...dataUtil.getForceArray(this.$refs.select.modelValue), tagName]
      this.$refs.select.$emit('update:modelValue', tags)
      this.$refs.select.blur()
    },
    async getTags () {
      const params = (this.isEmployerMode) ? { employer_id: this.user.employer_id } : { owner_id: this.user.id }
      const linkTagsResp = await this.$api.get('social-link-tag/', { params })
      return linkTagsResp.data
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    await authStore.setUser()
    const { user } = storeToRefs(authStore)
    this.user = user
    this.tags = await this.getTags()
    this.isLoaded = true
  }
}
</script>
