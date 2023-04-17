<template>
  <q-btn
    ripple no-wrap style="padding: 8px; height: 40px;"
  >
    <q-img v-if="platform.logo" :src="platform.logo" width="18px"/>
    <q-icon v-else tag="div" :name="`fa-brands ${platform.icon}`" class="q-mr-sm"/>
    <div class="text-center" style="font-family: Roboto, sans-serif; font-size: 14px; padding-left: 24px;">
      {{ buttonText }}
    </div>
  </q-btn>
</template>

<script>
export default {
  name: 'AuthSocialButton',
  props: {
    platform: Object,
    buttonText: String
  }
}
</script>
