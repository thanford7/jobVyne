<template>
  <DialogBase
    :base-title-text="titleText"
    :primary-button-text="(!this.user_ids) ? 'Create' : 'Update'"
    @ok="saveUser"
  >
    <q-form ref="form" v-if="isSingle">
      <SelectEmployer
        v-if="isAdmin"
        v-model="formDataSingle.employer_id" :is-multi="false"
        :rules="[ val => val || 'Employer is required']"
      />
      <q-input
        filled
        v-model="formDataSingle.first_name"
        label="First name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'First name is required']"
      />
      <q-input
        filled
        v-model="formDataSingle.last_name"
        label="Last name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Last name is required']"
      />
      <q-input
        v-if="!user_ids"
        filled
        v-model="formDataSingle.email"
        label="Email"
        lazy-rules
        :rules="[ val => val && val.length > 0 && formUtil.isGoodEmail(val) || 'Please enter a valid email']"
      />
      <SelectPermissionGroup
        label="Permission groups"
        v-model="formDataSingle.permission_group_ids"
      />
      <PasswordInput
        v-if="isAdmin"
        v-model="formDataSingle.password"
        :is-validate="true"
      />
    </q-form>
    <q-form ref="form" v-else>
      <SelectPermissionGroup
        v-model="formDataMulti.add_permission_group_ids"
        label="Add permission groups"
        :rules-override="[val => !hasAddRemoveOverlap || 'Add permissions can\'t overlap with those in the remove permissions selection',]"
      />
      <SelectPermissionGroup
        v-model="formDataMulti.remove_permission_group_ids"
        label="Remove permission groups"
        :rules-override="[val => !hasAddRemoveOverlap || 'Remove permissions can\'t overlap with those in the add permissions selection',]"
      />
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import PasswordInput from 'components/inputs/PasswordInput.vue'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data'
import formUtil from 'src/utils/form'
import { getAjaxFormData } from 'src/utils/requests'
import { useAuthStore } from 'stores/auth-store'
import SelectPermissionGroup from 'components/inputs/SelectPermissionGroup.vue'

const FORM_DATE_SINGLE_TEMPLATE = {
  first_name: null,
  last_name: null,
  email: null,
  permission_group_ids: null,
  employer_id: null,
  password: null
}

const FORM_DATE_MULTI_TEMPLATE = {
  add_permission_group_ids: null,
  remove_permission_group_ids: null
}

export default {
  name: 'DialogUser',
  extends: DialogBase,
  inheritAttrs: false,
  components: { PasswordInput, SelectPermissionGroup, DialogBase, SelectEmployer },
  data () {
    return {
      user_ids: null,
      isSingle: true,
      formDataSingle: { ...FORM_DATE_SINGLE_TEMPLATE },
      formDataMulti: { ...FORM_DATE_MULTI_TEMPLATE },
      dataUtil,
      formUtil
    }
  },
  props: {
    users: {
      type: [Array, Object] // Users can be plural (Array) or singular (Object)
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    titleText () {
      if (!this.user_ids) {
        return 'Create new user'
      } else if (this.isSingle) {
        return 'Update user'
      } else {
        return `Update ${this.user_ids.length} users`
      }
    },
    hasAddRemoveOverlap () {
      const intersection = this.dataUtil.getArrayIntersection(
        this.formDataMulti.add_permission_group_ids,
        this.formDataMulti.remove_permission_group_ids
      )
      return Boolean(intersection.length)
    }
  },
  methods: {
    async saveUser () {
      const isValid = await this.$refs.form.validate()
      if (!isValid) {
        return
      }
      const ajaxFn = (this.user_ids) ? this.$api.put : this.$api.post
      const data = {}
      if (this.user_ids) {
        data.user_ids = this.user_ids
      }
      Object.assign(data, (this.isSingle) ? this.formDataSingle : this.formDataMulti)
      if (!this.isAdmin) {
        data.employer_id = this.user.employer_id
      }
      await ajaxFn('employer/user/', getAjaxFormData(data))
      this.$emit('ok')
    }
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return { authStore, user }
  },
  async mounted () {
    // Clear out the forms
    Object.assign(this.formDataSingle, FORM_DATE_SINGLE_TEMPLATE)
    Object.assign(this.formDataMulti, FORM_DATE_MULTI_TEMPLATE)

    // Populate form for single user
    if (dataUtil.isObject(this.users) || this?.users?.length === 1) {
      const user = Array.isArray(this.users) ? this.users[0] : this.users
      this.user_ids = [user.id]
      Object.assign(this.formDataSingle, dataUtil.pick(user, ['first_name', 'last_name', 'email', 'employer_id']))
      this.formDataSingle.permission_group_ids = (user.employer_id) ? user.permission_groups_by_employer[user.employer_id].map((pg) => pg.id) : []
      this.isSingle = true
    } else if (this.users && this.users.length) { // Multiple users
      this.user_ids = this.users.map((user) => user.id)
      this.isSingle = false
    } else { // New user
      this.user_ids = null
      this.isSingle = true
    }
  }
}
</script>
