<template>
  <q-select
    filled use-chips multiple
    v-model="tags"
    @update:model-value="$emit('update:model-value', $event)"
    @new-value="createValue"
    :options="tagOptions"
    new-value-mode="add-unique"
    use-input input-debounce="0"
    autocomplete="name"
    option-value="id"
    option-label="name"
    label="Select tags or start typing..."
  >
    <template v-slot:append>
      <CustomTooltip>
        Tags help you organize and search for your content. All tags are converted to lowercase
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import { Loading } from 'quasar'
import CustomTooltip from 'components/CustomTooltip.vue'

export default {
  name: 'EmployerFileTagsSelector',
  components: { CustomTooltip },
  props: {
    modelValue: {
      type: [Array, null]
    }
  },
  data () {
    return {
      tags: null
    }
  },
  computed: {
    tagOptions () {
      return this.employerStore.getEmployerFileTags(this.authStore.propUser.employer_id)
    }
  },
  methods: {
    createValue (val, done) {
      val = (val) ? val.toLowerCase() : val
      done(val, 'add-unique')
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployerFileTags(authStore.propUser.employer_id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    return {
      authStore: useAuthStore(),
      employerStore: useEmployerStore()
    }
  }
}
</script>
