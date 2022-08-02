<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Employer settings"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="style" label="Brand style"/>
        <q-tab name="security" label="Security"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="style">
          <div class="row q-gutter-y-md">
            <div class="col-12 q-gutter-x-sm">
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Undo" color="grey-6" icon="undo"
                @click="undoEmployerChanges"
              />
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Save" color="accent" icon="save"
                @click="saveEmployerChanges"
              />
            </div>
            <div class="col-12 col-md-6 q-pr-md-sm">
              <FileDisplayOrUpload
                ref="logoUpload"
                label="logo"
                :file-url="employerData.logo_url"
                :new-file="employerData[newLogoKey]"
                :new-file-key="newLogoKey"
                file-url-key="logo_url"
              >
                <template v-slot:fileInput>
                  <q-file
                    ref="newLogoUpload"
                    filled bottom-slots clearable
                    v-model="employerData[newLogoKey]"
                    label="Logo"
                    class="q-mb-none"
                    :accept="fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])"
                    lazy-rules="ondemand"
                    :rules="[val => val || 'A file is required']"
                    max-file-size="1000000"
                  />
                </template>
              </FileDisplayOrUpload>
            </div>
            <div class="col-12">
              <div class="row">
                <div class="col-12 q-mb-sm">
                  Brand colors
                  <CustomTooltip>
                    These will be the default colors used for the employer profile page. If none are provided,
                    the JobVyne default colors will be used.
                  </CustomTooltip>
                </div>
                <div class="col-12">
                  <div class="row q-gutter-md">
                    <ColorPicker
                      v-model="employerData.color_primary"
                      label="Primary color"
                    />
                    <ColorPicker
                      v-model="employerData.color_secondary"
                      label="Secondary color"
                    />
                    <ColorPicker
                      v-model="employerData.color_accent"
                      label="Accent color"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="security">
          <div class="row q-gutter-y-md">
            <div class="col-12 q-gutter-x-sm">
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Undo" color="grey-6" icon="undo"
                @click="undoEmployerChanges"
              />
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Save" color="accent" icon="save"
                @click="saveEmployerChanges"
              />
            </div>
            <div class="col-12 q-gutter-x-sm">
              <q-input
                filled
                :model-value="employerData.email_domains"
                @update:model-value="employerData.email_domains = $event"
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
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import ColorPicker from 'components/inputs/ColorPicker.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'SettingsPage',
  components: { CustomTooltip, ColorPicker, FileDisplayOrUpload, PageHeader },
  data () {
    return {
      tab: 'style',
      newLogoKey: 'logo',
      currentEmployerData: this.getEmployerDataCopy(),
      employerData: this.getEmployerDataCopy(),
      fileUtil,
      FILE_TYPES
    }
  },
  computed: {
    hasEmployerDataChanged () {
      return !dataUtil.isDeepEqual(this.currentEmployerData, this.employerData)
    }
  },
  methods: {
    getEmployerDataCopy () {
      return dataUtil.deepCopy(this.employerStore.getEmployer(this.user.employer_id))
    },
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
        if (!matchedDomainStrings) {
          return domains
        }
        const lastMatch = matchedDomainStrings[matchedDomainStrings.length - 1]
        domains.push(lastMatch)
        return domains
      }, [])
      return emailDomains.join(',')
    },
    async saveEmployerChanges () {
      const data = Object.assign(
        {},
        this.employerData,
        (this.$refs.logoUpload) ? this.$refs.logoUpload.getValues() : {}
      )

      // Make sure a logo is uploaded if existing logo is not being used
      if (
        this.$refs.logoUpload &&
        this.$refs.logoUpload.isUpload &&
        !this.$refs.newLogoUpload.validate()
      ) {
        return
      }
      await this.$api.put(
        `employer/${this.employerData.id}/`,
        getAjaxFormData(data, [this.newLogoKey])
      )
      await this.employerStore.setEmployer(this.user.employer_id, true)
      this.currentEmployerData = this.getEmployerDataCopy()
      this.employerData = this.getEmployerDataCopy()
    },
    undoEmployerChanges () {
      this.employerData = dataUtil.deepCopy(this.currentEmployerData)
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const globalStore = useGlobalStore()
    const pageTitle = 'Employer Settings Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore,
      employerStore,
      user
    }
  }
}
</script>
