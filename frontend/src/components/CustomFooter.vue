<template>
  <q-footer elevated reveal class="bg-grey-8 text-white">
    <q-toolbar class="justify-center items-center">
      <div class="col-12 col-md-11 col-lg-8 q-py-md">
        <div class="row">
          <div class="col-6">
            <q-list class="lt-md" dense>
              <q-item :to="{ name: 'privacy' }" active-class="" clickable v-ripple>
                <q-item-section>Privacy</q-item-section>
              </q-item>
              <q-item :to="{ name: 'tos' }" active-class="" clickable v-ripple>
                <q-item-section>Terms of Service</q-item-section>
              </q-item>
            </q-list>
            <div class="gt-sm q-gutter-md">
              <div style="display: inline-block">
                <router-link :to="{ name: 'privacy' }" v-ripple class="text-white">Privacy</router-link>
              </div>
              <div style="display: inline-block">
                <router-link :to="{ name: 'tos' }" v-ripple class="text-white">Terms of Service</router-link>
              </div>
            </div>
          </div>
          <div class="col-6" style="margin-top: auto">
            <div class="flex justify-end">
              <img src="../assets/jobVyneLogoWhite.png" alt="Logo" style="max-height: 25px; object-fit: scale-down">
            </div>
          </div>
        </div>
      </div>
    </q-toolbar>
  </q-footer>
</template>

<script>
export default {
  name: 'CustomFooter'
}
</script>
