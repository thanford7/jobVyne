<template>
  <div
    class="text-negative text-small"
    :class="{
      'q-py-sm': hasError,
      'shake-once': hasError && isShake
    }"
  >
    {{ errorText }}
  </div>
</template>

<script>
export default {
  name: 'ErrorCallout',
  props: {
    errorText: [String, null]
  },
  computed: {
    hasError () {
      return Boolean(this.errorText && this.errorText.length)
    }
  },
  data () {
    return {
      isShake: false
    }
  },
  methods: {
    shake () {
      this.isShake = true
      setTimeout(() => {
        this.isShake = false
      }, 1000)
    }
  }
}
</script>
