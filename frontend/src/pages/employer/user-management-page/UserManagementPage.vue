<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="User management">
        <div>
          <q-icon name="info" size="24px"/>
          {{ dataUtil.pluralize('employee seat', subscription.active_employees) }}
          assigned out of {{ subscription.subscription_seats }}
        </div>
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
        <q-tab name="users" label="Users"/>
        <q-tab name="groups" label="Group permissions"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="users">
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <UserTable @userUpdate="updateSubscriptionData(true)"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="groups">
          <div class="row q-gutter-y-md">
            <div class="col-12 callout-card">
              Users can be added to multiple permission groups. Permissions are additive. For example, if a user is part of
              two groups and one has permission to add employees and the other does not, the user WILL have the ability to add
              employees.
            </div>
            <div class="col-12 q-pt-md">
              <q-card class="q-mb-md">
                <q-card-section>
                  <div class="q-mb-sm flex">
                    <div class="text-h6">Groups</div>
                    <q-space/>
                    <q-btn v-if="authStore.getHasPermission(PERMISSION_NAMES.MANAGE_PERMISSION_GROUPS)" color="accent"
                           icon="add" ripple label="Add Group" @click="openEmployerAuthGroupDialog"/>
                  </div>
                  <q-separator/>
                  <q-scroll-area class="q-mt-sm" style="height: 20vh;">
                    <div v-for="userGroup in userGroups">
                      <div class="text-bold q-mb-sm">{{ userGroup.name }}</div>
                      <q-list>
                        <q-item
                          v-for="group in permissionGroups.filter((g) => g.user_type_bit === userGroup.user_type_bit)"
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
                            <Tooltip>
                              When a new {{ userGroup.name }} user joins JobVyne, they will be added to this permission
                              group
                            </Tooltip>
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
                      <div class="q-gutter-x-sm">
                        <q-btn
                          v-if="!getIsGroupReadOnly(selectedGroup) && hasSelectedGroupPermissionsChanged"
                          dense ripple
                          color="primary" icon="save" label="Save changes"
                          @click="saveGroup"
                        />
                        <div style="display: inline-block;">
                          <q-btn
                            v-if="!selectedGroup.is_default && !getIsGroupReadOnly(selectedGroup)"
                            dense ripple
                            color="primary" icon="star" label="Make default"
                            @click="setDefaultGroup"
                          />
                          <q-chip v-if="selectedGroup.is_default" color="grey-7" text-color="white" size="md"
                                  icon-right="help_outline">
                            Default
                          </q-chip>
                          <Tooltip>
                            When a new {{ userTypeUtil.getUserTypeNameFromBit(selectedGroup.user_type_bit) }} user joins
                            JobVyne, they
                            will be added to this permission
                            group
                          </Tooltip>
                        </div>
                        <q-btn
                          v-if="!selectedGroup.is_default && !getIsGroupReadOnly(selectedGroup)"
                          dense ripple
                          color="negative" icon="delete_outline" title="Delete group"
                          @click="deleteGroup"
                        >Delete
                        </q-btn>
                      </div>
                    </div>
                    <div v-if="getIsGroupReadOnly(selectedGroup)" class="bg-warning q-pl-sm">
                      Read Only
                      <CustomTooltip>
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
                      :disable="!selectedGroup.can_edit"
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
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import Tooltip from 'components/Tooltip.vue'
import UserTable from 'pages/employer/user-management-page/UserTable.vue'
import { useEmployerStore } from 'stores/employer-store.js'
import { useAuthStore } from 'stores/auth-store.js'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useGlobalStore } from 'stores/global-store.js'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogEmployerAuthGroup from 'components/dialogs/DialogEmployerAuthGroup.vue'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import userTypeUtil, {
  USER_TYPE_EMPLOYEE,
  USER_TYPE_EMPLOYER,
  USER_TYPES
} from 'src/utils/user-types.js'
import dateTimeUtil from 'src/utils/datetime.js'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'UserManagementPage',
  components: {
    Tooltip,
    UserTable,
    CustomTooltip,
    PageHeader
  },
  data () {
    return {
      tab: 'users',
      permissionGroups: [],
      selectedGroupId: null,
      userGroups: [USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE].map((userType) => {
        return {
          name: userType,
          user_type_bit: USER_TYPES[userType]
        }
      }),
      subscription: {},
      dataUtil,
      userTypeUtil,
      dateTimeUtil,
      PERMISSION_NAMES: pagePermissionsUtil.PERMISSION_NAMES,
      USER_TYPE_EMPLOYER,
      USER_TYPE_EMPLOYEE,
      employerStore: useEmployerStore(),
      authStore: useAuthStore(),
      q: useQuasar()
    }
  },
  computed: {
    selectedGroup () {
      if (!this.selectedGroupId) {
        return null
      }
      return this.permissionGroups.find((group) => group.id === this.selectedGroupId)
    },
    selectedGroupPermissions () {
      if (!this.selectedGroup) {
        return null
      }
      const relevantPermissions = this.selectedGroup.permissions.filter((p) => p.user_type_bits & this.selectedGroup.user_type_bit)

      // Copy the starting permissions so we can check for changes
      if (!this.selectedGroup.currentPermissions) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.selectedGroup.currentPermissions = dataUtil.deepCopy(relevantPermissions)
      }
      return relevantPermissions
    },
    hasSelectedGroupPermissionsChanged () {
      if (!this.selectedGroup || !this.selectedGroup.currentPermissions) {
        return false
      }
      for (const permission of this.selectedGroup.currentPermissions) {
        const comparisonPermission = this.selectedGroup.permissions.find((p) => p.id === permission.id)
        if (permission.is_permitted !== comparisonPermission.is_permitted) {
          return true
        }
      }
      return false
    }
  },
  methods: {
    async updateSubscriptionData (isForceRefresh) {
      await this.employerStore.setEmployerSubscription(this.authStore.user.employer_id, isForceRefresh)
      this.subscription = this.employerStore.getEmployerSubscription(this.authStore.user.employer_id)
    },
    async updateEmployerPermissionData (isForceRefresh) {
      await this.employerStore.setEmployerPermissions(this.authStore.user.employer_id, isForceRefresh)
      this.permissionGroups = this.employerStore.getEmployerPermissions(this.authStore.user.employer_id)
    },
    getIsGroupReadOnly (group) {
      return !group.employer_id || !group.can_edit
    },
    deleteGroup () {
      const userType = userTypeUtil.getUserTypeNameFromBit(this.selectedGroup.user_type_bit)
      openConfirmDialog(
        this.q,
        `Any ${userType} users that are part of the ${this.selectedGroup.name} group will be moved to the default group for ${userType} users. Are you sure you wish to proceed?`,
        {
          okFn: async () => {
            await this.$api.delete(`employer/permission/${this.selectedGroupId}/`)
            await this.employerStore.setEmployer(this.authStore.user.employer_id, true)
            await this.updateEmployerPermissionData(true)
            await this.authStore.setUser(true)
          }
        }
      )
    },
    async setDefaultGroup () {
      await this.$api.put(
        `employer/permission/${this.selectedGroupId}/`,
        getAjaxFormData({ is_default: true })
      )
      await this.updateEmployerPermissionData(true)
      await this.authStore.setUser(true)
    },
    async saveGroup () {
      await this.$api.put(
        `employer/permission/${this.selectedGroupId}/`,
        getAjaxFormData({ permissions: this.selectedGroup.permissions })
      )
      await this.updateEmployerPermissionData(true)
      await this.authStore.setUser(true)
    },
    openEmployerAuthGroupDialog () {
      return this.q.dialog({
        component: DialogEmployerAuthGroup
      }).onOk((groupId) => {
        this.selectedGroupId = groupId
      })
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'User Management'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  },
  async mounted () {
    Loading.show()

    await this.authStore.setUser().then(() => {
      const employerId = this.authStore.propUser.employer_id
      return Promise.all([
        this.employerStore.setEmployer(employerId),
        this.employerStore.setEmployerJobs(employerId),
        this.updateEmployerPermissionData(false),
        this.updateSubscriptionData(false)
      ])
    }).finally(() => {
      Loading.hide()
    })
    this.selectedGroupId = this.permissionGroups[0].id
  }
}
</script>

<style scoped>

</style>
