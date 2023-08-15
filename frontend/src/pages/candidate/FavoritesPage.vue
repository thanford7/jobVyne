<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Favorites"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            :loading="isLoading"
            :rows="userFavorites.employers"
            :columns="employerFavoriteColumns"
            :rows-per-page-options="[25]"
          >
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th auto-width class="text-left"></q-th>
                <q-th
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  <span>{{ col.label }}</span>
                </q-th>
              </q-tr>
            </template>
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td auto-width>
                  <q-btn
                    outline round dense icon="fas fa-store-slash" color="negative" class="q-mr-xs" size="12px"
                    title="Remove favorite"
                    @click="deleteEmployerFavorite(props.row)"
                  />
                </q-td>
                <q-td
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  <template v-if="col.name === 'employerName'">
                    <a :href="`/co/${props.row.employer_key}`" target="_blank" :title="col.value">
                      {{ dataUtil.truncateText(col.value, 20, { isWholeWord: false }) }}
                    </a>
                  </template>
                  <template v-else>
                    <span>{{ col.value }}</span>
                  </template>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </div>
      </div>
    </div>
  </q-page>
</template>
<script>
import PageHeader from 'components/PageHeader.vue'
import { useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useUserStore } from 'stores/user-store.js'

const employerFavoriteColumns = [
  {
    name: 'employerName',
    field: 'employer_name',
    align: 'left',
    label: 'Company',
    sortable: true
  },
  {
    name: 'jobCount',
    field: 'open_job_count',
    align: 'center',
    label: 'Open Jobs',
    sortable: true
  }
]

export default {
  name: 'FavoritesPage',
  components: { PageHeader },
  data () {
    return {
      isLoading: false,
      userFavorites: {},
      employerFavoriteColumns,
      user: null,
      authStore: useAuthStore(),
      userStore: useUserStore(),
      dataUtil,
      q: useQuasar()
    }
  },
  methods: {
    async updateData (isForceRefresh = true) {
      this.isLoading = true
      await this.userStore.setUserFavorites(this.user.id, { isForceRefresh })
      this.userFavorites = this.userStore.getUserFavorites(this.user.id)
      this.isLoading = false
    },
    async deleteEmployerFavorite (employerFavorite) {
      openConfirmDialog(
        this.q,
        `Are you sure you want to remove ${employerFavorite.employer_name} from your favorites?`,
        {
          okFn: async () => {
            await this.$api.delete('user/favorite/', {
              data: getAjaxFormData({ employer_id: employerFavorite.employer_id, user_id: this.user.id })
            })
            await this.updateData()
          }
        }
      )
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      this.user = this.authStore.propUser
      return Promise.all([
        this.updateData(false)
      ])
    })
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Favorites'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
