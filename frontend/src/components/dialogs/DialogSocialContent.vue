<template>
  <DialogBase
    ref="baseDialog"
    :base-title-text="titleText"
    :primary-button-text="btnText"
    :is-full-screen="true"
    :is-o-k-btn-enabled="isValidForm"
    :ok-btn-help-text="validationHelpText"
    @ok="save"
    @show="focusInput"
  >
    <div class="row q-mt-md q-gutter-y-md">
      <div class="col-12 col-md-6 q-pr-md-sm">
        <q-input
          ref="contentInput"
          v-model="formData.content" type="textarea" filled
          label="Content"
          :hint="characterLengthText"
        />
        <PostLiveView
          v-if="!isTemplate"
          :content="formData.content"
          :file="formData.employer_file || formData.user_file"
          :job-link="formData.jobLink"
          :max-char-count="platformCfg.characterLimit"
          @content-update="formData.formatted_content = $event"
        />
      </div>
      <div class="col-12 col-md-6 q-pl-md-sm border-left-1-gray-100">
        <BaseExpansionItem
          v-if="!isTemplate"
          :is-include-separator="false"
          title="Starting template" class="content-expansion"
        >
          <q-table
            dense flat
            :hide-header="true"
            :hide-bottom="true"
            :columns="templateTableColumns"
            :rows="templateTableRows"
          >
            <template v-slot:body-cell-action="props">
              <q-td>
                <q-btn
                  unelevated dense label="Add" color="grey-6"
                  @click="addContent(props.row.content)"
                />
              </q-td>
            </template>
          </q-table>
        </BaseExpansionItem>
        <BaseExpansionItem
          title="Placeholder content" class="content-expansion"
          :is-include-separator="false"
        >
          <template v-slot:header>
            <CustomTooltip>
              This content will be filled in dynamically based on the link or
              job you choose to post
            </CustomTooltip>
          </template>
          <q-table
            dense flat
            :hide-bottom="true"
            :columns="placeholderTableColumns"
            :rows="placeholderTableRows"
          >
            <template v-slot:body-cell-action="props">
              <q-td>
                <q-btn
                  unelevated dense label="Add" color="grey-6"
                  @click="addContent(props.row.placeholder)"
                />
              </q-td>
            </template>
          </q-table>
        </BaseExpansionItem>
        <template v-if="!isTemplate">
          <BaseExpansionItem
            title="Photos/Videos" class="content-expansion"
            :is-include-separator="false"
          >
            <SelectFiles
              ref="selectFiles"
              v-model:employer-file-ids="formData.employer_file"
              v-model:user-file-ids="formData.user_file"
              :file-type-keys="platformCfg.allowedMedia"
              :is-multi-select="platformCfg.isMultiMedia"
              :is-employer="false"
            >
              <template v-slot:after>
                <q-btn
                  unelevated ripple color="primary" stretch
                  class="h-100"
                  @click="openFileModal"
                >Add new
                </q-btn>
              </template>
            </SelectFiles>
          </BaseExpansionItem>
          <BaseExpansionItem
            title="Jobs link" class="content-expansion"
            :is-include-separator="false"
          >
            <SelectJobLink v-model="formData.jobLink" :is-required="true" :platform-filter="[platform.name]">
              <template v-slot:after>
                <q-btn
                  unelevated ripple color="primary" stretch
                  class="h-100"
                  @click="openSociaLinkModal"
                >Add new
                </q-btn>
              </template>
            </SelectJobLink>
          </BaseExpansionItem>
          <BaseExpansionItem
            :title="`Auto-post to ${platform.name}`" class="content-expansion"
            :is-include-separator="false"
          >
            <template v-slot:header>
              <CustomTooltip>
                Once you create this post, it will automatically be posted to the selected social accounts.
              </CustomTooltip>
            </template>
            <q-checkbox
              v-for="cred in socialAuthStore.socialCredentials[platform.name]"
              v-model="formData.post_accounts[cred.email]"
              :label="cred.email"
            />
            <div v-if="!socialAuthStore.socialCredentials[platform.name] || !socialAuthStore.socialCredentials[platform.name].length">
              You do not have a {{ platform.name }} account connected. Go to the
              <q-btn
                class="a-style"
                flat no-caps dense type="a"
                :to="{ name: 'employee-social-accounts' }"
                @click="closeDialog"
              >social accounts page</q-btn>
              for one-click set-up.
            </div>
          </BaseExpansionItem>
        </template>
      </div>
    </div>
  </DialogBase>
</template>

<script>
import BaseExpansionItem from 'components/BaseExpansionItem.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import DialogEmployerFile, { loadDialogEmployerFileDataFn } from 'components/dialogs/DialogEmployerFile.vue'
import DialogSocialLink from 'components/dialogs/DialogSocialLink.vue'
import DialogUserFile, { loadDialogUserFileDataFn } from 'components/dialogs/DialogUserFile.vue'
import SelectFiles from 'components/inputs/SelectFiles.vue'
import SelectJobLink from 'components/inputs/SelectJobLink.vue'
import PostLiveView from 'pages/employee/content-page/PostLiveView.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'

export const loadDialogSocialContentFn = () => {
  const contentStore = useContentStore()
  const socialAuthStore = useSocialAuthStore()
  const authStore = useAuthStore()
  return authStore.setUser().then(() => {
    return Promise.all([
      contentStore.setSocialContent(authStore.propUser.employer_id, authStore.propUser.id),
      socialAuthStore.setUserSocialCredentials()
    ])
  })
}

export const SOCIAL_CONTENT_PLACEHOLDERS = {
  EMPLOYER: '{{employer}}',
  JOB_LINK: '{{link}}',
  JOBS_LIST: '{{jobs-list}}'
}

export default {
  name: 'DialogSocialContent',
  extends: DialogBase,
  inheritAttrs: false,
  components: { PostLiveView, SelectJobLink, SelectFiles, BaseExpansionItem, CustomTooltip, DialogBase },
  props: {
    contentItem: {
      type: [Object, null],
      default: () => ({})
    },
    platform: [Object, null],
    user: Object,
    isEmployer: Boolean,
    isTemplate: Boolean
  },
  data () {
    return {
      formData: (this.contentItem) ? { ...this.contentItem, post_accounts: {} } : { post_accounts: {} },
      contentStore: null,
      socialAuthStore: null,
      FILE_TYPES
    }
  },
  computed: {
    titleText () {
      let text
      if (this.isTemplate) {
        text = 'template'
      } else {
        text = `${this.platform.name} post`
      }
      return `${this.btnText} ${text}`
    },
    btnText () {
      return (!this.contentItem.id) ? 'Create' : 'Update'
    },
    platformCfg () {
      if (this.isTemplate) {
        return
      }
      return socialUtil.platformCfgs[this.platform.name]
    },
    isValidForm () {
      return Boolean(
        this.formData.content && this.formData.content.length &&
        (this.isTemplate || this.formData.jobLink) &&
        (!this.platformCfg || this.formData.formatted_content.length <= this.platformCfg.characterLimit)
      )
    },
    validationHelpText () {
      if (this.isValidForm) {
        return null
      } else if (this.isTemplate) {
        return 'Template content is required'
      } else {
        let text = 'Content and jobs link are required'
        if (this.platformCfg.characterLimit) {
          text += `. Total character limit cannot exceed ${this.platformCfg.characterLimit} characters`
        }
        return text
      }
    },
    socialCredentials () {
      if (this.isTemplate || !this.socialAuthStore) {
        return null
      }
      return this.socialAuthStore.socialCredentials
    },
    placeholderTableColumns () {
      return [
        { name: 'action', field: 'action', align: 'center' },
        { name: 'name', field: 'name', align: 'left', label: 'Name' },
        { name: 'placeholder', field: 'placeholder', align: 'left', label: 'Placeholder' },
        { name: 'example', field: 'example', align: 'left', label: 'Example', style: 'white-space: pre-line;' }
      ]
    },
    placeholderTableRows () {
      return [
        { name: 'Employer', placeholder: SOCIAL_CONTENT_PLACEHOLDERS.EMPLOYER, example: 'Google' },
        {
          name: 'Jobs page link',
          placeholder: SOCIAL_CONTENT_PLACEHOLDERS.JOB_LINK,
          example: 'www.jobvyne.com/jobs-link/ad8audafdi'
        },
        {
          name: 'Open jobs list',
          placeholder: SOCIAL_CONTENT_PLACEHOLDERS.JOBS_LIST,
          example: '- Software engineer\n- Product manager\n- Market analyst'
        }
      ]
    },
    templateTableColumns () {
      return [
        { name: 'action', field: 'action', align: 'center' },
        { name: 'content', field: 'content', align: 'left', label: 'Template', classes: 'table-wrap' }
      ]
    },
    templateTableRows () {
      return this.contentStore.getSocialContent(this.user.employer_id, this.user.id)
    },
    characterLengthText () {
      const placeholderRegex = /\{\{.*?}}/
      let textWithoutPlaceholders
      if (this.formData.content) {
        textWithoutPlaceholders = this.formData.content.replace(placeholderRegex, '')
      } else {
        textWithoutPlaceholders = ''
      }
      const charLength = textWithoutPlaceholders.length
      return `At least ${dataUtil.pluralize('character', charLength)} (doesn't include placeholders)`
    }
  },
  watch: {
    socialCredentials () {
      if (!this.socialCredentials) {
        return
      }
      dataUtil.getForceArray(this.socialCredentials[this.platform.name]).forEach((cred) => {
        this.formData.post_accounts[cred.email] = false
      })
    }
  },
  methods: {
    addContent (content) {
      if (!this.formData.content) {
        this.formData.content = ''
      }
      this.formData.content += content
    },
    focusInput () {
      this.$refs.contentInput.focus()
    },
    async save () {
      if (this.isTemplate) {
        await this.saveTemplate()
      } else {
        await this.savePost()
      }
    },
    async savePost () {
      const method = (this.formData.id) ? this.$api.put : this.$api.post
      let data = (this.isEmployer) ? { employer_id: this.user.employer_id } : { user_id: this.user.id }
      data = Object.assign(data,
        dataUtil.pick(this.formData, ['content', 'formatted_content']),
        { platform_id: this.platform.id }
      )
      if (this.formData.employer_file) {
        data.employer_file_id = this.formData.employer_file.id
      } else if (this.formData.user_file) {
        data.user_file_id = this.formData.user_file.id
      }

      data.post_accounts = Object.entries(this.formData.post_accounts).reduce((data, [email, isShare]) => {
        if (!isShare) {
          return data
        }
        const cred = this.socialCredentials[this.platform.name].find((c) => c.email === email)
        data.push(cred)
        return data
      }, [])

      await method('social-post/', getAjaxFormData(data))
      if (this.isEmployer) {
        await this.contentStore.setSocialPosts(this.user.employer_id, null, 1, { isForceRefresh: true })
      } else {
        await this.contentStore.setSocialPosts(null, this.user.id, 1, { isForceRefresh: true })
      }
      await this.contentStore.setSocialContent(this.user.employer_id, this.user.id, true)
      this.$emit('ok')
    },
    async saveTemplate () {
      const method = (this.formData.id) ? this.$api.put : this.$api.post
      const data = (this.isEmployer) ? { employer_id: this.user.employer_id } : { user_id: this.user.id }
      await method('social-content-item/', getAjaxFormData({
        ...data,
        ...this.formData
      }))
      await this.contentStore.setSocialContent(this.user.employer_id, this.user.id, true)
      this.$emit('ok')
    },
    async openFileModal () {
      const cfg = {
        componentProps: { fileTypeKeys: [FILE_TYPES.IMAGE.key] }
      }
      if (this.isEmployer) {
        await loadDialogEmployerFileDataFn()
        cfg.component = DialogEmployerFile
      } else {
        await loadDialogUserFileDataFn()
        cfg.component = DialogUserFile
      }
      return this.q.dialog(cfg).onOk(() => {
        this.$refs.selectFiles.updateFiles()
      })
    },
    async openSociaLinkModal () {
      return this.q.dialog({
        component: DialogSocialLink,
        componentProps: {
          platform: this.platform
        }
      })
    },
    closeDialog () {
      this.$refs.baseDialog.$refs.dialogRef.hide()
    }
  },
  setup () {
    return {
      q: useQuasar()
    }
  },
  mounted () {
    this.contentStore = useContentStore()
    this.socialAuthStore = useSocialAuthStore()
  }
}
</script>

<style lang="scss" scoped>
.content-expansion .q-expansion-item__content {
  max-height: 20vh;
  overflow-y: scroll;
}
</style>
