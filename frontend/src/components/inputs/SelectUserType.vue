<template>
  <q-select
    filled emit-value map-options use-chips
    :model-value="selectedTypes"
    @update:model-value="$emit('update:model-value', getBitValue($event))"
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
import dataUtil from 'src/utils/data.js'
import userTypeUtil, {
  USER_TYPE_ADMIN,
  USER_TYPE_INFLUENCER,
  USER_TYPES
} from 'src/utils/user-types'

export default {
  name: 'SelectUserType',
  props: {
    modelValue: {
      type: [Number, null]
    },
    isRequired: {
      type: Boolean,
      default: true
    },
    isMulti: {
      type: Boolean,
      default: false
    },
    allowedUserTypes: {
      type: Array,
      default: Object.keys(USER_TYPES).filter((ut) => ![USER_TYPE_ADMIN, USER_TYPE_INFLUENCER].includes(ut))
    }
  },
  computed: {
    selectedTypes () {
      if (!this.isMulti || dataUtil.isNil(this.modelValue)) {
        return (this.modelValue === 0) ? null : this.modelValue
      }
      const includeBits = this.userGroups.reduce((allBits, userGroup) => {
        allBits |= userGroup.user_type_bit
        return allBits
      }, 0)
      return userTypeUtil.getUserTypeList(this.modelValue, true, { excludeBits: 0, includeBits })
    },
    userGroups () {
      return this.allowedUserTypes.map((userType) => {
        return {
          name: userType,
          user_type_bit: USER_TYPES[userType]
        }
      })
    },
    rules () {
      return (this.isRequired) ? [val => val || 'User type is required'] : []
    }
  },
  methods: {
    getBitValue (selectedBitsList) {
      // Some bits are not shown in the selection because users should not be able to edit them
      // For example an employer should not be able to edit a users bits for candidate or admin
      // To avoid overwriting these values, we must preserve any bits that the user already has
      const preserveBits = Object.entries(USER_TYPES).reduce((preserveBits, [userType, userBit]) => {
        if (!this.allowedUserTypes.includes(userType)) {
          preserveBits |= userBit
        }
        return preserveBits
      }, 0)
      const userPreserveBits = preserveBits & this.modelValue
      const selectedBits = dataUtil.getBitsFromList(selectedBitsList)
      return userPreserveBits | selectedBits
    }
  }
}
</script>
