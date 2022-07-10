<template>
  <div class="login-container">
    <q-page padding>
      <BannerMessage/>
      <div class="row justify-center items-center" style="height: 75vh;">
        <q-card class="col-10 col-md-4 col-lg-3">
          <q-card-section>
            <div class="flex justify-center">
              <img src="../assets/jobVyneLogoOnly.png" alt="Logo" style="height: 70px; object-fit: scale-down">
            </div>
            <h5 class="text-center">Welcome back!</h5>
          </q-card-section>
          <q-card-section>
            <AuthAll/>
          </q-card-section>
        </q-card>
      </div>
    </q-page>
  </div>
</template>

<script>
import BannerMessage from 'components/BannerMessage.vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'
import AuthAll from 'components/AuthAll.vue'

// TODO: Add functionality to switch between user types (this could be a unique link for each - employer, influencer, etc)
// TODO: Add functionality to switch between sign up vs login
export default {
  name: 'PageName',
  components: { AuthAll, BannerMessage },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Login'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  position: relative;
  height: 100vh;
  width: 100%;

  &::before {
    content: "";
    background: url('../assets/background/connectwork.png') no-repeat center center fixed;
    background-size: cover;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    opacity: 0.2;
    overflow: hidden;
  }
}
</style>
