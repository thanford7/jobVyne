<template>
  <div ref="calendarContainer">
    <div ref="calendar" class="calendly-inline-widget" style="min-width: 320px; height: 780px"></div>
  </div>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import { loadScript } from 'src/utils/load-script.js'

let CALENDAR_ID = 0

export default {
  name: 'CalendlyEmbed',
  props: {
    firstName: [String, null],
    lastName: [String, null],
    email: [String, null]
  },
  computed: {
    calendlyUrl () {
      return dataUtil.getUrlWithParams({
        path: 'https://calendly.com/jobvyne/30min',
        addParams: [
          { key: 'hide_event_type_details', val: 1 },
          { key: 'name', val: dataUtil.getFullName(this.firstName, this.lastName) },
          { key: 'email', val: this.email }
        ]
      })
    }
  },
  methods: {
    createCalendarDOM () {
      CALENDAR_ID++
      const calendar = document.createElement('iframe')
      calendar.id = `cal-${CALENDAR_ID}`
      calendar.setAttribute('src', this.calendlyUrl)
      calendar.setAttribute('height', '100%')
      calendar.setAttribute('width', '100%')
      calendar.setAttribute('frameBorder', '0')
      calendar.setAttribute('title', 'Calendly Scheduling Page')
      return calendar
    },
    getCalendarDOM () {
      return document.getElementById(`cal-${CALENDAR_ID}`)
    }
  },
  async created () {
    await loadScript('https://assets.calendly.com/assets/external/widget.js')
  },
  mounted () {
    this.$refs.calendar.appendChild(this.createCalendarDOM())
  },
  beforeUnmount () {
    this.getCalendarDOM().remove()
  }
}
</script>
