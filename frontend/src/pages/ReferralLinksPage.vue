<template>
  <q-page padding>
    <div class="q-ml-sm">
      <div class="row q-pb-sm border-bottom-2-gray-300">
        <h5 class="text-gray-900">Referral links</h5>
        <p class="text-gray-500 q-mt-none">
          Add one or more referral links to your social media accounts. Anyone that visits your page can click on the
          link
          and will be directed to a webpage with all open jobs at your company. If they apply and work at your company,
          you can collect a referral bonus!
        </p>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            1
          </div>
          <h6 style="display: inline-block;">Select the platform where you will display the link</h6>
        </div>
        <div class="col-12">
          <q-select
            outlined
            v-model="formData.platform"
            :emit-value="true"
            :options="socialStore.platforms"
            option-value="name"
            option-label="name"
            label="Platform"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            2
          </div>
          <h6 style="display: inline-block;">Add filters for the jobs to display when the link is clicked</h6>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            3
          </div>
          <h6 style="display: inline-block;">These are the currently open jobs based on the filter</h6>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            4
          </div>
          <h6 style="display: inline-block;">Posting instructions</h6>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { useSocialStore } from 'stores/social-store'

export default {
  data () {
    return {
      formData: {
        platform: null
      }
    }
  },
  setup () {
    const socialStore = useSocialStore()
    socialStore.setPlatforms()
    return { socialStore }
  }
}
</script>

<style lang="scss" scoped>
.row {
  margin-bottom: 8px;
}

.col-12 {
  margin-bottom: 8px;
}
</style>
