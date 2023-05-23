<template>
  <div>
    <template v-if="locations.length > condenseLocationLimit">
      <CustomTooltip>
        <template v-slot:icon>
          <q-chip
            color="grey-7" text-color="white" size="md" :icon="icon" :dense="isDense"
            class="ellipsis" title="Multiple locations"
          >
            Multiple locations&nbsp;
            <span v-if="utilStore.isUnderBreakPoint('md')">(press to view)</span>
            <span v-else>(hover to view)</span>
          </q-chip>
        </template>
        <ul>
          <li v-for="location in locations">
            {{ locationUtil.getFullLocation(location) }}
          </li>
        </ul>
      </CustomTooltip>
    </template>
    <template v-else-if="locations.length">
      <q-chip
        v-for="location in locations"
        color="grey-7" text-color="white" size="md" :icon="icon"
        :dense="isDense" class="ellipsis" :title="locationUtil.getFullLocation(location)"
      >
        {{ locationUtil.getFullLocation(location) }}
      </q-chip>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import locationUtil from 'src/utils/location.js'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'LocationChip',
  components: { CustomTooltip },
  props: {
    locations: Array,
    isDense: {
      type: Boolean,
      default: false
    },
    icon: {
      type: [String, null]
    },
    // The max locations to show before showing one chip with "Multiple locations"
    condenseLocationLimit: {
      type: Number,
      default: 1
    }
  },
  data () {
    return {
      locationUtil,
      utilStore: useUtilStore()
    }
  }
}
</script>
