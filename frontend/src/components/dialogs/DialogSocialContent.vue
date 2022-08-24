<template>
  <DialogBase
    :base-title-text="`${(contentItem.id) ? 'Edit' : 'Create'} content item`"
    :primary-button-text="(!contentItem.id) ? 'Create' : 'Update'"
    :is-full-screen="true"
    @ok="saveContent"
  >
    <div class="row q-mt-md q-gutter-y-md">
      <div class="col-12 col-md-6 q-pr-md-sm">
        <q-input
          v-model="formData.content" type="textarea" filled
          label="Content"
          :hint="characterLengthText"
        />
      </div>
      <div class="col-12 col-md-6">
        <CollapsableCard :is-dense="true" flat bordered>
          <template v-slot:header-left>
            <span class="text-bold">Placeholder content</span>
            <CustomTooltip>
              This content will be filled in dynamically based on the link or
              job you choose to post
            </CustomTooltip>
          </template>
          <template v-slot:body>
            <div class="q-pa-sm">
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
                      @click="addPlaceholder(props.row.placeholder)"
                    />
                  </q-td>
                </template>
                <template v-slot:body-cell-example="props">
                  <q-td :props="props">
                    <div v-html="props.row.example"/>
                  </q-td>
                </template>
              </q-table>
            </div>
          </template>
        </CollapsableCard>
      </div>
    </div>
  </DialogBase>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useContentStore } from 'stores/content-store.js'

export default {
  name: 'DialogSocialContent',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CustomTooltip, CollapsableCard, DialogBase },
  props: {
    contentItem: {
      type: [Object, null],
      default: () => ({})
    },
    user: Object,
    isEmployer: Boolean
  },
  data () {
    return {
      formData: { ...this.contentItem },
      contentStore: null
    }
  },
  computed: {
    placeholderTableColumns () {
      return [
        { name: 'action', field: 'action', align: 'center' },
        { name: 'name', field: 'name', align: 'left', label: 'Name' },
        { name: 'placeholder', field: 'placeholder', align: 'left', label: 'Placeholder' },
        { name: 'example', field: 'example', align: 'left', label: 'Example' }
      ]
    },
    placeholderTableRows () {
      return [
        { name: 'Employer', placeholder: '{{employer}}', example: 'Google' },
        { name: 'Jobs page link', placeholder: '{{link}}', example: 'www.jobvyne.com/jobs-link/ad8audafdi' },
        {
          name: 'Open jobs list',
          placeholder: '{{jobs-list}}',
          example: '- Software engineer<br>- Product manager<br>- Market analyst'
        }
      ]
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
  methods: {
    addPlaceholder (placeholder) {
      if (!this.formData.content) {
        this.formData.content = ''
      }
      this.formData.content += placeholder
    },
    async saveContent () {
      const method = (this.formData.id) ? this.$api.put : this.$api.post
      const data = (this.isEmployer) ? { employer_id: this.user.employer_id } : { user_id: this.user.id }
      await method('social-content-item/', getAjaxFormData({
        ...data,
        ...this.formData
      }))
      await this.contentStore.setSocialContent(this.user.employer_id, this.user.id, true)
      this.$emit('ok')
    }
  },
  mounted () {
    this.contentStore = useContentStore()
  }
}
</script>
