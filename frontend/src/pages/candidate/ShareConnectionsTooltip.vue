<template>
  <CustomTooltip :is_include_space="true" :icon_color_class="iconColor">
    <div>
      The purpose of JobVyne is to come together as a community and help each other find jobs and make new
      connections.
      When you share your connections, other JobVyne users can see information that would already be publicly
      available
      on LinkedIn:
    </div>
    <ul>
      <li>Name</li>
      <li>LinkedIn</li>
      <li>Employer</li>
      <li>Job Title</li>
      <li>Profession</li>
    </ul>
    <div>
      We DO NOT contact any of your connections or share any contact information with others.
    </div>
  </CustomTooltip>
</template>
<script>
import CustomTooltip from 'components/CustomTooltip.vue'

export default {
  name: 'ShareConnectionsTooltip',
  components: { CustomTooltip },
  props: {
    iconColor: {
      type: String,
      default: 'text-gray-500'
    }
  }
}
</script>
