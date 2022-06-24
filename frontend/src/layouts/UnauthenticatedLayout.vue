<template>
  <q-layout view="hHh lpr fFf">

    <q-header elevated reveal class="bg-white text-primary justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-py-md">
        <a href="/">
          <q-toolbar-title>
            <img src="../assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
          </q-toolbar-title>
        </a>
        <q-space />
        <q-tabs align="right" shrink>
          <q-route-tab to="/page1" label="Page One"/>
          <q-route-tab to="/page2" label="Page Two"/>
          <q-route-tab to="/login" label="Login"/>
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view/>
    </q-page-container>

    <q-footer elevated reveal class="bg-grey-8 text-white justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-py-md">
        <q-toolbar-title>
          <img src="../assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
export default {
  name: 'UnauthenticatedLayout'
}
</script>

<style scoped>

</style>
