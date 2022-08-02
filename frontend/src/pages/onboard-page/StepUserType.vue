<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Select the types of accounts that are relevant to you"
  >
    <div v-for="userType in userTypesCfg" class="col-6 col-md-4 q-pa-sm">
      <q-card
        class="h-100"
        style="cursor: pointer"
        :style="(formData.user_type_bits & userType.userTypeBit) ? {backgroundColor: colorUtil.changeAlpha(colorUtil.getPaletteColor('primary'), 0.2)} : null"
        @click="formData.user_type_bits ^= userType.userTypeBit"
      >
        <q-card-section>
          <div class="flex items-center justify-center">
            <q-icon :name="userType.icon" size="50px"/>
          </div>
          <h6 class="text-center">{{ userType.title }}</h6>
        </q-card-section>
        <q-tooltip class="bg-info" style="font-size: 14px;" max-width="500px">
          <ul>
            <li v-for="item in userType.descriptionItems">{{ item }}</li>
          </ul>
        </q-tooltip>
      </q-card>
    </div>
    <template v-slot:buttons>
      <slot name="backButton"></slot>
      <slot v-if="canContinue" name="continueButton"></slot>
    </template>
  </BaseStep>
</template>

<script>
import BaseStep from 'pages/onboard-page/BaseStep.vue'
import colorUtil from 'src/utils/color.js'

export default {
  name: 'StepUserType',
  components: { BaseStep },
  props: {
    userTypesCfg: Object,
    formData: Object
  },
  computed: {
    canContinue () {
      return this.formData.user_type_bits
    }
  },
  data () {
    return {
      colorUtil
    }
  }
}
</script>

<style scoped>

</style>
