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
            <h5 class="text-center">{{ (isCreate) ? newUserHeader : currentUserHeader }}</h5>
          </q-card-section>
          <q-card-section>
            <AuthAll :is-create="isCreate"/>
            <div class="q-mt-md">
              <div v-if="isCreate">
                Current user? <a href="#" @click="isCreate=false">Login here</a>
              </div>
              <div v-else>
                New user? <a href="#" @click="isCreate=true">Sign up here</a>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-page>
  </div>
</template>

<script>
import { USER_TYPES, USER_TYPE_EMPLOYEE } from 'src/utils/user-types.js'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'
import AuthAll from 'components/AuthAll.vue'
import BannerMessage from 'components/BannerMessage.vue'

export default {
  name: 'PageName',
  components: { AuthAll, BannerMessage },
  data () {
    return {
      isCreate: false,
      newUserHeader: 'Join JobVyne!',
      currentUserHeader: 'Welcome back!',
      USER_TYPES,
      USER_TYPE_EMPLOYEE
    }
  },
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
