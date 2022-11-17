<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    filled
    :options="socialLinks"
    option-value="id"
    label="Job link"
    :rules="rules"
  >
    <template v-slot:option="{ itemProps, opt, selected, toggleOption }">
        <q-item
          v-bind="itemProps"
          :active="selected"
          class="bg-hover"
          @click="toggleOption(opt)"
        >
          <div>
            <q-chip
              v-for="dept in opt.departments"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              {{ dept.name }}
            </q-chip>
            <q-chip
              v-if="!opt.departments.length"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              Departments: {{ globalStore.nullValueAnyStr }}
            </q-chip>
            <q-chip
              v-for="loc in locationUtil.getFormattedLocations(opt)"
              dense :color="loc.color" text-color="white" size="13px"
            >
              {{ loc.name }}
            </q-chip>
            <q-chip
              v-if="!locationUtil.getFormattedLocations(opt).length"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              Locations: {{ globalStore.nullValueAnyStr }}
            </q-chip>
          </div>
        </q-item>
    </template>
    <template v-slot:selected-item="{ opt, removeAtIndex, tabindex, index }">
      <q-chip
        removable
        @remove="removeAtIndex(index)"
        :tabindex="tabindex"
        class="text-small"
      >
        {{ socialUtil.getLinkTextDescription(opt) }}
      </q-chip>
    </template>
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import locationUtil from 'src/utils/location.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'SelectJobLink',
  props: {
    isRequired: {
      type: Boolean,
      default: false
    },
    platformName: {
      type: String
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      socialStore: null,
      authStore: null,
      globalStore: null,
      locationUtil,
      socialUtil
    }
  },
  computed: {
    rules () {
      if (!this.isRequired) {
        return []
      }
      return [
        (val) => val || 'Job link is required'
      ]
    },
    socialLinks () {
      return this.socialStore.getSocialLinkFilters(this.authStore.propUser.id).map((link) => {
        link.platformName = this.platformName
        return link
      })
    }
  },
  async mounted () {
    this.socialStore = useSocialStore()
    this.authStore = useAuthStore()
    this.globalStore = useGlobalStore()
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.socialStore.setSocialLinkFilters(this.authStore.propUser.id)
      ])
    })
    this.isLoaded = true
  }
}
</script>
