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
    <q-list>
      <q-item v-for="(appData, idx) in appsByEmployee">
        <q-item-section avatar class="leader-rank-section q-pl-lg">
          <div class="leader-rank-section__rank text-h5 font-primary">
            {{ idx + 1 }}
          </div>
          <q-avatar color="primary" text-color="white">
            {{ getUserInitials(appData.apps[0]) }}
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <div class="flex">
            <div class="text-h5">
              {{ getUserName(appData.apps[0]) }}
            </div>
            <q-space/>
            <div class="text-h5">
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
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

export default {
  name: 'EmployeeLeaderBoard',
  components: { ChartSkeleton },
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
      return dataUtil.sortBy(appsByEmployeeList, { key: 'appCount', direction: -1 }, true)
    },
    dateTitle () {
      if (this.dateGroup === GROUPINGS.WEEK.key) {
        return `Week of ${dateTimeUtil.getShortDate(this.dateRange.from)}`
      } else if (this.dateGroup === GROUPINGS.MONTH.key) {
        return `Month of ${dateTimeUtil.getLongMonthYearFromDate(this.dateRange.from)}`
      } else {
        return `Up to ${dateTimeUtil.getShortDate(this.dateRange.to)}`
      }
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
    await this.authStore.setUser()
    await this.setChartRawData()
    this.isInitLoaded = true
  }
}
</script>

<style lang="scss" scoped>
.leader-rank-section {
  position: relative;

  &__rank {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
  }
}
</style>
