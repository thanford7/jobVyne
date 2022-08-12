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
      <SelectJobDepartment v-model="formData.departments"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.city)" class="col-12">
      <SelectJobCity v-model="formData.cities"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.state)" class="col-12">
      <SelectJobState v-model="formData.states"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.country)" class="col-12">
      <SelectJobCountry v-model="formData.countries"/>
    </div>
    <div v-if="isFieldShown(FORM_TITLES.jobTitle)" class="col-12">
      <q-input filled title="Job titles" v-model="formData.job_titles_regex">
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

const FORM_TITLES = {
  department: 'Departments',
  city: 'Cities',
  state: 'States',
  country: 'Countries',
  jobTitle: 'Job titles'
}

export default {
  name: 'CriteriaSection',
  components: { CustomTooltip, SelectJobCity, SelectJobDepartment, SelectJobState, SelectJobCountry, SeparatorWithText },
  props: {
    formData: Object,
    label: String
  },
  data () {
    return {
      FORM_TITLES,
      rules: [
        { title: FORM_TITLES.department, isShown: false },
        { title: FORM_TITLES.city, isShown: false },
        { title: FORM_TITLES.state, isShown: false },
        { title: FORM_TITLES.country, isShown: false },
        { title: FORM_TITLES.jobTitle, isShown: false }
      ]
    }
  },
  methods: {
    isFieldShown (title) {
      return this.rules.find((f) => f.title === title).isShown
    }
  }
}
</script>
