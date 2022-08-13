<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="row q-gutter-y-sm">
    <div class="col-12">
      <SeparatorWithText>
        <q-btn-dropdown icon="add" :label="label" color="primary">
          <q-list>
            <q-item
              v-for="rule in rules"
              clickable v-close-popup @click="rule.isShown = !rule.isShown"
            >
              <q-item-section>
                {{ rule.title }}
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </SeparatorWithText>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.department)" class="col-12">
      <SelectJobDepartment v-model="formData.departments" @before-unmount="formData.departments = null"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.city)" class="col-12">
      <SelectJobCity v-model="formData.cities" @before-unmount="formData.cities = null"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.state)" class="col-12">
      <SelectJobState v-model="formData.states" @before-unmount="formData.states = null"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.country)" class="col-12">
      <SelectJobCountry v-model="formData.countries" @before-unmount="formData.countries = null"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.jobTitle)" class="col-12">
      <q-input filled label="Job titles" v-model="formData.job_titles_regex">
        <template v-slot:after>
          <CustomTooltip>
            Job titles uses a regular expression pattern, which will search for a substring match in each job title,
            case insensitive.
            Some common patterns that may be helpful:
            <ul>
              <li><code>engineer</code> | Will match job titles such as <code>software engineer</code> and <code>hardware
                engineer</code></li>
              <li><code>product|software</code> | Will match job titles such as <code>product manager</code> and <code>software
                engineer</code></li>
            </ul>
          </CustomTooltip>
        </template>
      </q-input>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SeparatorWithText from 'components/SeparatorWithText.vue'
import dataUtil from 'src/utils/data.js'

const FORM_TITLES = {
  department: 'Departments',
  city: 'Cities',
  state: 'States',
  country: 'Countries',
  jobTitle: 'Job titles'
}

export default {
  name: 'CriteriaSection',
  components: {
    CustomTooltip,
    SelectJobCity,
    SelectJobDepartment,
    SelectJobState,
    SelectJobCountry,
    SeparatorWithText
  },
  props: {
    formData: Object,
    isInclusion: Boolean
  },
  data () {
    return {
      FORM_TITLES,
      rules: [
        { title: FORM_TITLES.department, isShown: !dataUtil.isEmpty(this.formData.departments) },
        { title: FORM_TITLES.city, isShown: !dataUtil.isEmpty(this.formData.cities) },
        { title: FORM_TITLES.state, isShown: !dataUtil.isEmpty(this.formData.states) },
        { title: FORM_TITLES.country, isShown: !dataUtil.isEmpty(this.formData.countries) },
        { title: FORM_TITLES.jobTitle, isShown: Boolean(this.formData.job_titles_regex) }
      ]
    }
  },
  watch: {
    rules: {
      handler () {
        const jobTitleRule = this.rules.find((f) => f.title === FORM_TITLES.jobTitle)
        if (!jobTitleRule.isShown) {
          // eslint-disable-next-line vue/no-mutating-props
          this.formData.job_titles_regex = null
        }
      },
      deep: true
    }
  },
  computed: {
    label () {
      return `Add ${(this.isInclusion) ? 'inclusion' : 'exclusion'} criteria`
    }
  },
  methods: {
    isFieldShown (title) {
      return this.rules.find((f) => f.title === title).isShown
    }
  }
}
</script>
