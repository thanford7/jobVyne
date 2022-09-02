<template>
 <BaseContentPage :is-employer="true">
   <template v-slot:subheader>
     All posts and content are accessible to your employees. Create templates so
     employees can easily share content with their social networks.
   </template>
 </BaseContentPage>
</template>

<script>
import BaseContentPage from 'pages/content-page/BaseContentPage.vue'

export default {
  name: 'ContentPage',
  components: { BaseContentPage }
}
</script>
