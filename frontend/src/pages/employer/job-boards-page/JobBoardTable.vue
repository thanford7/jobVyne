<template>
  <div class="row">
    <div class="col-12 q-pt-md">
      <q-table
        :rows="jobLinks"
        :columns="jobLinkColumns"
        :rows-per-page-options="[10, 25, 50]"
        :loading="isLoading"
      >
        <template v-slot:top>
          <div>
            <q-btn
              label="Create new job board"
              color="primary" ripple unelevated
              @click="openJobLinkDialog()"
            />
          </div>
        </template>
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width/>
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              {{ col.label }}
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td auto-width>
              <q-btn
                color="primary" outline round dense
                title="Edit job board" class="q-mr-xs"
                @click="openJobLinkDialog(props.row)" icon="edit"
              />
              <q-btn
                color="negative" outline round dense title="Delete job board"
                @click="deleteJobLink(props.row.id)" icon="delete"
              />
            </q-td>
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <template v-if="col.name === 'link_name'">
                {{ props.row.link_name }}
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>
                    <q-chip v-if="props.row.employer_id && props.row.owner_id" icon="person_add" dense>
                      Employee referral
                    </q-chip>
                  </template>
                  This is an employee referral link. You may be eligible for a referral bonus by sharing
                  this link.
                </CustomTooltip>
              </template>
              <template v-else-if="col.name === 'link'">
                <a :href="props.row.url" target="_blank">
                  Job board link
                </a>
                <q-btn
                  flat round dense icon="content_copy"
                  size="sm" @click="dataUtil.copyText(props.row.url)"
                />
              </template>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJobLink from 'components/dialogs/DialogJobLink.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useSocialStore } from 'stores/social-store.js'

const jobLinkColumns = [
  { name: 'link_name', field: 'link_name', align: 'left', label: 'Name', sortable: true },
  { name: 'link', field: 'id', align: 'left', label: 'Link' }
]

export default {
  name: 'JobBoardTable',
  components: { CustomTooltip },
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isLoading: false,
      jobLinks: [],
      jobLinkColumns,
      dataUtil
    }
  },
  methods: {
    async setSocialLinks (isForceRefresh) {
      this.isLoading = true
      const params = (this.isEmployer) ? { employerId: this.user.employer_id } : { userId: this.user.id }
      await this.socialStore.setSocialLinks({ ...params, isForceRefresh })
      this.jobLinks = this.socialStore.getSocialLinks(params)
      this.isLoading = false
    },
    async deleteJobLink (jobLinkId) {
      openConfirmDialog(this.q, 'Are you sure you want to delete this job board? The link will still continue to work, but it will no longer be displayed in reports', {
        okFn: async () => {
          await this.$api.delete('social-link/', {
            data: getAjaxFormData({ social_link_id: jobLinkId })
          })
          await this.setSocialLinks(true)
        }
      })
    },
    openJobLinkDialog (jobLink) {
      const componentProps = { jobLink }
      if (this.isEmployer) {
        componentProps.employerId = this.user.employer_id
      }
      return this.q.dialog({
        component: DialogJobLink,
        componentProps
      }).onOk(async () => {
        await this.setSocialLinks(true)
      })
    }
  },
  async mounted () {
    await this.setSocialLinks(false)
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      socialStore: useSocialStore(),
      user,
      q: useQuasar()
    }
  }
}
</script>
