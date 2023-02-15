<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job links"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="employee" label="Employee referrals"/>
        <q-tab name="job" label="Job webpages"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="employee">
          <div>
            <div class="row q-gutter-y-md">
              <div class="col-12 callout-card">
                Send referral requests to employees. Each employee will receive a unique tracking link.
              </div>
              <div class="col-12 q-pt-md">
                <q-table>
                  <template v-slot:top>
                    <div>
                      <q-btn
                        label="Send referral request"
                        color="primary" ripple unelevated
                        @click="openReferralRequestDialog"
                      />
                    </div>
                  </template>
                </q-table>
              </div>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="job">
          <div>
            <div class="row">
              <div class="col-12 callout-card">
                Generate links that will direct to a job board page. This can be used as a company jobs website
                or posted on other areas of employer owned sites (such as a LinkedIn employer page).
              </div>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import DialogShareJobLink from 'components/dialogs/DialogShareJobLink.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobLinksPage',
  components: { PageHeader },
  data () {
    return {
      tab: 'employee'
    }
  },
  methods: {
    openReferralRequestDialog () {
      return this.q.dialog({
        component: DialogShareJobLink,
        componentProps: { employerId: this.user.employer_id }
      })
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Job links'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      user,
      q: useQuasar()
    }
  }
}
</script>
