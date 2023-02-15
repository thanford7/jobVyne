<template>
  <template v-if="locations.length > 1">
    <CustomTooltip>
      <template v-slot:icon>
        <q-chip
          color="grey-7" text-color="white" size="13px" dense
        >
          Multiple locations
        </q-chip>
      </template>
      <ul>
        <li v-for="location in locations">
          {{ locationUtil.getFullLocation(location) }}
        </li>
      </ul>
    </CustomTooltip>
  </template>
  <q-chip
    v-else-if="locations.length"
    dense
    color="grey-7"
    text-color="white"
    size="13px"
  >
    {{ locationUtil.getFullLocation(locations[0]) }}
  </q-chip>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import locationUtil from 'src/utils/location.js'

export default {
  name: 'LocationsCell',
  components: { CustomTooltip },
  props: {
    locations: Object
  },
  data () {
    return {
      locationUtil
    }
  }
}
</script>
