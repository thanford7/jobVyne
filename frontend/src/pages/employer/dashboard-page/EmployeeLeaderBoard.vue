<template>
  <div v-if="isInitLoaded" class="chart-container">
    <div class="text-bold q-pb-sm border-bottom-1-gray-300">
      Job Application Leaderboard
    </div>
    <div class="q-my-sm">
      <q-btn-toggle
        v-model="dateGroup"
        rounded unelevated
        color="grey-5"
        toggle-color="grey-8"
        :options="[
        { label: 'Week', value: GROUPINGS.WEEK.key },
        { label: 'Month', value: GROUPINGS.MONTH.key },
        { label: 'All Time', value: 'All' },
      ]"
      />
    </div>
    <div>
      {{ dateTitle }}
    </div>
    <q-list separator dense>
      <q-item v-for="(appData, idx) in appsByEmployee">
        <q-item-section avatar>
          <q-avatar v-if="getUserProfilePicUrl(appData.apps[0])">
            <img :src="getUserProfilePicUrl(appData.apps[0])">
          </q-avatar>
          <q-avatar v-else :style="getAvatarColorStyle()">
            {{ getUserInitials(appData.apps[0]) }}
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <div class="flex items-center">
            <div class="text-h6">
              {{ getUserName(appData.apps[0]) }}
            </div>
            <q-icon v-if="idx < 3" class="q-ml-sm" size="20px" name="emoji_events" :style="getAwardIconStyle(idx)"/>
            <q-space/>
            <div
              v-if="isEmployer"
              class="text-h6"
              @dblclick="openDataDialog(appData.apps)"
              style="cursor: pointer"
              title="Double click to view applications"
            >
              {{ appData.appCount }}
            </div>
            <div v-else class="text-h6">
              {{ appData.appCount }}
            </div>
          </div>
        </q-item-section>
      </q-item>
    </q-list>
    <q-spinner-ios
      class="chart-container__loading"
      v-if="isLoading"
      color="primary"
    />
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import ChartSkeleton from 'components/charts/ChartSkeleton.vue'
import DialogShowDataTable from 'components/dialogs/DialogShowDataTable.vue'
import { useQuasar } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

const TOP_EMPLOYEE_COUNT = 10

export default {
  name: 'EmployeeLeaderBoard',
  components: { ChartSkeleton },
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isInitLoaded: false,
      isLoading: false,
      chartRawData: null,
      dateGroup: GROUPINGS.WEEK.key,
      dateRange: this.getDateRange(GROUPINGS.WEEK.key),
      GROUPINGS
    }
  },
  computed: {
    appsByEmployee () {
      const groupedByEmployee = dataUtil.groupBy(this.chartRawData.applications, 'owner_id')
      const appsByEmployeeList = Object.values(groupedByEmployee).map((apps) => {
        return {
          appCount: apps.length,
          apps
        }
      })
      dataUtil.sortBy(appsByEmployeeList, { key: 'appCount', direction: -1 }, true)
      return appsByEmployeeList.slice(0, TOP_EMPLOYEE_COUNT)
    },
    dateTitle () {
      if (this.dateGroup === GROUPINGS.WEEK.key) {
        return `Week of ${dateTimeUtil.getShortDate(this.dateRange.from)}`
      } else if (this.dateGroup === GROUPINGS.MONTH.key) {
        return `Month of ${dateTimeUtil.getLongMonthYearFromDate(this.dateRange.from)}`
      } else {
        return `Up to ${dateTimeUtil.getShortDate(this.dateRange.to)}`
      }
    },
    employees () {
      const employees = this.employerStore.getEmployees(this.authStore.propUser.employer_id)
      if (!employees) {
        return {}
      }
      return employees.reduce((employeeMap, employee) => {
        employeeMap[employee.id] = employee
        return employeeMap
      }, {})
    }
  },
  watch: {
    dateGroup () {
      this.dateRange = this.getDateRange(this.dateGroup)
    },
    dateRange () {
      this.setChartRawData()
    }
  },
  methods: {
    getDateRange (dateGroup) {
      if (dateGroup === GROUPINGS.WEEK.key) {
        return {
          from: dateTimeUtil.getStartOfWeekDate(new Date(), { asString: false }),
          to: new Date()
        }
      } else if (dateGroup === GROUPINGS.MONTH.key) {
        return {
          from: dateTimeUtil.getStartOfMonthDate(new Date(), { asString: false }),
          to: new Date()
        }
      } else {
        return {
          from: null,
          to: new Date()
        }
      }
    },
    getAvatarColorStyle () {
      const backgroundColor = colorUtil.getRandomPastelColor()
      return { backgroundColor, color: colorUtil.getInvertedColor(backgroundColor) }
    },
    getAwardIconStyle (idx) {
      let backgroundColor
      if (idx === 0) {
        backgroundColor = '#d4af37'
      } else if (idx === 1) {
        backgroundColor = '#aaa9ad'
      } else {
        backgroundColor = '#b08d57'
      }
      return {
        backgroundColor,
        color: colorUtil.getInvertedColor(backgroundColor),
        borderRadius: '25px',
        padding: '4px'
      }
    },
    getUserInitials (app) {
      const firstInitial = (app?.owner_first_name?.length) ? dataUtil.capitalize(app.owner_first_name[0]) : ''
      const lastInital = (app?.owner_last_name?.length) ? dataUtil.capitalize(app.owner_last_name[0]) : ''
      return firstInitial + lastInital
    },
    getUserName (app) {
      const firstName = app.owner_first_name || ''
      const lastName = app.owner_last_name || ''
      return `${firstName} ${lastName}`
    },
    getUserProfilePicUrl (app) {
      const user = this.employees[app.owner_id] || {}
      return user.profile_picture_url
    },
    openDataDialog (apps) {
      return this.q.dialog({
        component: DialogShowDataTable,
        componentProps: { data: apps }
      })
    },
    async setChartRawData () {
      this.isLoading = true
      await this.dataStore.setSocialLinkPerformance(
        this.authStore.propUser.employer_id,
        this.dateRange.from,
        this.dateRange.to
      )
      this.isLoading = false
      this.chartRawData = this.dataStore.getSocialLinkPerformance(
        this.authStore.propUser.employer_id,
        this.dateRange.from,
        this.dateRange.to
      )
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.dataStore = useDataStore()
    this.employerStore = useEmployerStore()
    await this.authStore.setUser()
    await this.setChartRawData()
    await this.employerStore.setEmployees(this.authStore.propUser.employer_id)
    this.isInitLoaded = true
  },
  setup () {
    return { q: useQuasar() }
  }
}
</script>
