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
      <q-item v-for="(employeeData, idx) in employeesAppCount">
        <q-item-section avatar>
          <q-avatar v-if="employeeData.owner_picture_url">
            <img :src="employeeData.owner_picture_url">
          </q-avatar>
          <q-avatar v-else :style="getAvatarColorStyle()">
            {{ getUserInitials(employeeData) }}
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <div class="flex items-center">
            <div class="text-h6">
              {{ employeeData.owner_name }}
            </div>
            <q-icon v-if="idx < 3" class="q-ml-sm" size="20px" name="emoji_events" :style="getAwardIconStyle(idx)"/>
            <q-space/>
            <div
              v-if="isEmployer && false"
              class="text-h6"
              style="cursor: pointer"
              title="Double click to view applications"
            >
              {{ employeeData.count }}
            </div>
            <div v-else class="text-h6">
              {{ employeeData.count }}
            </div>
          </div>
        </q-item-section>
      </q-item>
      <q-item
        v-if="!employeesAppCount || !employeesAppCount.length"
        class="q-mt-sm"
      >
        <q-item-section avatar>
          <q-icon name="fa-solid fa-bed"/>
        </q-item-section>
        <q-item-section>
          <div class="row">
            <div class="col-12 text-bold">
              No employees on the board this week
            </div>
            <div class="col-12 text-bold">
              You could be the first...
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
import userUtil from 'src/utils/user.js'
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
    employeesAppCount () {
      dataUtil.sortBy(this.chartRawData, { key: 'count', direction: -1 }, true)
      return this.chartRawData.slice(0, TOP_EMPLOYEE_COUNT)
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
    getUserInitials (employeeData) {
      return userUtil.getUserInitials(employeeData, 'owner_first_name', 'owner_last_name')
    },
    openDataDialog (apps) {
      return this.q.dialog({
        component: DialogShowDataTable,
        componentProps: { data: apps }
      })
    },
    async setChartRawData () {
      this.isLoading = true
      this.chartRawData = await this.dataStore.getApplications(
        this.dateRange.from,
        this.dateRange.to,
        {
          employer_id: this.authStore.propUser.employer_id,
          group_by: JSON.stringify(['owner_name'])
        }
      )
      this.isLoading = false
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
