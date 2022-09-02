<template>
  <BaseContentPage :is-employer="false"/>
</template>

<script>
import BaseContentPage from 'pages/content-page/BaseContentPage.vue'
export default {
  name: 'ContentPage',
  components: { BaseContentPage }
}
</script>
