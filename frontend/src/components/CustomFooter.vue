<template>
  <q-footer elevated reveal class="bg-grey-8 text-white justify-center row">
    <q-toolbar class="col-12 col-md-11 col-lg-8 q-py-md">
      <q-toolbar-title>
        <img src="../assets/jobVyneLogoWhite.png" alt="Logo" style="height: 40px; object-fit: scale-down">
      </q-toolbar-title>
      <q-tabs align="right" shrink>
        <q-route-tab to="/privacy" label="Privacy"/>
        <q-route-tab to="/terms-of-service" label="Terms of Service"/>
      </q-tabs>
    </q-toolbar>
  </q-footer>
</template>

<script>
export default {
  name: 'CustomFooter'
}
</script>
