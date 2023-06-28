<template>
  <div v-if="isLoaded">
    <div v-for="socialLink in socialUtil.getSocialLinks(socialStore.platforms, socialLink)"
         style="display: inline-block">
      <template v-if="socialLink.is_displayed">
        <CustomTooltip :is_include_icon="false">
          <template v-slot:content>
            <q-chip clickable outline color="primary" @click="dataUtil.copyText(socialLink.socialLink)">
              <div class="flex items-center">
                <img :src="socialLink.logo" :alt="socialLink.name" style="height: 16px;">
              </div>
            </q-chip>
          </template>
          {{ socialLink.name }}
        </CustomTooltip>
      </template>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'
import socialUtil from 'src/utils/social.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'ReferralLinkButtons',
  components: { CustomTooltip },
  props: {
    socialLink: Object
  },
  data () {
    return {
      isLoaded: false,
      platforms: null,
      socialStore: null,
      dataUtil,
      socialUtil
    }
  },
  async mounted () {
    this.socialStore = useSocialStore()
    await this.socialStore.setPlatforms()
    this.isLoaded = true
  }
}
</script>
