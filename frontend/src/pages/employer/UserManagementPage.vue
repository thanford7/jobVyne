<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="User management">
        Users can be added to multiple permission groups. Permissions are additive. For example, if a user is part of
        two groups and one has permission to add employees and the other does not, the user WILL have the ability to add
        employees.
      </PageHeader>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="groups" label="Group permissions"/>
        <q-tab name="users" label="Users"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="groups">
          <div class="row">
            <div class="col-12">
              <q-card class="q-mb-md">
                <q-card-section>
                  <div class="q-mb-sm flex">
                    <div class="text-h6">Groups</div>
                    <q-space/>
                    <q-btn color="accent" icon="add" label="Add Group" @click="openEmployerAuthGroupDialog"/>
                  </div>
                  <q-separator/>
                  <q-scroll-area class="q-mt-sm" style="height: 20vh;">
                    <q-list>
                      <q-item
                        v-for="group in employerStore.permissionGroups"
                        clickable v-ripple
                        :active="selectedGroupId === group.id"
                        active-class="border-left-4-primary text-bold"
                        @click="selectedGroupId = group.id"
                      >
                        {{ group.name }}
                      </q-item>
                    </q-list>
                  </q-scroll-area>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12">
              <q-card v-if="selectedGroup">
                <q-card-section>
                  <div class="q-mb-sm">
                    <div class="text-h6">
                      Permissions for {{ selectedGroup.name }} Group
                    </div>
                    <div v-if="selectedGroup.is_default" class="bg-warning q-pl-sm">
                      Read Only
                      <CustomTooltip :is_include_space="false">
                        <template v-slot:icon>
                          <q-icon class="self-center" name="info" size="18px" color="grey-8"/>
                        </template>
                        Default permission groups can't be edited. Create a new custom permission group if you want to
                        make changes.
                      </CustomTooltip>
                    </div>
                  </div>
                  <q-separator/>
                  <q-list>
                    <q-item
                      v-for="perm in selectedGroup.permissions"
                      tag="label"
                      :v-ripple="!selectedGroup.is_default"
                      :clickable="!selectedGroup.is_default"
                    >
                      <q-item-section>
                        <q-item-label>{{ perm.name }}</q-item-label>
                        <q-item-label caption>{{ perm.description }}</q-item-label>
                      </q-item-section>
                      <q-item-section avatar>
                        <q-toggle :disable="selectedGroup.is_default" v-model="perm.is_permitted"/>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="users">
          <div class="row">
            <div class="col-12"></div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useGlobalStore } from 'stores/global-store'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogEmployerAuthGroup from 'components/dialogs/DialogEmployerAuthGroup.vue'

export default {
  name: 'UserManagementPage',
  components: { CustomTooltip, PageHeader },
  data () {
    return {
      tab: 'groups',
      selectedGroupId: null
    }
  },
  computed: {
    selectedGroup () {
      if (!this.selectedGroupId) {
        return null
      }
      return this.employerStore.permissionGroups.find((group) => group.id === this.selectedGroupId)
    },
    authGroupScrollAreaHeight () {
      const width = window.innerWidth
      let scrollHeight
      if (width < 1440) {
        scrollHeight = '20vh'
      } else {
        scrollHeight = '60vh'
      }
      return `height: ${scrollHeight};`
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployerJobs(authStore.propUser.employer_id),
        employerStore.setEmployerPermissions()
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const employerStore = useEmployerStore()
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()

    const pageTitle = 'User Management'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    const $q = useQuasar()
    const openEmployerAuthGroupDialog = () => {
      return $q.dialog({
        component: DialogEmployerAuthGroup
      })
    }

    return { employerStore, authStore, globalStore, openEmployerAuthGroupDialog }
  },
  mounted () {
    this.selectedGroupId = this.employerStore.permissionGroups[0].id
  }
}
</script>

<style scoped>

</style>
