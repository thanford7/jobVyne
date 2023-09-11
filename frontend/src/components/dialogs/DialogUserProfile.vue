<template>
  <DialogBase
    ref="dialogRef"
    base-title-text="Welcome to JobVyne!"
  >
    <template v-slot:subTitle>Let's get to know each other a bit better</template>
    <div v-if="stepCount === 1">
      <q-form ref="profileForm" class="q-mt-sm q-gutter-y-sm">
        <q-input
          v-if="!user.first_name"
          filled
          v-model="profileFormData.first_name"
          label="First name"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'First name is required']"
        />
        <q-input
          v-if="!user.last_name"
          filled
          v-model="profileFormData.last_name"
          label="Last name"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Last name is required']"
        />
        <InputLinkedIn v-model="profileFormData.linkedin_url" :is-required="false"/>
        <InputURL v-model="profileFormData.professional_site_url" :is-required="false"
                  label-override="Portfolio URL"/>
        <q-input
          filled
          v-model="profileFormData.home_postal_code"
          label="Home postal code"
        >
          <template v-slot:after>
            <CustomTooltip>
              This helps us recommend jobs that are close to you
            </CustomTooltip>
          </template>
        </q-input>
        <q-input
          filled
          v-model="profileFormData.job_title"
          label="Job title"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Job title is required']"
        />
        <SelectJobProfession
          v-model="profileFormData.profession_id"
          label="Profession" class="q-mb-md"
          :is-required="false" :is-multi="false"
        />
      </q-form>
    </div>
    <div v-if="stepCount === 2">
      <div class="q-mb-md">Tell us a bit about the types of jobs you're looking for so we can suggest the most relevant ones</div>
      <q-form ref="preferenceForm" class="q-mt-sm q-gutter-y-sm">
        <SelectRemote v-model="preferencesFormData.work_remote_type_bit"/>
        <SelectJobProfession v-model="preferencesFormData.job_search_professions" :is-multi="true" :is-required="true"/>
        <SelectJobLevel v-model="preferencesFormData.job_search_levels" :is-multi="true" :is-required="true"/>
      </q-form>
    </div>
    <template v-slot:buttons>
      <q-btn v-if="stepCount > 1" flat color="gray-7" @click="stepCount += -1" label="Back" class="q-mr-sm"/>
      <q-btn v-if="stepCount !== 2" @click="advanceStepper()" color="accent" label="Continue" :loading="isSavingUserProfile"/>
      <q-btn
        v-else
        class="bg-accent"
        flat ripple text-color="white"
        label="Save preferences"
        :loading="isLoading"
        @click="saveJobPreferences()"
      />
    </template>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputLinkedIn from 'components/inputs/InputLinkedIn.vue'
import InputURL from 'components/inputs/InputURL.vue'
import SelectJobLevel from 'components/inputs/SelectJobLevel.vue'
import SelectJobProfession from 'components/inputs/SelectJobProfession.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import dataUtil from 'src/utils/data'
import formUtil from 'src/utils/form'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store'

export default {
  name: 'DialogUserProfile',
  extends: DialogBase,
  inheritAttrs: false,
  components: { SelectJobLevel, SelectRemote, InputURL, InputLinkedIn, SelectJobProfession, DialogBase },
  data () {
    return {
      stepCount: 1,
      user: null,
      profileFormData: {},
      preferencesFormData: {},
      dataUtil,
      formUtil,
      isSavingUserProfile: false
    }
  },
  methods: {
    async advanceStepper () {
      if (this.stepCount === 1) {
        const isGoodForm = await this.$refs.profileForm.validate()
        if (!isGoodForm) {
          return false
        }
        await this.saveUserProfile()
      }
      this.stepCount += 1
    },
    async saveJobPreferences () {
      const isGoodForm = await this.$refs.preferenceForm.validate()
      if (!isGoodForm) {
        return
      }
      await this.$api.put('user/profile/', getAjaxFormData(Object.assign({
        user_id: this.user.id
      }, this.preferencesFormData)))
      this.$refs.dialogRef.onDialogOK()
      this.$emit('ok')
    },
    async saveUserProfile () {
      this.isSavingUserProfile = true
      await this.$api.put('user/profile/', getAjaxFormData(Object.assign({
        user_id: this.user.id
      }, this.profileFormData)))
      this.isSavingUserProfile = false
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    this.user = authStore.propUser
    this.profileFormData = dataUtil.pick(this.user, [
      'first_name', 'last_name', 'linkedin_url', 'professional_site_url', 'job_title', 'profession_id'
    ])
  }
}
</script>
