<template>
  <div class="bg-grey-8 text-white">
    <q-toolbar class="justify-center items-center">
      <ResponsiveWidth class="q-py-md">
        <div class="row">
          <div class="col-8 col-md-6">
            <div class="lt-md">
              <q-list dense>
                <q-item :to="{ name: 'privacy' }" active-class="" clickable v-ripple>
                  <q-item-section>Privacy</q-item-section>
                </q-item>
                <q-item :to="{ name: 'tos' }" active-class="" clickable v-ripple>
                  <q-item-section>Terms of Service</q-item-section>
                </q-item>
                <q-item :to="{ name: 'credits' }" active-class="" clickable v-ripple>
                  <q-item-section>Credits</q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>
                    Copyright JobVyne {{ dateTimeUtil.getCurrentYear() }}
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
            <div class="gt-sm q-gutter-md">
              <div style="display: inline-block">
                Copyright JobVyne {{ dateTimeUtil.getCurrentYear() }}
              </div>
              <div style="display: inline-block">
                <router-link :to="{ name: 'privacy' }" v-ripple class="text-white">Privacy</router-link>
              </div>
              <div style="display: inline-block">
                <router-link :to="{ name: 'tos' }" v-ripple class="text-white">Terms of Service</router-link>
              </div>
              <div style="display: inline-block">
                <router-link :to="{ name: 'credits' }" v-ripple class="text-white">Credits</router-link>
              </div>
            </div>
          </div>
          <div class="col-4 col-md-6" style="margin-top: auto">
            <div class="flex justify-end">
              <img src="../assets/jobVyneLogoWhite.png" alt="Logo" style="max-height: 25px; object-fit: scale-down">
            </div>
          </div>
        </div>
      </ResponsiveWidth>
    </q-toolbar>
  </div>
</template>

<script>
import dateTimeUtil from 'src/utils/datetime'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'

export default {
  name: 'CustomFooter',
  components: { ResponsiveWidth },
  data () {
    return {
      dateTimeUtil
    }
  }
}
</script>
