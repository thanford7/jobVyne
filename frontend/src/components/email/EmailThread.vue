<template>
  <div v-if="emailThread.length">
    <div class="text-bold">{{ emailThread[0].subject }}</div>
    <q-list separator>
      <q-item v-for="email in emailThread" clickable v-ripple @click="email.isShowHtml = !email.isShowHtml">
        <q-item-section>
          <q-item-label caption>
            <span class="text-weight-bold">{{ email.from_address }}</span>
          </q-item-label>
          <div v-if="email.isShowHtml" class="q-my-md">
            <div v-html="email.body_html"></div>
          </div>
          <div v-else class="q-mt-sm">{{ dataUtil.truncateText(email.body, 100) }}</div>
          <template v-if="email.attachments?.length">
            <div class="text-small text-bold q-mt-sm">
              Attachments
            </div>
            <div class="text-small">
              <a v-for="attachment in email.attachments" :href="attachment.url" target="_blank" @click.stop>
                {{ attachment.name }}
              </a>
            </div>
          </template>
        </q-item-section>
        <q-item-section side top class="text-small">
          {{ dateTimeUtil.getDateTime(email.created_dt, { isIncludeSeconds: false }) }}
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'

export default {
  name: 'EmailThread',
  props: {
    emailThread: Array
  },
  data () {
    return {
      dataUtil,
      dateTimeUtil
    }
  }
}
</script>
