<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Feedback">
        We want to hear from you! If there is an issue, we will work to fix it as quickly as possible. If you have a
        feature request or product idea, we will consider it for our roadmap.
      </PageHeader>
      <FeedbackForm/>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import FeedbackForm from 'pages/feedback-page/FeedbackForm.vue'

export default {
  name: 'FeedbackPage',
  components: { FeedbackForm, PageHeader }
}
</script>
