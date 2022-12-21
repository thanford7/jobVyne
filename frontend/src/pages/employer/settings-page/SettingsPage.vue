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
        <q-tab name="general" label="General"/>
        <q-tab name="security" label="Security"/>
        <q-tab name="integration" label="Integration"/>
        <q-tab v-if="hasPaymentPermission" name="billing" label="Billing"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="general">
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
            <div class="col-12 col-md-6">
              <EmailInput
                v-model="employerData.notification_email"
                label="Notification email"
                :is-required="false"
              >
                <template v-slot:after>
                  <CustomTooltip>
                    If provided, a notification email will be sent to this address every time an application
                    is submitted for any job or an employee provides feedback on an applicant. This is likely
                    only necessary if your company doesn't use an applicant tracking system.
                  </CustomTooltip>
                </template>
              </EmailInput>
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
                  Current active {{ dataUtil.pluralize('employee', this.employerData.employee_count_active) }}
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
                      <td class="text-bold">Billing interval</td>
                      <td>{{ dataUtil.capitalize(subscriptionData.interval) }}</td>
                    </tr>
                    <tr>
                      <td class="text-bold">Price per {{ subscriptionData.interval }}</td>
                      <td>{{ subscriptionUtil.getFormattedPrice(subscriptionData.total_price) }}
                      </td>
                    </tr>
                    <tr>
                      <td class="text-bold">Subscription term</td>
                      <td>
                        <template v-if="subscriptionData.start_date">
                          {{ dateTimeUtil.getShortDate(subscriptionData.start_date) }} -
                          {{ dateTimeUtil.getShortDate(subscriptionData.end_date) }}
                          <CustomTooltip v-if="subscriptionData.is_cancel_at_end" :is_include_icon="false">
                            <template v-slot:content>
                              <q-chip dense label="No auto-renew" color="negative"/>
                            </template>
                            The subscription will remain active until the end date, but will not
                            automatically renew afterwards. Click the "Un-cancel subscription" button
                            to ensure your subscription remains active.
                          </CustomTooltip>
                          <CustomTooltip v-else :is_include_icon="false">
                            <template v-slot:content>
                              <q-chip dense label="Auto-renew" color="positive"/>
                            </template>
                            The subscription will auto-renew at the end of the subscription term and you will
                            be pilled for the full subscription amount.
                          </CustomTooltip>
                        </template>
                        <template v-else>
                          N/A
                        </template>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else class="text-bold q-mt-sm">
                  No plan selected
                </div>
                <div
                  v-if="!subscriptionData.is_cancel_at_end && subscriptionData.start_date"
                  class="q-mt-md"
                >
                  <q-btn
                    v-if="subscriptionUtil.getIsUnpaid(subscriptionData.status)"
                    class="q-mr-sm"
                    color="primary"
                    :label="`Pay subscription (${subscriptionUtil.getFormattedPrice(subscriptionData.total_price)})`"
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
                  v-else-if="subscriptionData.start_date"
                  class="q-mt-md"
                  label="Un-cancel subscription"
                  color="accent"
                  @click="reinstateSubscription()"
                />
                <PlanSection
                  v-if="isPlansShown"
                  :employee-count="this.employerData.employee_count_active"
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
                    <StripeAccountType :payment-method="props.row"/>
                  </q-td>
                </template>
                <template v-slot:body-cell-details="props">
                  <q-td key="details" :props="props">
                    <StripePaymentMethodDetails :payment-method="props.row"/>
                  </q-td>
                </template>
              </q-table>
            </div>
          </div>
          <StripePaymentFields
            v-if="isAddPaymentMethod"
            :billing-data="billingData"
            :employer-data="employerData"
            @cancel="isAddPaymentMethod = false"
            @submitted="isAddPaymentMethod = false"
          />
          <div class="row q-mt-md">
            <div class="col-12 text-h6 q-mb-md">
              Past payments
            </div>
            <div class="col-12 q-mb-md">
              <q-table
                :rows="payments"
                :columns="pastPaymentColumns"
                hide-pagination
                no-data-label="No payments to display"
              >
                <template v-slot:body-cell-paymentDT="props">
                  <q-td key="paymentDT" :props="props">
                    {{ dateTimeUtil.getShortDate(props.row.charge_dt) }}
                  </q-td>
                </template>
                <template v-slot:body-cell-subscriptionDateRange="props">
                  <q-td key="subscriptionDateRange" :props="props">
                    {{ dateTimeUtil.getShortDate(props.row.period_start) }} -
                    {{ dateTimeUtil.getShortDate(props.row.period_end) }}
                  </q-td>
                </template>
                <template v-slot:body-cell-paymentURL="props">
                  <q-td key="paymentURL" :props="props">
                    <a :href="props.row.receipt_url" target="_blank">View receipt</a>
                  </q-td>
                </template>
              </q-table>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogSubscriptionPayment, {
  loadDialogSubscriptionPaymentFn
} from 'components/dialogs/DialogSubscriptionPayment.vue'
import ColorPicker from 'components/inputs/ColorPicker.vue'
import EmailInput from 'components/inputs/EmailInput.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import PageHeader from 'components/PageHeader.vue'
import BillingInformationFields from 'pages/employer/settings-page/BillingInformationFields.vue'
import InputPermittedEmailDomains from 'pages/employer/settings-page/InputPermittedEmailDomains.vue'
import IntegrationSection from 'pages/employer/settings-page/IntegrationSection.vue'
import PlanSection from 'pages/employer/settings-page/PlanSection.vue'
import StripeAccountType from 'pages/employer/settings-page/StripeAccountType.vue'
import StripePaymentFields from 'pages/employer/settings-page/StripePaymentFields.vue'
import StripePaymentMethodDetails from 'pages/employer/settings-page/StripePaymentMethodDetails.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import subscriptionUtil, { SUBSCRIPTION_STATUS } from 'src/utils/subscription.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useBillingStore } from 'stores/billing-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

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
]

const pastPaymentColumns = [
  { name: 'paymentDT', field: 'charge_dt', format: dateTimeUtil.getShortDate, align: 'left', label: 'Payment date' },
  { name: 'subscriptionDateRange', field: 'period_start', align: 'left', label: 'Subscription period' },
  {
    name: 'amountPaid',
    field: 'charge_amount',
    format: subscriptionUtil.getFormattedPrice,
    align: 'center',
    label: 'Amount paid'
  },
  { name: 'paymentURL', field: 'receipt_url', align: 'center', label: 'Receipt' }
]

export default {
  name: 'SettingsPage',
  components: {
    EmailInput,
    StripePaymentMethodDetails,
    StripeAccountType,
    StripePaymentFields,
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
      tab: 'general',
      newLogoKey: 'logo',
      currentEmployerData: this.getEmployerDataCopy(),
      employerData: this.getEmployerDataCopy(),
      currentBillingData: this.getEmployerBillingDataCopy(),
      billingData: this.getEmployerBillingDataCopy(),
      isSavingBillingData: false,
      subscriptionData: this.billingStore.getEmployerSubscription(this.user.employer_id),
      paymentMethods: this.billingStore.getEmployerPaymentMethods(this.user.employer_id),
      payments: this.billingStore.getEmployerCharges(this.user.employer_id),
      colorUtil,
      dataUtil,
      dateTimeUtil,
      fileUtil,
      subscriptionUtil,
      FILE_TYPES,
      isPlansShown: false,
      isAddPaymentMethod: !this.billingStore.getEmployerPaymentMethods(this.user.employer_id),
      paymentMethodColumns,
      selectedPaymentMethod: [],
      SUBSCRIPTION_STATUS,
      pastPaymentColumns
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
    availableSeats () {
      if (!this.subscriptionData) {
        return 0
      }
      return this.subscriptionData.quantity - this.employerData.employee_count_active
    }
  },
  watch: {
    tab () {
      this.$router.replace({ name: this.$route.name, params: this.$route.params, query: { tab: this.tab } })
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
      await this.updateSubscription()
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
    async openPaymentDialog () {
      await loadDialogSubscriptionPaymentFn()
      this.q.dialog({
        component: DialogSubscriptionPayment,
        componentProps: {
          employerData: this.employerData,
          subscription: this.subscriptionData,
          paymentMethod: dataUtil.getForceArray(this.paymentMethods).find((pm) => pm.is_default)
        }
      }).onOk(async () => {
        await this.updateEmployerData()
        await this.updateSubscription()
      })
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
    }
  },
  mounted () {
    const { tab } = this.$route.query
    if (tab) {
      this.tab = tab
    }
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
        billingStore.setEmployerCharges(authStore.propUser.employer_id),
        billingStore.setEmployerSubscription(authStore.propUser.employer_id),
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

    return {
      authStore,
      billingStore,
      employerStore,
      user,
      q: useQuasar()
    }
  }
}
</script>
