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
                    <q-btn v-if="authStore.getHasPermission(PERMISSION_NAMES.MANAGE_PERMISSION_GROUPS)" color="accent" icon="add" label="Add Group" @click="openEmployerAuthGroupDialog"/>
                  </div>
                  <q-separator/>
                  <q-scroll-area class="q-mt-sm" style="height: 20vh;">
                    <div v-for="userGroup in userGroups">
                      <div class="text-bold q-mb-sm">{{ userGroup.name }}</div>
                      <q-list>
                        <q-item
                          v-for="group in employerStore.permissionGroups.filter((g) => g.user_type_bit === userGroup.user_type_bit)"
                          clickable v-ripple
                          :active="selectedGroupId === group.id"
                          active-class="border-left-4-primary"
                          class="items-center"
                          @click="selectedGroupId = group.id"
                        >
                          <span :class="(selectedGroupId === group.id) ? 'text-bold' : ''">{{ group.name }}</span>
                          <q-chip v-if="getIsGroupReadOnly(group)" color="grey-7" text-color="white" size="sm">
                            Read Only
                          </q-chip>
                          <q-chip v-if="group.is_default" color="grey-7" text-color="white" size="sm"
                                  icon-right="help_outline">
                            Default
                            <q-tooltip class="info" style="font-size: 14px;" max-width="500px">
                              When a new {{ userGroup.name }} user joins JobVyne, they will be added to this permission
                              group
                            </q-tooltip>
                          </q-chip>
                        </q-item>
                      </q-list>
                    </div>
                  </q-scroll-area>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12">
              <q-card v-if="selectedGroup">
                <q-card-section>
                  <div class="q-mb-sm">
                    <div class="flex q-mb-sm">
                      <div class="text-h6">
                        Permissions for {{ selectedGroup.name }} Group
                      </div>
                      <q-space/>
                      <div>
                        <q-btn v-if="!selectedGroup.is_default && !getIsGroupReadOnly(selectedGroup)" dense color="primary" icon="star" label="Make default group" @click="setDefaultGroup"/>
                        <q-chip v-if="selectedGroup.is_default" color="grey-7" text-color="white" size="md" icon-right="help_outline">
                          Default
                        </q-chip>
                        <q-tooltip class="info" style="font-size: 14px;" max-width="500px">
                          When a new {{ getUserTypeNameFromBit(selectedGroup.user_type_bit) }} user joins JobVyne, they will be added to this permission
                          group
                        </q-tooltip>
                      </div>
                    </div>
                    <div v-if="getIsGroupReadOnly(selectedGroup)" class="bg-warning q-pl-sm">
                      Read Only
                      <CustomTooltip :is_include_space="false">
                        <template v-slot:icon>
                          <q-icon class="self-center" name="info" size="18px" color="grey-8"/>
                        </template>
                        <span v-if="selectedGroup.can_edit">
                          General permission groups can't be edited. Create a new custom permission group if you want to
                          make changes.
                        </span>
                        <span v-else>
                          You do not have the appropriate permissions to edit this group
                        </span>
                      </CustomTooltip>
                    </div>
                  </div>
                  <q-separator/>
                  <q-list>
                    <q-item
                      v-for="perm in selectedGroupPermissions"
                      tag="label"
                      :v-ripple="selectedGroup.can_edit"
                      :clickable="selectedGroup.can_edit"
                    >
                      <q-item-section>
                        <q-item-label>{{ perm.name }}</q-item-label>
                        <q-item-label caption>{{ perm.description }}</q-item-label>
                      </q-item-section>
                      <q-item-section avatar>
                        <q-toggle :disable="!selectedGroup.can_edit" v-model="perm.is_permitted"/>
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
import {
  PERMISSION_NAMES,
  useAuthStore,
  USER_TYPE_EMPLOYEE,
  USER_TYPE_EMPLOYER,
  USER_TYPES
} from 'stores/auth-store'
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
      selectedGroupId: null,
      userGroups: [USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE].map((userType) => {
        return {
          name: userType,
          user_type_bit: USER_TYPES[userType]
        }
      }),
      PERMISSION_NAMES
    }
  },
  computed: {
    selectedGroup () {
      if (!this.selectedGroupId) {
        return null
      }
      return this.employerStore.permissionGroups.find((group) => group.id === this.selectedGroupId)
    },
    selectedGroupPermissions () {
      if (!this.selectedGroup) {
        return null
      }
      return this.selectedGroup.permissions.filter((p) => p.user_type_bits & this.selectedGroup.user_type_bit)
    }
  },
  methods: {
    getIsGroupReadOnly (group) {
      return !group.employer_id || !group.can_edit
    },
    getUserTypeNameFromBit (userTypeBit) {
      for (const [name, bit] of Object.entries(USER_TYPES)) {
        if (bit === userTypeBit) {
          return name
        }
      }
    },
    setDefaultGroup () {
      // TODO
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
