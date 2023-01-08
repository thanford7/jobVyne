<template>
  <q-page>
    <div class="row justify-center q-pt-xl q-gutter-y-lg  vine-background-1">
      <ResponsiveWidth class="q-px-md">
        <div class="row q-my-xl">
          <transition appear enter-active-class="animated slideInLeft">
            <div class="col-12 col-md-7 q-gutter-y-lg">
              <div class="rfs-h2 text-center text-bold font-primary">Turn your employees into your best recruiters</div>
              <div class="rfs-h6 text-center text-gray-700">
                Automate employee referrals and generate more meaningful connections with job seekers
              </div>
              <q-btn
                icon="event" color="accent" size="1.2rem" class="w-100 q-mt-xl" ripple
                label="Schedule demo"
                @click="openDialogDemoSignUp()"
              />
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
      <div class="row justify-center w-100 wavey" style="background-color: rgba(155, 162, 255, 0.2);">
        <ResponsiveWidth class="q-gutter-y-xl q-px-md q-py-xl">
          <div class="rfs-h4 font-primary q-ml-md-xl text-center">You are missing talented candidates</div>
          <div class="row">
            <div class="col-12 col-md-6 q-pa-sm">
              <div class="border-1-negative border-rounded q-pa-md">
                <div class="rfs-h5 text-center q-mb-lg">Traditional Referral Programs</div>
                <div class="text-center q-mb-lg">
                  <q-img class="w-25" src="~assets/icons/one-to-one2.png" alt="One to one sharing"/>
                </div>
                <div class="rfs-h6 q-mb-lg">
                  Employee referral programs are "one to one". An employee has to know of a job candidate that
                  is a good fit and reach out to that person.
                </div>
                <div class="rfs-h6 q-mb-sm">
                  This means you <b>miss out</b> on:
                </div>
                <ListIcon class="rfs-h6"
                  :items="[
                    'Passive candidates',
                    'Candidates that the employee didn\'t think of',
                    'Candidates that could have been referred by employees that don\'t participate in employee referrals'
                  ]"
                  color="negative"
                  icon-name="visibility_off"
                />
              </div>
            </div>
            <div class="col-12 col-md-6 q-pa-sm">
              <div class="border-1-positive border-rounded q-pa-md h-100">
                <div class="rfs-h5 text-center q-mb-lg">JobVyne Platform</div>
                <div class="text-center q-mb-lg">
                  <q-img class="w-25" src="~assets/icons/many-to-one2.png" alt="Many to one sharing"/>
                </div>
                <div class="rfs-h6 q-mb-lg">
                  JobVyne automatically posts multiple recent jobs to employees' social networks. Job candidates
                  self-identify
                  and apply directly.
                </div>
                <div class="rfs-h6 q-mb-sm">
                  This means you <b>get more referrals</b> from:
                </div>
                <ListIcon class="rfs-h6"
                  :items="[
                    'Passive candidates',
                    'Candidates that the employee didn\'t think of',
                    '2nd and 3rd degree connections in an employee\'s network'
                  ]"
                  color="positive"
                  icon-name="group_add"
                />
              </div>
            </div>
          </div>
        </ResponsiveWidth>
      </div>
      <div class="row justify-center w-100">
        <ResponsiveWidth class="q-gutter-y-xl q-px-md q-py-xl">
          <div class="rfs-h4 font-primary q-ml-md-xl text-center">Employers and employees love JobVyne</div>
          <div class="q-pa-md">
            <q-carousel
              id="testimonials"
              animated keep-alive
              v-model="slide"
              infinite :autoplay="autoplay" control-color="primary"
              :height="(utilityStore.isMobile) ? '60vh' : '40vh'"
              transition-prev="slide-right"
              transition-next="slide-left"
              @mouseenter="autoplay = 7000"
              @mouseleave="autoplay = false"
              style="background-color: rgba(0,0,0,0);"
            >
              <q-carousel-slide :name="1">
                <div class="flex h-100 items-center justify-center">
                  <TestimonialCard
                    :class="(utilityStore.isMobile) ? '' : 'w-50'"
                    headshot-src="/images/headshots/heatherWaldron.png"
                    quote="JobVyne has made it so easy for employees to get the word out on new job openings and to get referrals.
                    Hiring managers have been very happy with the quality of the applicants as well."
                    name="Heather Waldron"
                    job-title="HR Generalist"
                  />
                </div>
              </q-carousel-slide>
              <q-carousel-slide :name="2">
                <div class="flex h-100 items-center justify-center">
                  <TestimonialCard
                    :class="(utilityStore.isMobile) ? '' : 'w-50'"
                    headshot-src="/images/headshots/timBirkmire.jpeg"
                    quote="I got my first referral a few days after setting up my account. It's easy and simple. Every employee should check this out!"
                    name="Tim Birkmire"
                    job-title="Senior Software Engineer"
                  />
                </div>
              </q-carousel-slide>
              <q-carousel-slide :name="3">
                <div class="flex h-100 items-center justify-center">
                  <TestimonialCard
                    :class="(utilityStore.isMobile) ? '' : 'w-50'"
                    headshot-src="/images/headshots/gretelUptegrove.jpeg"
                    quote="I've never made a referral before, but JobVyne allows me to 'set it and forget it'. I got a referral within two weeks of joining the platform."
                    name="Gretel Uptegrove"
                    job-title="Data Engineer"
                  />
                </div>
              </q-carousel-slide>
              <q-carousel-slide :name="4">
                <div class="flex h-100 items-center justify-center">
                  <TestimonialCard
                    :class="(utilityStore.isMobile) ? '' : 'w-50'"
                    headshot-src="/images/headshots/russGunther.jpeg"
                    quote="It's often difficult to keep up with all of the job postings. JobVyne automatically updates the jobs so I don't even have to think about it. It's a great platform."
                    name="Russ Gunther"
                    job-title="Senior Software Engineer"
                  />
                </div>
              </q-carousel-slide>
              <q-carousel-slide :name="5">
                <div class="flex h-100 items-center justify-center">
                  <TestimonialCard
                    :class="(utilityStore.isMobile) ? '' : 'w-50'"
                    headshot-src="/images/headshots/ericHochberg.jpeg"
                    quote="I attend a lot of events and can share job openings with potential candidates by sharing a JobVyne QR code. It makes recruiting a lot easier. Even better, the QR code is linked to me so I can get a referral bonus!"
                    name="Eric Hochberg"
                    job-title="Director of Product Management"
                  />
                </div>
              </q-carousel-slide>
            </q-carousel>
          </div>
        </ResponsiveWidth>
      </div>
      <div class="row justify-center w-100 wavey" style="background-color: rgba(155, 162, 255, 0.2);">
        <ResponsiveWidth class="q-gutter-y-xl q-px-md q-py-xl">
          <div class="rfs-h4 font-primary q-ml-md-xl q-pt-lg">How it works</div>
          <q-intersection once style="min-height: 150px" transition="slide-right" :threshold="0.8"
                          transition-duration="1000">
            <HowItWorksItem
              header="JobVyne integrates with your Applicant Tracking System
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
        <div class="rfs-h4 font-primary q-mb-lg text-center">Your employees are your best recruiters</div>
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
      <div class="row justify-center wavey-top w-100 q-pb-xl" style="background-color: rgba(155, 162, 255, 0.2);">
        <div class="col-12 col-md-8 q-mt-xl">
          <div class="rfs-h4 font-primary text-center q-mb-sm">
            Don't miss out on your best source for talent. Get more employee referrals today
          </div>
          <q-btn
            icon="event" color="accent" size="1.2rem" class="w-100 q-mt-md" ripple
            label="Schedule demo"
            @click="openDialogDemoSignUp()"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import DialogDemoSignUp from 'components/dialogs/DialogDemoSignUp.vue'
import ListIcon from 'components/ListIcon.vue'
import TestimonialCard from 'components/TestimonialCard.vue'
import { useUtilStore } from 'stores/utility-store.js'
import { defineComponent } from 'vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta, useQuasar } from 'quasar'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import HowItWorksItem from 'pages/index-page/HowItWorksItem.vue'
import BenefitItem from 'pages/index-page/BenefitItem.vue'

export default defineComponent({
  name: 'IndexPage',
  components: { TestimonialCard, ListIcon, BenefitItem, HowItWorksItem, ResponsiveWidth },
  data () {
    return {
      autoplay: 7000, // Number of milliseconds to show each slide
      slide: 1
    }
  },
  methods: {
    openDialogDemoSignUp () {
      this.q.dialog({
        component: DialogDemoSignUp
      })
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Home'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
    return {
      utilityStore: useUtilStore(),
      q: useQuasar()
    }
  }
})
</script>

<style lang="scss">
.vine-background-1 {
  position: relative;

  &::before {
    content: "";
    background: url('../../assets/background/vine1.jpeg') center center fixed;
    background-size: cover;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    opacity: 0.15;
    overflow: hidden;
  }
}

#testimonials {
  // Prevents headshots from being clipped
  overflow: visible;
  .q-panel {
    overflow: visible;
  }
}
</style>
