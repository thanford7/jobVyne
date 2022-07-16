<template>
  <div>
    <AuthEmailForm :is-create="isCreate" :default-email="defaultEmail" :user-type-bit="userTypeBit"/>
    <SeparatorWithText>or</SeparatorWithText>
    <AuthSocialButtons
      :is-create="isCreate"
      :user-type-bit="userTypeBit"
      :redirect-page-url="redirectPageUrl"
      :redirect-params="redirectParams"
    />
  </div>
</template>

<script>
import AuthEmailForm from 'components/AuthEmailForm.vue'
import AuthSocialButtons from 'components/AuthSocialButtons.vue'
import SeparatorWithText from 'components/SeparatorWithText.vue'
import { USER_TYPES } from 'src/utils/user-types'
export default {
  name: 'AuthAll',
  components: {
    AuthEmailForm,
    AuthSocialButtons,
    SeparatorWithText
  },
  props: {
    defaultEmail: {
      type: [String, null],
      default: null
    },
    isCreate: {
      type: Boolean,
      default: false
    },
    userTypeBit: {
      type: Number,
      default: USER_TYPES.Employee
    },
    redirectPageUrl: {
      type: [String, null]
    },
    redirectParams: {
      type: [Object, null]
    }
  }
}
</script>
