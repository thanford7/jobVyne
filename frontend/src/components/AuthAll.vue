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
      type: [Number, null]
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
