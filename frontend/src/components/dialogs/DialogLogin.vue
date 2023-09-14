<template>
  <DialogBase
    :base-title-text="(isCreate) ? 'Join JobVyne' : 'Login'"
    :is-include-buttons="false"
    width="700px"
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
    <q-card v-if="isCreate" class="q-px-sm q-pt-sm q-mb-md border-y-1-gray-100" flat>
      <div>
        Join thousands of other professionals! Unlock all of the benefits of JobVyne for free!
      </div>
      <ListIcon
        class="text-small"
        :items="[
          {icon: 'groups', text: 'Connect with other professionals that can provide warm introductions to hiring companies'},
          {icon: 'event', text: 'Get notified when the most recent and relevant jobs are posted'},
          {icon: 'attach_money', text: 'Easily search jobs by location, salary, and applicant tracking sytem'}
        ]"
        icon-size="24px"
      />
    </q-card>
    <AuthAll
      :is-create="isCreate"
      :redirect-page-url="redirectPageUrl"
      :redirect-params="signUpParams"
      :user-type-bit="userTypeBit"
      :style-override="styleOverride"
    />
  </DialogBase>
</template>

<script>
import AuthAll from 'components/AuthAll.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import ListIcon from 'components/ListIcon.vue'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'DialogLogin',
  extends: DialogBase,
  inheritAttrs: false,
  components: { ListIcon, AuthAll, DialogBase },
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
  computed: {
    signUpParams () {
      if (this.isCreate) {
        return this.redirectParams
      } else {
        return dataUtil.omit(this.redirectParams, ['isSignUp'])
      }
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
