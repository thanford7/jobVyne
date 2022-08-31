<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    filled use-input
    v-model="selectedLink"
    @update:model-value="emitModelValue"
    :options="socialLinks"
    autocomplete="platformName"
    @filter="filterLinks"
    option-value="id"
    option-label="platformName"
    label="Job link"
    :rules="rules"
  >
    <template v-slot:option="{ itemProps, opt, selected, toggleOption }">
      <BaseExpansionItem :title="opt.platformName">
        <q-item
          v-for="link in opt.platformLinks"
          v-bind="getOptionProps(itemProps)"
          :active="selected"
          class="bg-hover"
          @click="toggleOption(link)"
        >
          <div>
            <q-chip
              v-for="dept in link.departments"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              {{ dept.name }}
            </q-chip>
            <q-chip
              v-if="!link.departments.length"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              Departments: {{ globalStore.nullValueAnyStr }}
            </q-chip>
            <q-chip
              v-for="loc in locationUtil.getFormattedLocations(link)"
              dense :color="loc.color" text-color="white" size="13px"
            >
              {{ loc.name }}
            </q-chip>
            <q-chip
              v-if="!locationUtil.getFormattedLocations(link).length"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              Locations: {{ globalStore.nullValueAnyStr }}
            </q-chip>
          </div>
        </q-item>
      </BaseExpansionItem>
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
import BaseExpansionItem from 'components/BaseExpansionItem.vue'
import dataUtil from 'src/utils/data.js'
import locationUtil from 'src/utils/location.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'SelectJobLink',
  components: { BaseExpansionItem },
  props: {
    isEmitIdOnly: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      selectedLink: null,
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
      let links = this.socialStore.getSocialLinkFilters(this.authStore.propUser.id)
      links = Object.entries(dataUtil.groupBy(links, 'platform_name')).map(([platformName, platformLinks]) => {
        return {
          platformName: (platformName === 'null') ? this.globalStore.nullValueStr : platformName,
          platformLinks
        }
      })
      dataUtil.sortBy(links, 'platformName', true)
      if (!this.filterTxt || this.filterTxt === '') {
        return links
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return links.filter((l) => l.platformName && l.platformName.match(filterRegex))
    }
  },
  methods: {
    filterLinks (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    },
    emitModelValue (value) {
      if (this.isEmitIdOnly) {
        value = (value && value.length) ? value.map(v => v.id) : value
      }
      this.$emit('update:model-value', value)
    },
    getOptionProps (itemProps) {
      return dataUtil.omit(itemProps, ['id', 'onClick', 'onMousemove'])
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
