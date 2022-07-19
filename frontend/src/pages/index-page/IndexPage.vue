<template>
  <q-page>
    <div class="row justify-center q-mt-xl q-gutter-y-lg">
      <ResponsiveWidth class="q-px-md">
        <div class="row">
          <transition appear enter-active-class="animated slideInLeft">
            <div class="col-12 col-md-7 q-gutter-y-lg">
              <div class="rfs-h2 text-center text-bold font-primary">Turn your employees into your best recruiters</div>
              <div class="rfs-h6 text-center text-gray-700">
                Automate employee referrals and generate more meaningful connections with job seekers
              </div>
              <WaitlistSignUp class="q-px-lg"/>
            </div>
          </transition>
          <transition appear enter-active-class="animated slideInRight">
            <div class="col-12 col-md-5 q-pl-md-md q-pl-none q-mt-md q-mt-md-none">
              <div class="flex justify-center items-center" style="height: 100%">
                <img src="~assets/images/social-share.jpg" alt="Social sharing"
                     style="object-fit: scale-down; max-width: 100%">
              </div>
            </div>
          </transition>
        </div>
      </ResponsiveWidth>
      <div class="row justify-center bg-grey-2 w-100">
        <ResponsiveWidth class="q-gutter-y-xl q-px-md q-py-xl">
          <div class="rfs-h4 font-primary q-ml-md-xl">How it works</div>
          <q-intersection once style="min-height: 150px" transition="slide-right" :threshold="0.8"
                          transition-duration="1000">
            <HowItWorksItem
              header="JobVyne automatically integrates with your Applicant Tracking System
                to pull job posting information"
              :benefits="[
              'One click integration so you don\'t have to do any extra work to post jobs',
              'Job applications are automatically pushed to your ATS so you maintain one system of record'
            ]"
            >
              <template v-slot:icon>
                <q-img class="w-25" src="~assets/icons/integration.png" alt="iconAlt"/>
              </template>
            </HowItWorksItem>
          </q-intersection>
          <q-intersection once style="min-height: 150px" transition="slide-left" :threshold="0.7"
                          transition-duration="1000">
            <HowItWorksItem
              header="Employees generate unique links to post on their social media profiles"
              :benefits="[
              'Links are tracked by the creator (employee) and platform (e.g. LinkedIn) allowing you to analyze performance',
              'Links can be personalized to filter for specific job positions. For example, all product manager positions in the state of Washington'
            ]"
            >
              <template v-slot:icon>
                <q-img class="w-25" src="~assets/icons/social-sharing.png" alt="Social sharing"/>
              </template>
            </HowItWorksItem>
          </q-intersection>
          <q-intersection once style="min-height: 150px" transition="slide-right" :threshold="0.7"
                          transition-duration="1000">
            <HowItWorksItem
              header="Job seekers can view and apply for jobs by clicking on a JobVyne link"
              :benefits="[
              'Each link directs to a personalized page which includes all relevant jobs, company description, and information about the employee that created the link',
              'Each page is integrated with your ATS so applications are automatically pushed to a configurable stage in the application process (e.g. opportunity stage)'
            ]"
            >
              <template v-slot:icon>
                <q-img class="w-25" src="~assets/icons/job-search.png" alt="Job search"/>
              </template>
            </HowItWorksItem>
          </q-intersection>
          <q-intersection once style="min-height: 150px" transition="slide-left" :threshold="0.7"
                          transition-duration="1000">
            <HowItWorksItem
              header="JobVyne tracks the applications attributed to each employee and calculates
                which employees are eligible for referral bonuses"
              :benefits="[
              'Job applications are timestamped and attributed to the employee whose link was used. This creates a full audit process to determine which employee should receive a referral bonus',
              'Employers can analyze the performance of the referral program by employee, social platform, job position, etc.'
            ]"
            >
              <template v-slot:icon>
                <q-img class="w-25" src="~assets/icons/employee-money.png" alt="Employee financial tracking"/>
              </template>
            </HowItWorksItem>
          </q-intersection>
        </ResponsiveWidth>
      </div>
      <ResponsiveWidth class="q-px-md q-py-lg">
        <div class="rfs-h4 font-primary q-mb-lg">Your employees are your best recruiters</div>
        <div class="row">
          <div class="col-12 col-md-6 q-pa-md" v-for="benefit in [
            {
              stat: '88%',
              description: 'Employers that say employee referrals are their number one source of talent'
            },
            {
              stat: '5X',
              description: 'Greater click through rate from employee content vs brand content'
            },
            {
              stat: '10X',
              description: 'Greater reach of combined employee social media network vs that of the employer'
            },
            {
              stat: '34%',
              description: 'Higher trust in a friend or family member vs a company executive'
            }
          ]">
            <BenefitItem :stat="benefit.stat" :description="benefit.description"/>
          </div>
        </div>
      </ResponsiveWidth>
      <div class="row justify-center bg-grey-2 w-100">
        <div class="col-12 col-md-6 col-lg-4 q-py-lg">
          <div class="rfs-h4 font-primary text-center q-mb-lg">
            Join the waitlist now!
          </div>
          <WaitlistSignUp/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import HowItWorksItem from 'pages/index-page/HowItWorksItem.vue'
import BenefitItem from 'pages/index-page/BenefitItem.vue'
import WaitlistSignUp from 'pages/index-page/WaitlistSignUp.vue'

export default defineComponent({
  name: 'IndexPage',
  components: { WaitlistSignUp, BenefitItem, HowItWorksItem, ResponsiveWidth },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Home'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
})
</script>
