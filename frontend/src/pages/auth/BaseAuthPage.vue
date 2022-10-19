<template>
  <div class="login-container">
    <q-page padding>
      <BannerMessage/>
      <div class="row justify-center items-center" style="height: 75vh; margin-top: 10vh;">
        <q-card class="col-10 col-md-5 col-lg-4">
          <q-card-section>
            <div class="flex justify-center">
              <img src="../../assets/jobVyneLogoOnly.png" alt="Logo" style="height: 70px; object-fit: scale-down">
            </div>
            <h5 class="text-center">
              <slot name="header"/>
            </h5>
          </q-card-section>
          <q-card-section>
            <slot/>
          </q-card-section>
        </q-card>
      </div>
    </q-page>
  </div>
</template>

<script>
import BannerMessage from 'components/BannerMessage.vue'

export default {
  name: 'BaseAuthPage',
  components: { BannerMessage }
}
</script>

<style lang="scss" scoped>
.login-container {
  position: relative;
  height: 100vh;
  width: 100%;

  &::before {
    content: "";
    background: url('../../assets/background/connectwork.png') no-repeat center center fixed;
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
