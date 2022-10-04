<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Employer settings"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="style" label="Brand style"/>
        <q-tab name="security" label="Security"/>
        <q-tab name="integration" label="Integration"/>
        <q-tab v-if="hasPaymentPermission" name="billing" label="Billing"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated @transition="setupStripePaymentDom()">
        <q-tab-panel name="style">
          <div class="row q-gutter-y-md">
            <div class="col-12 q-gutter-x-sm">
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Undo" color="grey-6" icon="undo"
                @click="undoEmployerChanges"
              />
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Save" color="accent" icon="save"
                @click="saveEmployerChanges"
              />
            </div>
            <div class="col-12 col-md-6 q-pr-md-sm">
              <FileDisplayOrUpload
                ref="logoUpload"
                label="logo"
                :file-url="employerData.logo_url"
                :new-file="employerData[newLogoKey]"
                :new-file-key="newLogoKey"
                file-url-key="logo_url"
              >
                <template v-slot:fileInput>
                  <q-file
                    ref="newLogoUpload"
                    filled bottom-slots clearable
                    v-model="employerData[newLogoKey]"
                    label="Logo"
                    class="q-mb-none"
                    :accept="fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])"
                    lazy-rules="ondemand"
                    :rules="[val => val || 'A file is required']"
                    max-file-size="1000000"
                  />
                </template>
              </FileDisplayOrUpload>
            </div>
            <div class="col-12">
              <div class="row">
                <div class="col-12 q-mb-sm">
                  Brand colors
                  <CustomTooltip :is_include_space="true">
                    These will be the default colors used for the employer profile page. If none are provided,
                    the JobVyne default colors will be used.
                  </CustomTooltip>
                </div>
                <div class="col-12">
                  <div class="row q-gutter-md">
                    <ColorPicker
                      v-model="employerData.color_primary"
                      label="Primary color"
                    />
                    <ColorPicker
                      v-model="employerData.color_secondary"
                      label="Secondary color"
                    />
                    <ColorPicker
                      v-model="employerData.color_accent"
                      label="Accent color"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="security">
          <div class="row q-gutter-y-md">
            <div class="col-12 q-gutter-x-sm">
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Undo" color="grey-6" icon="undo"
                @click="undoEmployerChanges"
              />
              <q-btn
                v-if="hasEmployerDataChanged"
                ripple label="Save" color="accent" icon="save"
                @click="saveEmployerChanges"
              />
            </div>
            <div class="col-12 q-gutter-x-sm">
              <InputPermittedEmailDomains :employer-data="employerData"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="integration">
          <IntegrationSection :ats-data="employerData.ats_cfg" @update-employer="updateEmployerData()"/>
        </q-tab-panel>
        <q-tab-panel v-if="hasPaymentPermission" name="billing">
          <q-form ref="planForm" class="q-mb-md">
            <div class="row">
              <div class="col-12 text-h6">
                Subscription information
              </div>
              <div class="col-12">
                <div class="q-mt-sm q-pa-sm border-rounded" :class="(availableSeats < 0) ? 'bg-warning' : ''">
                  <q-icon name="help_outline"/>
                  Current active {{ dataUtil.pluralize('employee', employeeCount) }}
                  <span v-if="availableSeats >= 0">
                    ({{ dataUtil.pluralize('seat', availableSeats) }} available)
                  </span>
                  <span v-else>
                    ({{ dataUtil.pluralize('additional seat', availableSeats * -1) }} required)
                  </span>
                </div>
                <div v-if="subscriptionData" class="q-mt-sm">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="text-bold">Subscription Status</td>
                      <td>
                        <span v-if="subscriptionData.active">
                          Active
                        </span>
                        <span v-else>Inactive</span>
                      </td>
                    </tr>
                    <tr>
                      <td class="text-bold">Billing status</td>
                      <td>
                        <CustomTooltip
                          v-if="subscriptionData.status === SUBSCRIPTION_STATUS.CANCELED"
                          :is_include_icon="false"
                        >
                          <template v-slot:content>
                            <q-chip dense label="Canceled" color="negative"/>
                          </template>
                          The plan will continue until the end of its term.
                        </CustomTooltip>
                        <q-chip v-else-if="subscriptionData.status === SUBSCRIPTION_STATUS.ACTIVE" dense label="Paid"
                                color="positive"/>
                        <CustomTooltip
                          v-if="subscriptionUtil.getIsUnpaid(subscriptionData.status)"
                          :is_include_icon="false"
                        >
                          <template v-slot:content>
                            <q-chip dense label="Unpaid" color="negative"/>
                          </template>
                          Add a payment method to pay the outstanding balance.
                        </CustomTooltip>
                      </td>
                    </tr>
                    <tr>
                      <td class="text-bold">Employee seats</td>
                      <td>{{ subscriptionData.quantity }}</td>
                    </tr>
                    <tr>
                      <td class="text-bold">Plan interval</td>
                      <td>{{ dataUtil.capitalize(subscriptionData.interval) }}</td>
                    </tr>
                    <tr>
                      <td class="text-bold">Price per {{ subscriptionData.interval }}</td>
                      <td>{{subscriptionUtil.getFormattedSubscriptionPrice(subscriptionData)}}
                      </td>
                    </tr>
                    <tr>
                      <td class="text-bold">Start date</td>
                      <td>{{ dateTimeUtil.getShortDate(subscriptionData.start_date) }}</td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else class="text-bold q-mt-sm">
                  No plan selected
                </div>
                <div
                  v-if="subscriptionData.status !== SUBSCRIPTION_STATUS.CANCELED"
                  class="q-mt-md"
                >
                  <q-btn
                    v-if="subscriptionUtil.getIsUnpaid(subscriptionData.status)"
                    class="q-mr-sm"
                    color="primary"
                    :label="`Pay subscription (${subscriptionUtil.getFormattedSubscriptionPrice(subscriptionData)})`"
                    @click="openPaymentDialog"
                  />
                  <q-btn
                    v-if="!isPlansShown"
                    :label="(subscriptionData) ? 'Update subscription' : 'Select a subscription'"
                    color="accent"
                    @click="isPlansShown = true"
                  />
                  <q-btn
                    v-if="subscriptionData"
                    class="q-ml-sm"
                    label="Cancel subscription"
                    color="negative"
                    @click="cancelSubscription()"
                  />
                </div>
                <q-btn
                  v-else
                  class="q-mt-md"
                  label="Un-cancel subscription"
                  color="accent"
                  @click="reinstateSubscription()"
                />
                <PlanSection
                  v-if="isPlansShown"
                  :employee-count="employeeCount"
                  :employer-id="employerData.id"
                  :subscription="subscriptionData"
                  :can-close="true"
                  @updateSubscription="updateSubscription()"
                  @close="isPlansShown = false"
                />
              </div>
            </div>
          </q-form>
          <q-form ref="billingForm" class="q-mb-md">
            <div class="row">
              <div class="col-12 text-h6 q-mb-md">
                Billing information
              </div>
              <div class="col-12 q-gutter-x-sm">
                <q-btn
                  v-if="hasPaymentDataChanged"
                  ripple label="Undo" color="grey-6" icon="undo"
                  @click="undoBillingChanges"
                />
                <q-btn
                  v-if="hasPaymentDataChanged"
                  ripple label="Save" color="accent" icon="save"
                  :loading="isSavingBillingData"
                  @click="saveBillingChanges"
                />
              </div>
              <BillingInformationFields :billing-data="billingData"/>
            </div>
          </q-form>
          <q-form ref="paymentForm" @submit.prevent="submitPaymentMethod()">
            <div class="row">
              <div class="col-12 text-h6 q-mb-md">
                Payment information
              </div>
              <div class="col-12 q-mb-md">
                <q-table
                  v-if="!isAddPaymentMethod"
                  :rows="paymentMethods"
                  :columns="paymentMethodColumns"
                  row-key="id"
                  hide-pagination
                  no-data-label="No payment methods to display"
                  selection="single"
                  v-model:selected="selectedPaymentMethod"
                >
                  <template v-slot:top>
                    <q-btn ripple color="primary" label="Add payment method" @click="isAddPaymentMethod = true"/>
                    <template v-if="selectedPaymentMethod.length">
                      <q-btn
                        v-if="!selectedPaymentMethod[0].is_default"
                        ripple color="primary" label="Make default"
                        class="q-ml-sm"
                        @click="makeDefaultPaymentMethod"
                      />
                      <CustomTooltip v-if="selectedPaymentMethod[0].is_default" :is_include_icon="false">
                        <template v-slot:content>
                          <q-btn
                            ripple color="negative" label="Delete" icon="delete"
                            class="q-ml-sm"
                            disabled
                            @click="deletePaymentMethod"
                          />
                        </template>
                        Default payment method cannot be deleted
                      </CustomTooltip>
                      <q-btn
                        v-else
                        ripple color="negative" label="Delete" icon="delete"
                        class="q-ml-sm"
                        @click="deletePaymentMethod"
                      />
                    </template>
                  </template>
                  <template v-slot:body-cell-accountType="props">
                    <q-td key="accountType" :props="props">
                      <span v-if="props.row.type === 'card'">Card</span>
                      <span v-else-if="props.row.type === 'us_bank_account'">Bank account</span>
                      <q-chip v-if="props.row.is_default" label="Default" color="positive" dense/>
                    </q-td>
                  </template>
                  <template v-slot:body-cell-details="props">
                    <q-td key="details" :props="props">
                      <template v-if="props.row.type === 'card'">
                        <div>
                          <span class="text-bold">Card number: </span>
                          *********{{ props.row.last4 }}
                        </div>
                        <div>
                          <span class="text-bold">Expiration: </span>
                          {{ props.row.exp_month }}/{{ props.row.exp_year }}
                        </div>
                      </template>
                      <template v-else-if="props.row.type === 'us_bank_account'">
                        <div>
                          <span class="text-bold">Account number: </span>
                          *********{{ props.row.last4 }}
                        </div>
                        <div>
                          <span class="text-bold">Account type: </span>
                          {{ dataUtil.capitalize(props.row.account_type) }}
                        </div>
                      </template>
                    </q-td>
                  </template>
                </q-table>
              </div>
              <div class="col-12"
                   :style="`visibility: ${(isAddPaymentMethod) ? 'visible' : 'hidden'}`">
                <div id="payment-element">
                  <!-- Stripe Elements will create form elements here -->
                </div>
                <div class="q-mt-sm">
                  <q-btn
                    label="Cancel" color="grey-6" @click="isAddPaymentMethod = false"
                    class="q-mr-sm"
                  />
                  <q-btn
                    label="Save payment details" color="accent" type="submit"
                  />
                </div>
              </div>
            </div>
          </q-form>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogSubscriptionPayment from 'components/dialogs/DialogSubscriptionPayment.vue'
import ColorPicker from 'components/inputs/ColorPicker.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import PageHeader from 'components/PageHeader.vue'
import BillingInformationFields from 'pages/employer/settings-page/BillingInformationFields.vue'
import InputPermittedEmailDomains from 'pages/employer/settings-page/InputPermittedEmailDomains.vue'
import IntegrationSection from 'pages/employer/settings-page/IntegrationSection.vue'
import PlanSection from 'pages/employer/settings-page/PlanSection.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { loadScript, removeScript } from 'src/utils/load-script.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import subscriptionUtil, { SUBSCRIPTION_STATUS } from 'src/utils/subscription.js'
import { USER_TYPES } from 'src/utils/user-types.js'
import { useAjaxStore } from 'stores/ajax-store.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useBillingStore } from 'stores/billing-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { onUnmounted } from 'vue'

const STRIPE_SCRIPT = 'https://js.stripe.com/v3/'
const paymentMethodColumns = [
  { name: 'accountType', field: 'type', align: 'left', label: 'Type' },
  {
    name: 'institution',
    field: 'institution',
    format: (val) => dataUtil.capitalize(val, false),
    align: 'left',
    label: 'Institution'
  },
  { name: 'details', field: 'last4', align: 'left', label: 'Details' }
  // Include whether this is the company default
  // Include status (e.g. confirmed, pending confirmation)
]

export default {
  name: 'SettingsPage',
  components: {
    BillingInformationFields,
    PlanSection,
    InputPermittedEmailDomains,
    IntegrationSection,
    CustomTooltip,
    ColorPicker,
    FileDisplayOrUpload,
    PageHeader
  },
  data () {
    return {
      tab: 'style',
      newLogoKey: 'logo',
      currentEmployerData: this.getEmployerDataCopy(),
      employerData: this.getEmployerDataCopy(),
      currentBillingData: this.getEmployerBillingDataCopy(),
      billingData: this.getEmployerBillingDataCopy(),
      isSavingBillingData: false,
      subscriptionData: this.billingStore.getEmployerSubscription(this.user.employer_id),
      paymentSetupKey: this.billingStore.getEmployerPaymentSetup(this.user.employer_id),
      paymentMethods: this.billingStore.getEmployerPaymentMethods(this.user.employer_id),
      colorUtil,
      dataUtil,
      dateTimeUtil,
      fileUtil,
      subscriptionUtil,
      FILE_TYPES,
      stripe: null,
      stripeElements: null,
      isStripeLoaded: false,
      isPlansShown: false,
      isAddPaymentMethod: !this.billingStore.getEmployerPaymentMethods(this.user.employer_id),
      paymentMethodColumns,
      selectedPaymentMethod: [],
      SUBSCRIPTION_STATUS
    }
  },
  computed: {
    hasPaymentPermission () {
      return pagePermissionsUtil.hasPermission(this.user, pagePermissionsUtil.PERMISSION_NAMES.MANAGE_BILLING_SETTINGS)
    },
    hasEmployerDataChanged () {
      return !dataUtil.isDeepEqual(this.currentEmployerData, this.employerData)
    },
    hasPaymentDataChanged () {
      return !dataUtil.isDeepEqual(this.currentBillingData, this.billingData)
    },
    employeeCount () {
      return this.employerData.employees.filter((employee) => {
        return Boolean(employee.user_type_bits & USER_TYPES.Employee) && (!employee.is_employer_deactivated)
      }).length
    },
    availableSeats () {
      if (!this.subscriptionData) {
        return 0
      }
      return this.subscriptionData.quantity - this.employeeCount
    }
  },
  watch: {
    subscriptionData () {
      this.setupStripePaymentDom()
    }
  },
  methods: {
    getEmployerDataCopy () {
      return dataUtil.deepCopy(this.employerStore.getEmployer(this.user.employer_id))
    },
    getEmployerBillingDataCopy () {
      return dataUtil.deepCopy(this.employerStore.getEmployerBilling(this.user.employer_id))
    },
    async saveEmployerChanges () {
      const data = Object.assign(
        {},
        this.employerData,
        (this.$refs.logoUpload) ? this.$refs.logoUpload.getValues() : {}
      )

      // Make sure a logo is uploaded if existing logo is not being used
      if (
        this.$refs.logoUpload &&
        this.$refs.logoUpload.isUpload &&
        !this.$refs.newLogoUpload.validate()
      ) {
        return
      }
      await this.$api.put(
        `employer/${this.employerData.id}/`,
        getAjaxFormData(data, [this.newLogoKey])
      )
      await this.updateEmployerData()
    },
    async saveBillingChanges () {
      const isValidForm = await this.$refs.billingForm.validate()
      if (!isValidForm) {
        return
      }
      this.isSavingBillingData = true
      await this.$api.put(`employer/billing/${this.employerData.id}/`, getAjaxFormData(this.billingData))
      await this.employerStore.setEmployerBilling(this.user.employer_id, true)
      this.currentBillingData = this.getEmployerBillingDataCopy()
      this.billingData = this.getEmployerBillingDataCopy()
      this.isSavingBillingData = false
    },
    async updateEmployerData () {
      await this.employerStore.setEmployer(this.user.employer_id, true)
      this.currentEmployerData = this.getEmployerDataCopy()
      this.employerData = this.getEmployerDataCopy()
    },
    async updateSubscription () {
      await this.billingStore.setEmployerSubscription(this.user.employer_id, true)
      this.subscriptionData = this.billingStore.getEmployerSubscription(this.user.employer_id)
      this.isPlansShown = false
    },
    async reinstateSubscription () {
      await this.$api.put(`billing/subscription/${this.subscriptionData.id}/`, getAjaxFormData({
        employer_id: this.user.employer_id,
        is_reinstate: true
      }))
    },
    async cancelSubscription () {
      openConfirmDialog(this.q, 'Are you sure you want to cancel your subscription? You will continue to have access to the product until the end of your subscription term.',
        {
          okFn: async () => {
            await this.$api.delete(`billing/subscription/${this.subscriptionData.id}/`, {
              data: getAjaxFormData({
                employer_id: this.user.employer_id
              })
            })
            await this.updateSubscription()
          }
        }
      )
    },
    undoEmployerChanges () {
      this.employerData = dataUtil.deepCopy(this.currentEmployerData)
    },
    undoBillingChanges () {
      this.billingData = dataUtil.deepCopy(this.currentBillingData)
    },
    openPaymentDialog () {
      this.q.dialog({
        component: DialogSubscriptionPayment,
        componentProps: {
          billingData: this.getEmployerBillingDataCopy(),
          subscription: this.subscriptionData
        }
      })
    },
    async submitPaymentMethod () {
      const { error } = await this.stripe.confirmSetup({
        elements: this.stripeElements,
        confirmParams: {
          return_url: window.location.href // TODO: Add tab to return url so user is redirected to same page
        }
      })

      if (error) {
        this.ajaxStore.addErrorMsg(error)
      } else {
        this.ajaxStore.addSuccessMsg('Payment successfully added')
      }
      this.isAddPaymentMethod = false
    },
    async updatePaymentMethodData () {
      await this.billingStore.setEmployerPaymentMethods(this.user.employer_id, true)
      this.paymentMethods = this.billingStore.getEmployerPaymentMethods(this.user.employer_id)
      this.selectedPaymentMethod = []
    },
    async deletePaymentMethod () {
      await this.$api.delete(`billing/payment-method/${this.selectedPaymentMethod[0].id}`)
      await this.updatePaymentMethodData()
    },
    async makeDefaultPaymentMethod () {
      await this.$api.put('billing/payment-method/', getAjaxFormData({
        id: this.selectedPaymentMethod[0].id,
        is_default: true
      }))
      await this.updatePaymentMethodData()
    },
    setupStripePaymentDom () {
      const paymentElement = document.getElementById('payment-element')
      if (paymentElement && this.paymentSetupKey && !this.isStripeLoaded) {
        // Set up Stripe.js and Elements to use in checkout form
        this.stripeElements = this.stripe.elements({
          clientSecret: this.paymentSetupKey,
          appearance: {
            theme: 'stripe',
            variables: {
              colorPrimary: colorUtil.getPaletteColor('primary'),
              colorBackground: colorUtil.getPaletteColor('grey-2'),
              colorDanger: colorUtil.getPaletteColor('negative'),
              fontFamily: 'Open Sans, system-ui, sans-serif',
              borderRadius: '4px'
            }
          }
        })

        // Create and mount the Payment Element
        const paymentElement = this.stripeElements.create('payment', {
          defaultValues: {
            billingDetails: {
              name: this.employerData.name,
              email: this.billingData.billing_email,
              address: {
                line1: this.billingData.street_address,
                line2: this.billingData.street_address_2,
                city: this.billingData.city,
                state: this.billingData.state,
                country: this.billingData.country,
                postal_code: this.billingData.postal_code
              }
            }
          }
        })
        paymentElement.mount('#payment-element')
        this.isStripeLoaded = true
      }
    }
  },
  async created () {
    await loadScript(STRIPE_SCRIPT).then(() => {
      this.stripe = window.Stripe(process.env.STRIPE_PUBLIC_KEY)
      this.setupStripePaymentDom()
    })
  },
  preFetch () {
    const billingStore = useBillingStore()
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployerBilling(authStore.propUser.employer_id),
        billingStore.setEmployerSubscription(authStore.propUser.employer_id),
        billingStore.setEmployerPaymentSetup(authStore.propUser.employer_id),
        billingStore.setEmployerPaymentMethods(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const billingStore = useBillingStore()
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const globalStore = useGlobalStore()
    const pageTitle = 'Employer Settings Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    onUnmounted(() => removeScript(STRIPE_SCRIPT))

    return {
      ajaxStore: useAjaxStore(),
      authStore,
      billingStore,
      employerStore,
      user,
      q: useQuasar()
    }
  }
}
</script>
