<template>
  <div class="row">
    <div class="col-12 text-center">
      <q-btn-toggle
        v-model="formData.memberType"
        toggle-color="grey-7"
        :options="memberOptions"
      />
    </div>
    <div class="col-12 q-pt-lg q-px-md-md q-py-sm">
      <div class="row">
        <template v-if="isLoading">
          <div v-for="n in 3" class="col-12 col-md-4 col-lg-3 q-px-md-md" :data-times="n">
            <q-skeleton type="rect" style="height: 15vh;"/>
          </div>
        </template>
        <template v-else>
          <div
            v-for="member in members"
            class="col-12 col-md-4 col-lg-3 q-px-md-md"
          >
            <q-card>
              <div class="bg-grey-3 q-px-md q-py-xs">
                {{ communityUtil.get_member_type_label(member.member_type_bits) }}
              </div>
              <q-item class="border-bottom-1-gray-300">
                <q-item-section avatar>
                  <q-avatar>
                    <img :src="member.profile_picture_url">
                  </q-avatar>
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-bold">{{ member.first_name }} {{ member.last_name }}</q-item-label>
                  <q-item-label caption>
                    <a :href="member.linkedin_url" target="_blank">LinkedIn</a>
                    <template v-if="member.professional_site_url">
                      &nbsp;&nbsp;
                      <a :href="member.professional_site_url" target="_blank">
                        Professional Site
                      </a>
                    </template>
                    <template v-if="member.email">
                      &nbsp;&nbsp;
                      <a :href="`mailto: ${member.email}`">
                        {{ member.email }}
                      </a>
                    </template>
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-card-section>
                <template v-if="communityUtil.isJobSeeker(member.member_type_bits)">
                  <div class="text-bold q-mb-sm">Looking for jobs in:</div>
                  <q-chip v-if="member.job_search_level" icon="trending_up" color="orange-2" title="Job Level" dense>
                    {{ member.job_search_level.level }}
                  </q-chip>
                  <template v-if="member.job_search_industries">
                    <q-chip v-for="industry in member.job_search_industries" icon="business" color="teal-2"
                            title="Industry"
                            dense>
                      {{ industry.name }}
                    </q-chip>
                  </template>
                  <template v-if="member.job_search_professions">
                    <q-chip v-for="profession in member.job_search_professions" icon="work" color="light-blue-2"
                            title="Profession" dense>
                      {{ profession.name }}
                    </q-chip>
                  </template>
                  <template v-if="member.job_search_qualifications">
                    <div class="text-bold q-mt-sm border-top-1-gray-100 q-py-sm">
                      Qualifications
                    </div>
                    <div>{{ member.job_search_qualifications }}</div>
                  </template>
                </template>
                <template v-if="member.job_connections?.length">
                  <div
                    class="text-bold q-pt-sm"
                    :class="(communityUtil.isJobSeeker(member.member_type_bits)) ? 'q-mt-sm border-top-1-gray-100' : ''"
                  >
                    Job connections:
                  </div>
                  <q-list separator>
                    <q-item v-for="jobConnection in member.job_connections" clickable
                            @click="openUrlInNewTab(jobConnection.job_url)">
                      <q-item-section avatar>
                        <q-avatar rounded>
                          <img :src="jobConnection.job_employer_logo_url">
                        </q-avatar>
                      </q-item-section>
                      <q-item-section>
                        <div>
                          {{ jobConnection.job_title }}
                        </div>
                        <div>
                          {{ jobConnection.job_employer }}
                        </div>
                        <div class="text-small">
                          <q-chip v-if="jobConnection.is_job_remote" label="Remote" dense/>
                          {{ jobConnection.job_location }}
                        </div>
                      </q-item-section>
                      <q-item-section side top>
                        <template v-if="communityUtil.isConnectionHiringMember(jobConnection.connection_type)">
                          <q-item-label caption>
                            {{ CONNECTION_TYPES[jobConnection.connection_type].name }}
                          </q-item-label>
                          <div>
                            <q-icon v-for="n in 4" name="star" color="orange" :times="n"/>
                          </div>
                        </template>
                        <template v-if="communityUtil.isConnectionCurrentEmployee(jobConnection.connection_type)">
                          <q-item-label caption>
                            {{ CONNECTION_TYPES[jobConnection.connection_type].name }}
                          </q-item-label>
                          <div>
                            <q-icon v-for="n in 3" name="star" color="orange" :times="n"/>
                          </div>
                        </template>
                        <template v-if="communityUtil.isConnectionFormerEmployee(jobConnection.connection_type)">
                          <q-item-label caption>
                            {{ CONNECTION_TYPES[jobConnection.connection_type].name }}
                          </q-item-label>
                          <div>
                            <q-icon v-for="n in 2" name="star" color="orange" :times="n"/>
                          </div>
                        </template>
                        <template v-if="communityUtil.isConnectionKnowEmployee(jobConnection.connection_type)">
                          <q-item-label caption>
                            {{ CONNECTION_TYPES[jobConnection.connection_type].name }}
                          </q-item-label>
                          <div>
                            <q-icon v-for="n in 1" name="star" color="orange" :times="n"/>
                          </div>
                        </template>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </template>
              </q-card-section>
            </q-card>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import communityUtil, { CONNECTION_TYPES, MEMBER_TYPE_ALL, MEMBER_TYPES } from 'src/utils/community.js'
import { openUrlInNewTab } from 'src/utils/requests.js'
import { useCommunityStore } from 'stores/community-store.js'

/* eslint-disable vue/no-unused-vars */

export default {
  name: 'CommunitySection',
  props: {
    user: [Object, null],
    employer: [Object, null]
  },
  data () {
    return {
      isLoading: false,
      members: [],
      formData: {
        memberType: MEMBER_TYPES[MEMBER_TYPE_ALL].value
      },
      communityStore: useCommunityStore(),
      communityUtil,
      CONNECTION_TYPES,
      openUrlInNewTab
    }
  },
  computed: {
    memberOptions () {
      return Object.values(MEMBER_TYPES).map((mt) => {
        mt.label = mt.filter_label
        return mt
      })
    }
  },
  watch: {
    formData: {
      async handler () {
        await this.updateData()
      },
      deep: true
    }
  },
  methods: {
    async updateData () {
      this.isLoading = true
      const memberQueryParams = {
        professionKey: this.$route.params.professionKey,
        ...this.formData
      }
      if (this.employer) {
        memberQueryParams.employerId = this.employer.id
      }
      await this.communityStore.setMembers(memberQueryParams)
      this.members = this.communityStore.getMembers(memberQueryParams)
      this.isLoading = false
    }
  },
  async mounted () {
    await this.updateData()
  }
}
</script>
