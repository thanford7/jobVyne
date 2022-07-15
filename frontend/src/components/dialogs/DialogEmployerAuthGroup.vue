<template>
  <DialogBase
    title-text="Create new group"
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
    <q-select
      filled
      v-model="formData.user_type_bit"
      :options="userGroups"
      autocomplete="name"
      option-value="user_type_bit"
      option-label="name"
      label="User type"
      :rules="[val => val && val.length > 0 || 'User type is required',]"
    />
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore, USER_TYPE_EMPLOYEE, USER_TYPE_EMPLOYER, USER_TYPES } from 'stores/auth-store'
import { getAjaxFormData } from 'src/utils/requests'

export default {
  name: 'DialogEmployerAuthGroup',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase },
  data () {
    return {
      formData: {
        name: null,
        user_type_bit: null
      },
      userGroups: [USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE].map((userType) => {
        return {
          name: userType,
          user_type_bit: USER_TYPES[userType]
        }
      })
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
      await this.$api.post('employer/permission/', getAjaxFormData(data))
      this.employerStore.setEmployerPermissions()
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
