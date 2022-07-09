<template>
  <div class="separator q-my-md">
    <q-separator/>
    <div class="separator__text">
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SeparatorWithText'
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
    left: 50%;
    background-color: $white;
    transform: translate(-50%, -50%);
  }
}
</style>
