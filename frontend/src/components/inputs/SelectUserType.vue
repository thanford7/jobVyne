<template>
  <q-select
    filled emit-value map-options
    :multiple="isMulti"
    :options="userGroups"
    autocomplete="name"
    option-value="user_type_bit"
    option-label="name"
    label="User type"
    :rules="rules"
  />
</template>

<script>
import { USER_TYPE_EMPLOYEE, USER_TYPE_EMPLOYER, USER_TYPE_INFLUENCER, USER_TYPES } from 'src/utils/user-types'

export default {
  name: 'SelectUserType',
  props: {
    isRequired: {
      type: Boolean,
      default: true
    },
    isMulti: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    userGroups () {
      return [USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE, USER_TYPE_INFLUENCER].map((userType) => {
        return {
          name: userType,
          user_type_bit: USER_TYPES[userType]
        }
      })
    },
    rules () {
      return (this.isRequired) ? [val => val || 'User type is required'] : []
    }
  }
}
</script>
