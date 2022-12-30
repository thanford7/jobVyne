<template>
  <div>
    <q-field
      filled
      :model-value="modelValue"
      class="phone-container"
      lazy-rules
      :rules="[
        () => !isRequired || isValid || 'Please provide a valid phone number'
      ]"
    >
      <vue-tel-input
        :model-value="modelValue"
        @update:model-value="$emit('update:model-value', $event)"
        mode="international"
        :preferredCountries="['us', 'ca', 'gb']"
        :onlyCountries="[
          'ar','at','au','be','bg','bo','br','bs','bz','ca','ch','cl','cn','co',
          'cr','cu','de','dk','do','ec','ee','eg','er','es','fi','fr','gb','gr',
          'gt','gu','hk','hn','hr','id','ie','il','in','is','it','jm','jp','kp',
          'kr','lt','lu','lv','mx','ng','ni','nl','no','nz','pa','pe','ph','pl',
          'pr','pt','py','qa','ro','rs','sa','se','sg','si','sv','th','tw','ua',
          'us','uy','za'
        ]"
        :inputOptions="{
          placeholder: label || 'Phone number',
          autofocus: isAutoFocus
        }"
        :styleClasses="['phone']"
        :valid-characters-only="true"
        @validate="setValidity"
      />
    </q-field>
  </div>
</template>

<script>
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/dist/vue-tel-input.css'

export default {
  name: 'PhoneInput',
  components: { VueTelInput },
  props: {
    modelValue: [String, null],
    isRequired: Boolean,
    label: [String, null],
    isAutoFocus: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      phoneNumber: null,
      defaultCountry: 'us',
      isValid: false
    }
  },
  methods: {
    setValidity (phoneData) {
      this.isValid = phoneData.valid
    }
  },
  mounted () {
    //
  }
}
</script>

<style lang="scss">
.phone {
  border: 0;
  background-color: rgba(0, 0, 0, 0);
  width: 100%;
  font-family: inherit;

  & input {
    background-color: rgba(0, 0, 0, 0);
  }

  &:focus-within {
    box-shadow: none;
  }
}

.phone-container .q-field__control {
  padding: 0 12px 0 0;
}
</style>
