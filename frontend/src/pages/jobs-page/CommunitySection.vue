<template>
  <div class="row">
    <div class="col-12 text-center">
      <q-btn-toggle
        v-model="formData.memberType"
        toggle-color="grey-7"
        :options="[
          {label: 'All members', value: 'all'},
          {label: 'Job seekers', value: 'job_seekers'},
          {label: 'Hiring managers', value: 'hiring_managers'}
        ]"
      />
    </div>
    <div class="col-12 q-pt-lg q-px-md-md">
      <div class="row">
        <q-card
          v-for="member in members"
          class="col-12 col-md-4 col-lg-3"
        >
          <q-item class="border-bottom-1-gray-300">
            <q-item-section avatar>
              <q-avatar>
                <img :src="member.profile_picture_url">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ member.first_name }} {{ member.last_name }}</q-item-label>
              <q-item-label caption>
                <a :href="member.linkedin_url" target="_blank">LinkedIn</a>
                <template v-if="member.professional_site_url">
                  &nbsp;&nbsp;<a :href="member.professional_site_url" target="_blank">Professional Site</a>
                </template>
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-card-section v-if="member.member_type === 'Job seeker'">
            <div class="text-bold q-mb-sm">Looking for jobs in:</div>
            <q-chip v-if="member.job_search_level" icon="trending_up" color="orange-2" title="Job Level" dense>
              {{ member.job_search_level.level }}
            </q-chip>
            <template v-if="member.job_search_industries">
              <q-chip v-for="industry in member.job_search_industries" icon="business" color="teal-2" title="Industry" dense>
                {{ industry.name }}
              </q-chip>
            </template>
            <template v-if="member.job_search_professions">
              <q-chip v-for="profession in member.job_search_professions" icon="work" color="light-blue-2" title="Profession" dense>
                {{ profession.name }}
              </q-chip>
            </template>
            <template v-if="member.job_search_qualifications">
              <div class="text-bold q-mt-sm border-top-1-gray-100 q-py-sm">
                Qualifications
              </div>
              <div>{{ member.job_search_qualifications }}</div>
            </template>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { useCommunityStore } from 'stores/community-store.js'

export default {
  name: 'CommunitySection',
  props: {
    user: [Object, null],
    employer: [Object, null]
  },
  data () {
    return {
      members: [],
      formData: {
        memberType: 'all',
        isIncludeHiringManagers: true,
        isIncludeJobSeekers: true,
        isIncludeMembers: true
      },
      communityStore: useCommunityStore()
    }
  },
  async mounted () {
    const memberQueryParams = {
      professionKey: this.$route.params.professionKey
    }
    if (this.employer) {
      memberQueryParams.employerId = this.employer.id
    }
    await this.communityStore.setMembers(this.memberType, memberQueryParams)
    this.members = this.communityStore.getMembers(this.memberType, memberQueryParams)
  }
}
</script>
