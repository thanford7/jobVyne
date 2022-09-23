<template>
  <q-select
    v-if="isLoaded"
    filled use-chips multiple
    v-model="tags"
    @update:model-value="$emit('update:model-value', $event)"
    @new-value="createValue"
    :options="tagOptions"
    new-value-mode="add-unique"
    use-input input-debounce="0"
    autocomplete="name"
    @filter="filterTags"
    option-value="id"
    option-label="name"
    label="Select tags or start typing..."
  >
    <template v-slot:append>
      <CustomTooltip :is_include_space="true">
        Tags help you organize and search for your content. All tags are converted to lowercase
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import CustomTooltip from 'components/CustomTooltip.vue'

export default {
  name: 'FileTagsSelector',
  components: { CustomTooltip },
  props: {
    modelValue: {
      type: [Array, null]
    }
  },
  data () {
    return {
      isLoaded: false,
      tags: null,
      filterTxt: null
    }
  },
  computed: {
    tagOptions () {
      const options = this.employerStore.getEmployerFileTags(this.authStore.propUser.employer_id)
      if (!this.filterTxt || this.filterTxt === '') {
        return options
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return options.filter((opt) => opt.name.match(filterRegex))
    }
  },
  methods: {
    createValue (val, done) {
      val = (val) ? val.toLowerCase() : val
      done(val, 'add-unique')
    },
    filterTags (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      employerStore: useEmployerStore()
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployerFileTags(this.authStore.propUser.employer_id)
      ])
    })
    this.isLoaded = true
  }
}
</script>
