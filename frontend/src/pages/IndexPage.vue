<template>
  <q-page padding>
    <div class="row justify-center q-mt-xl">
      <ResponsiveWidth>
        <div class="row">
          <div class="col-12 col-md-7 q-gutter-y-lg">
            <div class="rfs-h2 text-center text-bold font-primary">Turn your employees into your best recruiters</div>
            <div class="rfs-h6 text-center text-gray-700">
              Automate employee referrals and generate more meaningful connections with job seekers
            </div>
            <div class="q-px-lg">
              <q-input
                filled
                v-model="email"
                label="Email"
                :rules="[ val => val && val.length > 0 && isGoodEmail(val) || 'Please enter a valid email']"
              >
                <template v-slot:after>
                  <q-btn class="h-100" color="accent" ripple unelevated @click="saveWaitlist">
                    Join waitlist
                  </q-btn>
                </template>
              </q-input>
            </div>
          </div>
          <div class="col-12 col-md-5 q-pl-md-md q-pl-none q-mt-md q-mt-md-none">
            <div class="flex justify-center items-center" style="height: 100%">
              <img src="../assets/images/social-share.jpg" alt="Social sharing"
                   style="object-fit: scale-down; max-width: 100%">
            </div>
          </div>
        </div>
      </ResponsiveWidth>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'

export default defineComponent({
  name: 'IndexPage',
  components: { ResponsiveWidth },
  data () {
    return {
      email: null
    }
  },
  methods: {
    saveWaitlist () {
      //
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Home'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
})
</script>
