<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <q-input
    filled
    :model-value="employerData.email_domains"
    @update:model-value="
    employerData.email_domains = $event"
    @blur="employerData.email_domains = getNormalizedEmailDomains(employerData.email_domains)"
    label="Permitted email domains"
    lazy-rules
    :rules="[ val => val && val.length > 0 || 'At least one email domain is required']"
  >
    <template v-slot:append>
      <CustomTooltip>
        Add a comma separated list of permitted email domains. Any user that signs up for JobVyne
        and has an email address with one of the permitted domains will be allowed to automatically
        be added to your employee referral program without further action from an administrator. Email
        domains are the last part of the email address after the "@". For example, the email domain for
        "jane@acme.org" is "acme.org". Only business email domains are allowed. Public domains such as
        "gmail.com" or "yahoo.com" are not permitted.
      </CustomTooltip>
    </template>
  </q-input>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'

const NOT_PERMITTED_DOMAINS = [
  'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com'
]

export default {
  name: 'InputPermittedEmailDomains',
  props: {
    employerData: Object
  },
  components: { CustomTooltip },
  methods: {
    getNormalizedEmailDomains (rawEmailDomains) {
      if (!rawEmailDomains) {
        return rawEmailDomains
      }
      let emailDomains = rawEmailDomains.trim().split(',')
      const domainRegex = /([0-9a-z-]+?\.[0-9a-z-]+)/ig
      emailDomains = emailDomains.reduce((domains, ed) => {
        ed = ed.trim()
        if (!ed || !ed.length) {
          return domains
        }
        const matchedDomainStrings = ed.match(domainRegex)
        if (!matchedDomainStrings || NOT_PERMITTED_DOMAINS.includes(ed)) {
          return domains
        }
        const lastMatch = matchedDomainStrings[matchedDomainStrings.length - 1]
        domains.push(lastMatch)
        return domains
      }, [])
      return emailDomains.join(',')
    }
  }
}
</script>
