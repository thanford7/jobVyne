<template>
  <div class="separator q-my-md">
    <q-separator/>
    <div
      class="separator__text"
      :class="(textPosition === 'center') ? 'separator__text-center' : 'separator__text-left'"
    >
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SeparatorWithText',
  props: {
    textPosition: {
      type: [String, null],
      default: 'center'
    }
  }
}
</script>

<style lang="scss" scoped>
.separator {
  height: 1em;
  position: relative;

  &__text {
    padding: 0 1em;
    position: absolute;
    top: 0;
    background-color: $white;
    &-center {
      left: 50%;
      transform: translate(-50%, -50%);
    }
    &-left {
      left: 0;
      transform: translateY(-50%);
    }
  }
}
</style>
