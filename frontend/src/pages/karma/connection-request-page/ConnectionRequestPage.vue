<template>
  <q-page padding>
    <div class="q-pb-sm header border-bottom-2-gray-300">
      <div class="flex flex-center q-py-sm">
        <img src="~assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
      </div>
      <div class="self-center title">
        <h4 class="q-mb-none text-center">KARMA CONNECT</h4>
        <div class="text-center">Doing Good While Doing Good</div>
      </div>
    </div>
  </q-page>
</template>

<script>

export default {
  name: 'ConnectionRequestPage'
}
</script>

<style lang="scss" scoped>
  .header {
    display: grid;
    grid-template-columns: 25% 50% 25%;
    grid-column-gap: 5px;

    @media (max-width: 767px) {
      grid-template-columns: 1fr;
    }
  }
</style>
