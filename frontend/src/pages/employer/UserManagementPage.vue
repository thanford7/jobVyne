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
        <q-tab name="users" label="Users"/>
        <q-tab name="groups" label="Group permissions"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="users">
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <q-card>
                <div class="row q-ml-sm q-py-sm q-pr-md">
                  <div class="text-h6">User filters</div>
                  <q-space/>
                  <q-btn
                    color="grey-7"
                    flat
                    dense
                    :icon="isUserFilterExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                    @click="isUserFilterExpanded = !isUserFilterExpanded"
                  />
                </div>
                <q-slide-transition>
                  <div v-show="isUserFilterExpanded" class="row">
                    <div class="col-12 col-md-4 q-pa-sm">
                      <q-input filled borderless debounce="300" v-model="userFilter.searchText" placeholder="Search">
                        <template v-slot:append>
                          <q-icon name="search"/>
                          <q-tooltip class="info" style="font-size: 14px;" max-width="500px">
                            Search by first name, last name, or email
                          </q-tooltip>
                        </template>
                      </q-input>
                    </div>
                    <div class="col-12 col-md-4 q-pa-sm">
                      <SelectUserType
                        v-model="userFilter.userTypeBitsList"
                        :is-multi="true"
                        :is-required="false"
                      />
                    </div>
                    <div class="col-12 col-md-4 q-pa-sm">
                      <SelectPermissionGroup
                        v-model="userFilter.permissionGroupIds"
                        :is-required="false"
                      />
                    </div>
                    <div class="q-pa-sm">
                      <a href="#" @click="clearUserFilter">Clear all</a>
                    </div>
                  </div>
                </q-slide-transition>
              </q-card>
            </div>
            <div class="col-12">
              <q-table
                :rows="employees || []"
                :columns="userColumns"
                row-key="id"
                :filter-method="employeeDataFilter"
                filter="userFilter"
                selection="multiple"
                v-model:selected="selectedUsers"
                :rows-per-page-options="[25, 50, 100]"
              >
                <template v-if="authStore.getHasPermission(PERMISSION_NAMES.MANAGE_USER)" v-slot:top>
                  <q-btn class="q-mr-sm" color="primary" icon="add" label="Add user" @click="openUserModal()"/>
                  <div v-if="selectedUsers && selectedUsers.length" class="q-gutter-x-sm">
                    <q-btn color="primary" icon="edit"
                           :label="`Modify ${dataUtil.pluralize('user', selectedUsers.length)}`"
                           @click="openUserModal(selectedUsers)"/>
                    <q-btn v-if="deactivatedUserCount" color="primary" icon="power"
                           :label="`Re-activate ${dataUtil.pluralize('user', deactivatedUserCount)}`"
                           @click="activateUsers(false)"/>
                    <div v-if="activatedUserCount" style="display: inline-block;">
                      <q-btn color="negative" icon="power_off"
                             :label="`De-activate ${dataUtil.pluralize('user', activatedUserCount)}`"
                             @click="activateUsers(true)"/>
                      <q-tooltip class="info" style="font-size: 14px;" max-width="500px">
                        User(s) will no longer be able to create links for your company. Any current links will be
                        re-directed
                        to a general company page with all open jobs shown.
                      </q-tooltip>
                    </div>
                  </div>
                </template>
                <template v-slot:body-cell-userTypeBits="props">
                  <q-td key="user_type_bits">
                    <q-chip
                      v-for="userTypeName in userTypeUtil.getUserTypeList(props.row.user_type_bits)"
                      color="grey-7"
                      text-color="white"
                    >{{ userTypeName }}
                    </q-chip>
                  </q-td>
                </template>
                <template v-slot:body-cell-permissionGroups="props">
                  <q-td key="permission_groups">
                    <q-chip
                      v-for="group in props.row.permission_groups"
                      color="grey-7"
                      text-color="white"
                    >{{ group.name }}
                    </q-chip>
                  </q-td>
                </template>
              </q-table>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="groups">
          <div class="row">
            <div class="col-12">
              <q-card class="q-mb-md">
                <q-card-section>
                  <div class="q-mb-sm flex">
                    <div class="text-h6">Groups</div>
                    <q-space/>
                    <q-btn v-if="authStore.getHasPermission(PERMISSION_NAMES.MANAGE_PERMISSION_GROUPS)" color="accent"
                           icon="add" label="Add Group" @click="openEmployerAuthGroupDialog"/>
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
                      <div class="q-gutter-x-sm">
                        <q-btn
                          v-if="!selectedGroup.is_default && !getIsGroupReadOnly(selectedGroup)"
                          dense
                          color="negative" icon="delete_outline" title="Delete group"
                          @click="deleteGroup"
                        >Delete group
                        </q-btn>
                        <div style="display: inline-block;">
                          <q-btn
                            v-if="!selectedGroup.is_default && !getIsGroupReadOnly(selectedGroup)"
                            dense
                            color="primary" icon="star" label="Make default group"
                            @click="setDefaultGroup"
                          />
                          <q-chip v-if="selectedGroup.is_default" color="grey-7" text-color="white" size="md"
                                  icon-right="help_outline">
                            Default
                          </q-chip>
                          <q-tooltip class="info" style="font-size: 14px;" max-width="500px">
                            When a new {{ userTypeUtil.getUserTypeNameFromBit(selectedGroup.user_type_bit) }} user joins
                            JobVyne, they
                            will be added to this permission
                            group
                          </q-tooltip>
                        </div>
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
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests'
import userTypeUtil, {
  PERMISSION_NAMES,
  USER_TYPE_EMPLOYEE,
  USER_TYPE_EMPLOYER,
  USER_TYPES
} from 'src/utils/user-types'
import dateTimeUtil from 'src/utils/datetime'
import dataUtil from 'src/utils/data'
import DialogUser from 'components/dialogs/DialogUser.vue'
import SelectUserType from 'components/inputs/SelectUserType.vue'
import SelectPermissionGroup from 'components/inputs/SelectPermissionGroup.vue'

const userColumns = [
  {
    name: 'is_employer_deactivated',
    field: 'is_employer_deactivated',
    align: 'center',
    label: 'Active',
    format: (val) => (val) ? 'No' : 'Yes',
    sortable: true
  },
  { name: 'first_name', field: 'first_name', align: 'left', label: 'First name', sortable: true },
  { name: 'last_name', field: 'last_name', align: 'left', label: 'Last name', sortable: true },
  { name: 'email', field: 'email', align: 'left', label: 'Email', sortable: true },
  { name: 'userTypeBits', field: 'user_type_bits', align: 'left', label: 'User types' },
  { name: 'permissionGroups', field: 'permission_groups', align: 'left', label: 'Permission groups' },
  { name: 'created_dt', field: 'created_dt', align: 'left', label: 'Joined date', format: dateTimeUtil.getShortDate }
]

const userFilterTemplate = {
  searchText: null,
  userTypeBitsList: null,
  permissionGroupIds: null
}

export default {
  name: 'UserManagementPage',
  components: { SelectPermissionGroup, SelectUserType, CustomTooltip, PageHeader },
  data () {
    return {
      tab: 'users',
      selectedGroupId: null,
      selectedUsers: [],
      userGroups: [USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE].map((userType) => {
        return {
          name: userType,
          user_type_bit: USER_TYPES[userType]
        }
      }),
      userColumns,
      userFilter: { ...userFilterTemplate },
      isUserFilterExpanded: true,
      dataUtil,
      userTypeUtil,
      dateTimeUtil,
      PERMISSION_NAMES
    }
  },
  computed: {
    activatedUserCount () {
      if (!this.selectedUsers) {
        return
      }
      return this.selectedUsers.filter((user) => !user.is_employer_deactivated).length
    },
    deactivatedUserCount () {
      if (!this.selectedUsers) {
        return
      }
      return this.selectedUsers.filter((user) => user.is_employer_deactivated).length
    },
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
    },
    employees () {
      return this.employerStore.employers[this.authStore.user.employer_id].employees
    }
  },
  methods: {
    getIsGroupReadOnly (group) {
      return !group.employer_id || !group.can_edit
    },
    deleteGroup () {
      const userType = userTypeUtil.getUserTypeNameFromBit(this.selectedGroup.user_type_bit)
      openConfirmDialog(
        this.$q,
        `Any ${userType} users that are part of the ${this.selectedGroup.name} group will be moved to the default group for ${userType} users. Are you sure you wish to proceed?`,
        {
          okFn: async () => {
            await this.$api.delete(`employer/permission/${this.selectedGroupId}/`)
            this.employerStore.setEmployer(this.authStore.user.employer_id, true)
            this.employerStore.setEmployerPermissions(true)
            this.authStore.setUser(true)
          }
        }
      )
    },
    unselectUsers () {
      this.selectedUsers = []
    },
    async activateUsers (isDeactivate) {
      await this.$api.put('employer/user/activate/', getAjaxFormData(
        { is_deactivate: isDeactivate, user_ids: this.selectedUsers.map((u) => u.id) }
      ))
      this.employerStore.setEmployer(this.authStore.user.employer_id, true)
      this.unselectUsers()
    },
    async setDefaultGroup () {
      await this.$api.put(
        `employer/permission/${this.selectedGroupId}/`,
        getAjaxFormData({ is_default: true })
      )
      this.employerStore.setEmployerPermissions(true)
      this.authStore.setUser(true)
    },
    openEmployerAuthGroupDialog () {
      return this.$q.dialog({
        component: DialogEmployerAuthGroup
      })
    },
    openUserModal (users) {
      const cfg = {
        component: DialogUser,
        componentProps: { users }
      }
      return this.$q.dialog(cfg).onOk(() => this.unselectUsers())
    },
    employeeDataFilter (rows) {
      const searchRegex = (this.userFilter.searchText && this.userFilter.searchText.length) ? new RegExp(`.*?${this.userFilter.searchText}.*?`, 'i') : null
      return rows.filter((employee) => {
        if (searchRegex && !(employee.first_name.match(searchRegex) || employee.last_name.match(searchRegex) || employee.email.match(searchRegex))) {
          return false
        }
        if (this.userFilter?.userTypeBitsList?.length) {
          const matchedBits = this.userFilter.userTypeBitsList.reduce((matchedBits, userTypeBit) => {
            matchedBits += userTypeBit & employee.user_type_bits
            return matchedBits
          }, 0)
          if (!matchedBits) {
            return false
          }
        }
        if (this.userFilter?.permissionGroupIds?.length) {
          const employeePermissionGroupIds = employee.permission_groups.map((p) => p.id)
          const intersection = dataUtil.getArrayIntersection(employeePermissionGroupIds, this.userFilter.permissionGroupIds)
          if (!intersection.length) {
            return false
          }
        }
        return true
      })
    },
    clearUserFilter () {
      this.userFilter = { ...userFilterTemplate }
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

    return { employerStore, authStore, globalStore, $q }
  },
  mounted () {
    this.selectedGroupId = this.employerStore.permissionGroups[0].id
  }
}
</script>

<style scoped>

</style>
