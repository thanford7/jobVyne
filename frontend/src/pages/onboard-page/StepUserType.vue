<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Select the types of accounts that are relevant to you"
  >
    <q-form ref="form">
      <div class="row">
        <div v-for="userType in userTypesCfg" class="col-6 col-md-4 q-pa-sm">
          <q-card
            :id="userType.id"
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
            <Tooltip>
              <ul>
                <li v-for="item in userType.descriptionItems">{{ item }}</li>
              </ul>
            </Tooltip>
          </q-card>
        </div>
      </div>
    </q-form>
    <template v-slot:buttons>
      <slot name="backButton"></slot>
      <slot v-if="canContinue" name="continueButton"></slot>
    </template>
  </BaseStep>
</template>

<script>
import Tooltip from 'components/Tooltip.vue'
import BaseStep from 'pages/onboard-page/BaseStep.vue'
import colorUtil from 'src/utils/color.js'

export default {
  name: 'StepUserType',
  components: { Tooltip, BaseStep },
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
  },
  methods: {
    async isValidForm () {
      return this.canContinue
    }
  }
}
</script>
