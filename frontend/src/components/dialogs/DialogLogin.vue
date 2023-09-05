<template>
  <DialogBase
    :base-title-text="(isCreate) ? 'Create account' : 'Login'"
    :is-include-buttons="false"
  >
    <div v-if="isShowLoginToggle" class="q-mb-md">
      <q-btn-toggle
        v-model="isCreate"
        toggle-color="grey-7" spread
        :options="[
          { label: 'Login', value: false },
          { label: 'Create account', value: true }
        ]"
      />
    </div>
    <AuthAll
      :is-create="isCreate"
      :redirect-page-url="redirectPageUrl"
      :redirect-params="redirectParams"
      :user-type-bit="userTypeBit"
      :style-override="styleOverride"
    />
  </DialogBase>
</template>

<script>
import AuthAll from 'components/AuthAll.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogLogin',
  extends: DialogBase,
  inheritAttrs: false,
  components: { AuthAll, DialogBase },
  props: {
    isCreateDefault: {
      type: Boolean,
      default: false
    },
    isShowLoginToggle: {
      type: Boolean,
      default: true
    },
    redirectPageUrl: {
      type: [String, null]
    },
    redirectParams: {
      type: [Object, null]
    },
    userTypeBit: {
      type: [Number, null]
    },
    styleOverride: {
      type: [Object, null]
    }
  },
  data () {
    return {
      isCreate: this.isCreateDefault
    }
  },
  methods: {
    closeDialog () {
      this.$emit('ok')
      this.$emit('hide')
    }
  },
  mounted () {
    this.$global.$on('login', this.closeDialog.bind(this))
  }
}
</script>
