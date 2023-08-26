<template>
  <q-table
    :loading="isLoading"
    :rows="users || []"
    :columns="userColumns"
    row-key="id"
    selection="multiple"
    v-model:selected="selectedUsers"
    :rows-per-page-options="[25]"
    v-model:pagination="pagination"
    :filter="userFilter"
    @request="fetchUsers"
  >
    <template v-slot:top>
      <div class="col-12">
        <div class="q-gutter-y-sm flex items-center">
          <q-btn-dropdown
            v-if="isAdminMode || authStore.getHasPermission(PERMISSION_NAMES.MANAGE_USER)"
            color="primary" label="User actions"
          >
            <q-list>
              <q-item clickable v-close-popup @click="openUserModal()">
                <q-item-section avatar>
                  <q-icon name="add"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Add user</q-item-label>
                </q-item-section>
              </q-item>
              <template v-if="selectedUsers && selectedUsers.length">
                <q-item clickable v-close-popup @click="openUserModal(selectedUsers)">
                  <q-item-section avatar>
                    <q-icon name="edit"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Modify {{ dataUtil.pluralize('user', selectedUsers.length) }}</q-item-label>
                  </q-item-section>
                </q-item>
                <q-item
                  v-if="deactivatedUserCount"
                  clickable v-close-popup @click="activateUsers(false)"
                >
                  <q-item-section avatar>
                    <q-icon name="power"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Re-activate {{
                        dataUtil.pluralize('user', deactivatedUserCount)
                      }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <q-item
                  v-if="activatedUserCount"
                  clickable v-close-popup @click="activateUsers(true)"
                >
                  <q-item-section avatar>
                    <q-icon name="power_off"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Deactivate {{
                        dataUtil.pluralize('user', activatedUserCount)
                      }}
                    </q-item-label>
                    <Tooltip>
                      User(s) will no longer be able to create links for your company. Any current links will
                      be re-directed to a general company page with all open jobs shown.
                    </Tooltip>
                  </q-item-section>
                </q-item>
                <q-item
                  v-if="hasNoSeatUserCount"
                  clickable v-close-popup @click="assignUserSeat(true)"
                >
                  <q-item-section avatar>
                    <q-icon name="person_add"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Assign employee seat {{
                        dataUtil.pluralize('user', hasNoSeatUserCount)
                      }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <q-item
                  v-if="hasSeatUserCount"
                  clickable v-close-popup @click="assignUserSeat(false)"
                >
                  <q-item-section avatar>
                    <q-icon name="person_remove"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Un-assign employee seat {{
                        dataUtil.pluralize('user', hasSeatUserCount)
                      }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <q-item
                  v-if="unapprovedUserCount"
                  clickable v-close-popup @click="approveUsers()"
                >
                  <q-item-section avatar>
                    <q-icon name="how_to_reg"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Approve permissions for {{
                        dataUtil.pluralize('user', unapprovedUserCount)
                      }}
                    </q-item-label>
                    <Tooltip>
                      If you don't want to approve all permissions for a specific user. Select the user, click
                      the "Modify user"
                      button and remove the permission from the list of permissions for that user.
                    </Tooltip>
                  </q-item-section>
                </q-item>
                <q-item
                  v-if="isAdminMode"
                  clickable v-close-popup @click="deleteUsers()"
                >
                  <q-item-section avatar>
                    <q-icon name="delete"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Delete {{
                        dataUtil.pluralize('user', selectedUsers.length)
                      }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-list>
          </q-btn-dropdown>
          <q-input
            class="q-ml-md-md"
            dense filled borderless debounce="300"
            v-model="userFilter.searchText" placeholder="Search"
          >
            <template v-slot:append>
              <q-icon name="search"/>
              <Tooltip>
                Search by first name, last name, or email
              </Tooltip>
            </template>
          </q-input>
          <div class="q-ml-md-md" style="display: inline-block">
            <a href="#" @click="clearUserFilter">Clear all filters</a>
          </div>
          <q-space/>
          <q-btn
            v-if="isAdminMode || authStore.getHasPermission(PERMISSION_NAMES.MANAGE_USER)"
            filled color="primary" label="Bulk upload users"
            @click="openBulkUploadUserDialog"
          />
        </div>
      </div>
    </template>
    <template v-slot:header-cell-is_approval_required="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Approval required"
                     :has-filter="userFilter.isApprovalRequired && userFilter.isApprovalRequired.length">
          <SelectYesNo label="Approval Required" v-model="userFilter.isApprovalRequired"/>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-employer_name="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Employer"
                     :has-filter="userFilter.employerIds && userFilter.employerIds.length">
          <SelectEmployer v-model="userFilter.employerIds" :is-multi="true"/>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-is_employer_deactivated="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Active"
                     :has-filter="userFilter.isActive && userFilter.isActive.length">
          <SelectYesNo label="Active" v-model="userFilter.isActive"/>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-has_employee_seat="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Has Seat"
                     :has-filter="userFilter.hasEmployeeSeat && userFilter.hasEmployeeSeat.length">
          <SelectYesNo label="Has Employee Seat" v-model="userFilter.hasEmployeeSeat"/>
        </TableFilter>
        <CustomTooltip v-if="!isAdminMode" icon_size="16px" :is_include_space="true">
          Your subscription supports {{ subscription.subscription_seats }} employee seats. If you have met your
          subscription limit,
          any additional employees that sign up will not have a seat. If an employee doesn't have a seat,
          all of their links will be redirected to the jobs page on your company website and their referrals
          will not be tracked.
          You can edit employees to reassign seats or update your subscription to support more employee
          seats.
        </CustomTooltip>
      </q-th>
    </template>
    <template v-slot:header-cell-is_employer_owner="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Account Owner"
                     :has-filter="userFilter.isAccountOwner && userFilter.isAccountOwner.length">
          <SelectYesNo label="Is Account Owner" v-model="userFilter.isAccountOwner"/>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-profession="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Departments"
                     :has-filter="userFilter.professionIds && userFilter.professionIds.length">
          <SelectJobProfession v-model="userFilter.professionIds" :is-multi="true" :is-required="false"/>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-user_type_bits="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="User type"
                     :has-filter="userFilter.userTypeBits && userFilter.userTypeBits.length">
          <SelectUserType
            v-model="userFilter.userTypeBits"
            :allowed-user-types="allowedUserTypes"
            :is-multi="true"
            :is-required="false"
          />
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-permission_groups>
      <q-th class="text-left">
        Permission groups
        <CustomTooltip icon_size="16px" :is_include_space="true">
          Some permission groups require approval from an employer user
          that has permission to manage other users.
          <div class="q-mt-sm">
            <q-chip label="Approved" color="positive" text-color="black"/>
            <q-chip label="Unapproved" color="negative" text-color="black"/>
          </div>
        </CustomTooltip>
        <TableFilter filter-name="Permission group"
                     :has-filter="userFilter.permissionGroupIds && userFilter.permissionGroupIds.length">
          <SelectPermissionGroup
            v-model="userFilter.permissionGroupIds"
            :is-required="false"
          />
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:body-cell-is_approval_required="props">
      <q-td class="text-center" :props="props">
        <CustomTooltip v-if="props.row.is_approval_required" :is_include_icon="false"
                       :is_include_space="true">
          <template v-slot:icon>
            <q-icon name="warning" color="warning" size="xs"/>
          </template>
          This user has one or more permissions which require approval from an authorized employer user.
          Select the user and click the "User Actions" dropdown button to approve or decline the
          permissions.
        </CustomTooltip>
        {{ props.value }}
      </q-td>
    </template>
    <template v-slot:body-cell-user_type_bits="props">
      <q-td key="user_type_bits">
        <q-chip
          v-for="userTypeName in userTypeUtil.getUserTypeList(
            props.row.user_type_bits, false, { excludeBits: (isAdminMode) ? 0 : USER_TYPES.Admin | USER_TYPES.Candidate }
          )"
          color="grey-7"
          text-color="white"
        >{{ userTypeName }}
        </q-chip>
      </q-td>
    </template>
    <template v-slot:body-cell-permission_groups="props">
      <q-td key="permission_groups">
        <template v-if="isAdminMode">
          <CustomTooltip v-for="group in props.value" :is_include_icon="false">
            <template v-slot:content>
              <q-chip
                :color="(group.is_approved) ? 'positive' : 'negative'"
                text-color="black"
              >
                {{ group.name }}
              </q-chip>
            </template>
            <div class="row text-small">{{ group.employer_name }}</div>
          </CustomTooltip>
        </template>
        <q-chip
          v-else
          v-for="group in props.value"
          :color="(group.is_approved) ? 'positive' : 'negative'"
          text-color="black"
        >
          {{ group.name }}
        </q-chip>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBulkUploadUsers from 'components/dialogs/DialogBulkUploadUsers.vue'
import DialogUser from 'components/dialogs/DialogUser.vue'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectJobProfession from 'components/inputs/SelectJobProfession.vue'
import SelectPermissionGroup from 'components/inputs/SelectPermissionGroup.vue'
import SelectUserType from 'components/inputs/SelectUserType.vue'
import SelectYesNo from 'components/inputs/SelectYesNo.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import Tooltip from 'components/Tooltip.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import userTypeUtil, {
  USER_TYPE_ADMIN, USER_TYPE_CANDIDATE,
  USER_TYPE_EMPLOYEE,
  USER_TYPE_EMPLOYER,
  USER_TYPE_INFLUENCER, USER_TYPES
} from 'src/utils/user-types.js'
import { useAdminStore } from 'stores/admin-store.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

const getAllUserPermissionGroups = (user) => {
  return Object.values(user.permission_groups_by_employer).reduce((allGroups, permissionGroups) => {
    return [...allGroups, ...permissionGroups]
  }, [])
}

const userFilterTemplate = {
  searchText: null,
  userTypeBits: null,
  permissionGroupIds: null,
  isApprovalRequired: null,
  isActive: null,
  isAccountOwner: null,
  employerIds: null,
  professionIds: null
}

const pagination = {
  sortBy: 'is_approval_required',
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: null
}

export default {
  name: 'UserTable',
  components: {
    SelectJobProfession,
    Tooltip,
    SelectEmployer,
    CustomTooltip,
    TableFilter,
    SelectPermissionGroup,
    SelectUserType,
    SelectYesNo
  },
  props: {
    isAdminMode: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoading: true,
      users: [],
      selectedUsers: [],
      subscription: {},
      userFilter: { ...userFilterTemplate },
      PERMISSION_NAMES: pagePermissionsUtil.PERMISSION_NAMES,
      dataUtil,
      userTypeUtil,
      USER_TYPES,
      pagination
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
    hasSeatUserCount () {
      if (!this.selectedUsers) {
        return
      }
      return this.selectedUsers.filter((user) => user.has_employee_seat).length
    },
    hasNoSeatUserCount () {
      if (!this.selectedUsers) {
        return
      }
      return this.selectedUsers.filter((user) => !user.has_employee_seat).length
    },
    unapprovedUserCount () {
      if (!this.selectedUsers) {
        return
      }
      return this.selectedUsers.filter((user) => user.is_approval_required).length
    },
    userColumns () {
      const cols = [
        {
          name: 'is_approval_required',
          field: 'is_approval_required',
          align: 'center',
          label: 'Approval required',
          format: (val) => (val) ? 'Yes' : 'No',
          sortable: true,
          classes: (row) => (row.is_approval_required) ? 'text-negative text-bold' : ''
        },
        {
          name: 'is_employer_deactivated',
          field: 'is_employer_deactivated',
          align: 'center',
          label: 'Active',
          format: (val) => (val) ? 'No' : 'Yes',
          sortable: true,
          classes: (row) => (row.is_employer_deactivated) ? 'text-negative text-bold' : ''
        },
        {
          name: 'has_employee_seat',
          field: 'has_employee_seat',
          align: 'center',
          label: 'Has Seat',
          format: (val) => (val) ? 'Yes' : 'No',
          sortable: true,
          classes: (row) => (row.has_employee_seat) ? '' : 'text-negative text-bold'
        },
        {
          name: 'is_employer_owner',
          field: 'is_employer_owner',
          align: 'center',
          label: 'Is Account Owner',
          format: (val) => (val) ? 'Yes' : 'No',
          sortable: true
        },
        { name: 'first_name', field: 'first_name', align: 'left', label: 'First name', sortable: true },
        { name: 'last_name', field: 'last_name', align: 'left', label: 'Last name', sortable: true },
        { name: 'email', field: 'email', align: 'left', label: 'Email', sortable: true },
        { name: 'profession', field: 'profession_name', align: 'left', label: 'Department', sortable: true },
        { name: 'user_type_bits', field: 'user_type_bits', align: 'left', label: 'User types' },
        { name: 'permission_groups', field: getAllUserPermissionGroups, align: 'left', label: 'Permission groups' },
        {
          name: 'created_dt',
          field: 'created_dt',
          align: 'left',
          label: 'Joined date',
          format: (val) => dateTimeUtil.getShortDate(val)
        }
      ]

      if (this.isAdminMode) {
        cols.splice(1, 0, {
          name: 'employer_name', field: 'employer_name', align: 'left', label: 'Employer', sortable: true
        })
      }

      return cols
    },
    allowedUserTypes () {
      let userTypes = [USER_TYPE_EMPLOYER, USER_TYPE_EMPLOYEE]
      if (this.isAdminMode) {
        // Employers shouldn't know if employees are also candidates (seeking jobs). Admins are irrelevant to employers
        // Influencer will be updated to be visible to employers once the functionality is added
        userTypes = [...userTypes, USER_TYPE_ADMIN, USER_TYPE_INFLUENCER, USER_TYPE_CANDIDATE]
      }
      return userTypes
    }
  },
  methods: {
    unselectUsers () {
      this.selectedUsers = []
    },
    async updateUserData () {
      this.unselectUsers()
      await this.fetchUsers()
      this.$emit('userUpdate')
    },
    async activateUsers (isDeactivate) {
      await this.$api.put('employer/user/activate/', getAjaxFormData({
        is_deactivate: isDeactivate,
        user_ids: this.selectedUsers.map((u) => u.id),
        employer_id: this.authStore.user.employer_id
      }))
      await this.updateUserData()
    },
    async assignUserSeat (isAssign) {
      await this.$api.put('employer/user/activate/', getAjaxFormData({
        is_assign: isAssign,
        user_ids: this.selectedUsers.map((u) => u.id),
        employer_id: this.authStore.user.employer_id
      }))
      await this.updateUserData()
    },
    async approveUsers () {
      await this.$api.put('employer/user/approve/', getAjaxFormData(
        { user_ids: this.selectedUsers.map((u) => u.id) }
      ))
      await this.updateUserData()
    },
    async deleteUsers () {
      openConfirmDialog(
        this.q,
        `Are you sure you want to delete ${dataUtil.pluralize('user', this.selectedUsers.length)}?`,
        {
          okFn: async () => {
            await this.$api.delete('employer/user/', {
              data: getAjaxFormData({ user_ids: this.selectedUsers.map((u) => u.id) })
            })
            await this.updateUserData()
          }
        }
      )
    },
    async fetchUsers ({ pagination = this.pagination, filter = this.userFilter } = {}) {
      this.isLoading = true
      await this.adminStore.setUsers(
        pagination.page,
        pagination.sortBy,
        pagination.descending,
        Object.assign(
          { employer_id: (this.isAdminMode) ? null : this.authStore.propUser.employer_id },
          filter || {}
        )
      )
      this.users = this.adminStore.paginatedUsers.users
      Object.assign(this.pagination, pagination)
      this.pagination.rowsNumber = this.adminStore.paginatedUsers.total_user_count
      this.isLoading = false
    },
    clearUserFilter () {
      this.userFilter = { ...userFilterTemplate }
    },
    openUserModal (users) {
      const cfg = {
        component: DialogUser,
        componentProps: { users, isAdmin: this.isAdminMode }
      }
      return this.q.dialog(cfg).onOk(async () => {
        this.unselectUsers()
        await this.fetchUsers()
      })
    },
    openBulkUploadUserDialog () {
      return this.q.dialog({
        component: DialogBulkUploadUsers,
        componentProps: { isAdminMode: this.isAdminMode }
      }).onOk(async () => {
        this.unselectUsers()
        await this.fetchUsers()
      })
    }
  },
  async mounted () {
    await this.authStore.setUser()
    await this.fetchUsers()
    if (!this.isAdminMode) {
      await this.employerStore.setEmployerSubscription(this.authStore.propUser.employer_id)
      this.subscription = this.employerStore.getEmployerSubscription(this.authStore.propUser.employer_id)
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      adminStore: useAdminStore(),
      employerStore: useEmployerStore(),
      q: useQuasar()
    }
  }
}
</script>
