<template>
  <q-input
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    filled
    :type="isPwdShown ? 'text' : 'password'"
    :label="label" :rules="rules"
    class="jv-password"
  >
    <template v-slot:append>
      <q-icon
        :name="isPwdShown ? 'visibility' : 'visibility_off'"
        class="cursor-pointer"
        @click="isPwdShown = !isPwdShown"
      />
    </template>
    <template v-if="isValidate" v-slot:after>
      <CustomTooltip>
        Password must have:
        <ul>
          <li>
            10 characters minimum
            <template v-if="modelValue">
              <q-icon v-if="pwdHas10Chars" name="check_circle" color="positive"/>
              <q-icon v-else name="cancel" color="negative"/>
            </template>
          </li>
          <li>
            At least 1 lowercase letter
            <template v-if="modelValue">
              <q-icon v-if="pwdHasLowercaseChar" name="check_circle" color="positive"/>
              <q-icon v-else name="cancel" color="negative"/>
            </template>
          </li>
          <li>
            At least 1 uppercase letter
            <template v-if="modelValue">
              <q-icon v-if="pwdHasUppercaseChar" name="check_circle" color="positive"/>
              <q-icon v-else name="cancel" color="negative"/>
            </template>
          </li>
          <li>
            At least 1 number
            <template v-if="modelValue">
              <q-icon v-if="pwdHasNumber" name="check_circle" color="positive"/>
              <q-icon v-else name="cancel" color="negative"/>
            </template>
          </li>
          <li>
            At least one symbol
            <template v-if="modelValue">
              <q-icon v-if="pwdHasSymbol" name="check_circle" color="positive"/>
              <q-icon v-else name="cancel" color="negative"/>
            </template>
          </li>
          <li>
            No spaces
            <template v-if="modelValue">
              <q-icon v-if="pwdHasNoWhiteSpace" name="check_circle" color="positive"/>
              <q-icon v-else name="cancel" color="negative"/>
            </template>
          </li>
        </ul>
      </CustomTooltip>
    </template>
  </q-input>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
export default {
  name: 'PasswordInput',
  components: { CustomTooltip },
  props: {
    modelValue: [String, null],
    label: {
      type: String,
      default: 'Password'
    },
    isValidate: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: true
    },
    customRules: [Array, null]
  },
  data () {
    return {
      isPwdShown: false
    }
  },
  computed: {
    rules () {
      if (this.customRules) {
        return this.customRules
      }
      if (!this.isRequired && !this.modelValue) {
        return null
      }
      if (this.isValidate) {
        return [
          (val) => this.has10Chars(val) || 'Password must be at least 10 characters long',
          (val) => this.hasLowercaseChar(val) || 'Password must have at least one lowercase letter',
          (val) => this.hasUppercaseChar(val) || 'Password must have at least one uppercase letter',
          (val) => this.hasNumber(val) || 'Password must have at least one number',
          (val) => this.hasSymbol(val) || 'Password must have at least symbol',
          (val) => this.hasNoWhiteSpace(val) || 'Password cannot have any spaces'
        ]
      }
      return [(val) => (val && val.length) || 'Password is required']
    },
    pwdHas10Chars () {
      return this.has10Chars(this.modelValue)
    },
    pwdHasLowercaseChar () {
      return this.hasLowercaseChar(this.modelValue)
    },
    pwdHasUppercaseChar () {
      return this.hasUppercaseChar(this.modelValue)
    },
    pwdHasNumber () {
      return this.hasNumber(this.modelValue)
    },
    pwdHasSymbol () {
      return this.hasSymbol(this.modelValue)
    },
    pwdHasNoWhiteSpace () {
      return this.hasNoWhiteSpace(this.modelValue)
    }
  },
  methods: {
    has10Chars (val) {
      return val && val.length >= 10
    },
    hasLowercaseChar (val) {
      return val && val.search(/[a-z]/) >= 0
    },
    hasUppercaseChar (val) {
      return val && val.search(/[A-Z]/) >= 0
    },
    hasNumber (val) {
      return val && val.search(/[0-9]/) >= 0
    },
    hasSymbol (val) {
      return val && val.search(/[^A-Za-z0-9]/) >= 0
    },
    hasNoWhiteSpace (val) {
      return val && val.search(/\s/) === -1
    }
  }
}
</script>
