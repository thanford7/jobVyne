<template>
  <DialogBase
    base-title-text="Create new group"
    primary-button-text="Create"
    @ok="saveGroup"
  >
    <q-input
      filled
      v-model="formData.name"
      label="Group name"
      lazy-rules
      :rules="[
        val => val && val.length > 0 || 'Group name is required',
        val => !existingGroupNames.includes(val) || 'There is already a group with this name'
      ]"
    />
    <SelectUserType
      v-model="formData.user_type_bit"
      :allowed-user-types="[USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE]"
    />
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import { USER_TYPE_EMPLOYEE, USER_TYPE_EMPLOYER } from 'src/utils/user-types.js'
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import { getAjaxFormData } from 'src/utils/requests'
import SelectUserType from 'components/inputs/SelectUserType.vue'

export default {
  name: 'DialogEmployerAuthGroup',
  extends: DialogBase,
  inheritAttrs: false,
  components: { SelectUserType, DialogBase },
  data () {
    return {
      formData: {
        name: null,
        user_type_bit: null
      },
      USER_TYPE_EMPLOYER,
      USER_TYPE_EMPLOYEE
    }
  },
  computed: {
    existingGroupNames () {
      return this.employerStore.permissionGroups.map((group) => group.name)
    }
  },
  methods: {
    async saveGroup () {
      const data = {
        ...this.formData,
        employer_id: this.authStore.user.employer_id
      }
      const resp = await this.$api.post('employer/permission/', getAjaxFormData(data))
      await this.employerStore.setEmployerPermissions(true)
      this.$emit('ok', resp.data.auth_group_id)
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    return employerStore.setEmployerPermissions()
  },
  setup () {
    return { authStore: useAuthStore(), employerStore: useEmployerStore() }
  }
}
</script>
