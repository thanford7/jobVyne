import dataUtil from 'src/utils/data.js'

class JobsUtil {
  filterJobs (formData, jobs) {
    const departmentIds = (formData.departments) ? formData.departments.map((department) => department.id) : []
    const cityIds = (formData.cities) ? formData.cities.map((city) => city.id) : []
    const stateIds = (formData.states) ? formData.states.map((state) => state.id) : []
    const countryIds = (formData.countries) ? formData.countries.map((country) => country.id) : []
    return jobs.filter((job) => {
      const jobCityIds = job.locations.map((l) => l.city_id)
      const jobStateIds = job.locations.map((l) => l.state_id)
      const jobCountryIds = job.locations.map((l) => l.country_id)
      if (formData.departments?.length && !departmentIds.includes(job.job_department_id)) {
        return false
      }
      if (formData.cities?.length && !dataUtil.getArrayIntersection(cityIds, jobCityIds).length) {
        return false
      }
      if (formData.states?.length && !dataUtil.getArrayIntersection(stateIds, jobStateIds).length) {
        return false
      }
      if (formData.countries?.length && !dataUtil.getArrayIntersection(countryIds, jobCountryIds).length) {
        return false
      }
      return true
    })
  }
}

const jobsUtil = new JobsUtil()
export default jobsUtil
