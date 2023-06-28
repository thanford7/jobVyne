<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    multiple clearable use-chips filled use-input
    map-options emit-value
    :options="filteredJobSubscriptions"
    @filter="filter"
    option-value="id" option-label="title"
    label="Job subscription"
    lazy-rules
    :rules="[
      (val) => val?.length || 'A value is required'
    ]"
  >
    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps" class="border-bottom-1-gray-300">
        <q-item-section>
          <div class="text-bold">{{ scope.opt.title }}</div>
          <JobSubscriptionInfo :job-subscription="scope.opt"/>
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import JobSubscriptionInfo from 'pages/employer/jobs-page/JobSubscriptionInfo.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useAuthStore } from 'stores/auth-store.js'
import { useJobSubscriptionStore } from 'stores/job-subscription-store.js'

export default {
  name: 'SelectJobSubscription',
  components: { JobSubscriptionInfo },
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isLoaded: false,
      jobSubscriptions: null,
      filterTxt: null
    }
  },
  computed: {
    filteredJobSubscriptions () {
      if (!this.filterTxt || this.filterTxt === '') {
        return this.jobSubscriptions
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.jobSubscriptions.filter((js) => js.title.match(filterRegex))
    }
  },
  methods: {
    filter (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    const params = (this.isEmployer) ? { employerId: this.user.employer_id } : { userId: this.user.id }
    await this.jobSubscriptionStore.setJobSubscription(params)
    this.jobSubscriptions = this.jobSubscriptionStore.getJobSubscription(params)
    this.isLoaded = true
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      user,
      jobSubscriptionStore: useJobSubscriptionStore()
    }
  }
}
</script>
