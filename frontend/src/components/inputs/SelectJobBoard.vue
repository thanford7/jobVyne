<template>
  <q-select
    :loading="isLoading"
    ref="select"
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    filled
    :options="socialLinks"
    option-value="id"
    option-label="link_name"
    label="Job board"
    :rules="rules"
  >
    <template v-slot:option="scope">
        <q-item
          v-bind="scope.itemProps"
          @click="scope.toggleOption(scope.opt)"
          class="bg-hover border-bottom-1-gray-100"
        >
          <q-item-section>
            <div class="text-bold">{{ scope.opt.link_name }}</div>
          </q-item-section>
          <q-item-section>
            <q-chip
              v-for="sub in scope.opt.job_subscriptions"
              dense color="blue-grey-7" text-color="white" size="13px"
            >
              {{ sub.title }}
            </q-chip>
          </q-item-section>
        </q-item>
    </template>
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data.js'
import locationUtil from 'src/utils/location.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'SelectJobBoard',
  props: {
    isEmployer: Boolean,
    modelValue: [Object, null],
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoading: true,
      socialLinks: [],
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
    }
  },
  async mounted () {
    const params = (this.isEmployer) ? { employerId: this.user.employer_id } : { userId: this.user.id }
    await this.socialStore.setSocialLinks(params)
    this.socialLinks = this.socialStore.getSocialLinks(params)

    // If a value is required and none is populated, use the default link
    if ((!this.modelValue || dataUtil.isEmpty(this.modelValue)) && this.isRequired) {
      const defaultLink = this.socialLinks.find((link) => link.is_default)
      this.$emit('update:model-value', defaultLink)
    }
    this.isLoading = false
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      user,
      socialStore: useSocialStore(),
      authStore: useAuthStore(),
      globalStore: useGlobalStore()
    }
  }
}
</script>
