<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job advertisements"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="search" label="Find partners"/>
        <q-tab name="saved-search" label="Saved search"/>
        <q-tab name="favorites" label="Favorites"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="search">
          <div class="q-mt-md">
            <div class="row q-gutter-y-md">
              <div class="col-12">
                <CollapsableCard title="Partner filters" :is-dense="true">
                  <template v-slot:body>
                    <div class="col-12 q-pa-sm">
                      <div class="row q-gutter-y-sm">
                        <div class="col-12">
                          <q-input
                            v-model="groupFilters.text"
                            filled label="Search by group name or skill"
                            debounce="500"
                          />
                        </div>
                        <div class="col-12 col-md-4 q-pr-md-sm">
                          <SelectJobCity
                            v-model="groupFilters.city_ids"
                            :is-emit-id="true"
                            :is-all="true"
                          />
                        </div>
                        <div class="col-12 col-md-4 q-px-md-sm">
                          <SelectJobState
                            v-model="groupFilters.state_ids"
                            :is-emit-id="true"
                            :is-all="true"
                          />
                        </div>
                        <div class="col-12 col-md-4 q-pl-md-sm">
                          <SelectJobCountry
                            v-model="groupFilters.country_ids"
                            :is-emit-id="true"
                            :is-all="true"
                          />
                        </div>
                        <div class="col-12 q-pt-sm">
                          <q-btn color="primary" label="Save search"/>
                        </div>
                      </div>
                    </div>
                  </template>
                </CollapsableCard>
              </div>
              <div class="col-12">
                <q-table
                  :columns="partnerColumns"
                  :rows="partnerRows"
                  row-key="id"
                  selection="multiple"
                  v-model:selected="partnersSelected"
                >
                  <template v-slot:top>
                    <div class="row">
                      <div class="col-12">
                        <q-btn
                          v-if="partnersSelected.length"
                          :label="`Setup job ads with ${dataUtil.pluralize('group', partnersSelected.length)}`"
                          icon-right="arrow_forward" color="primary"
                        />
                      </div>
                    </div>
                  </template>
                  <template v-slot:body-cell-name="props">
                    <q-td key="name" :props="props">
                      <q-avatar class="q-mr-md">
                        <q-img :src="props.row.logo"/>
                      </q-avatar>
                      {{ props.row.name }}
                    </q-td>
                  </template>
                  <template v-slot:body-cell-locations="props">
                    <q-td key="locations" :props="props">
                      <LocationChip :locations="props.row.locations" :is-dense="true" :condense-location-limit="2"/>
                    </q-td>
                  </template>
                  <template v-slot:body-cell-tags="props">
                    <q-td key="tags" :props="props">
                      <q-chip
                        v-for="tag in props.row.tags"
                        :color="(tag.type === 'skill') ? 'blue-8' : 'teal-8'" text-color="white" size="md" dense
                      >
                        {{ tag.name }}
                      </q-chip>
                    </q-td>
                  </template>
                </q-table>
              </div>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="saved-search">
          <div class="q-mt-md">
            <div class="row q-gutter-y-md">
              <div class="col-12"></div>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="favorites">
          <div class="q-mt-md">
            <div class="row q-gutter-y-md">
              <div class="col-12"></div>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import dataUtil from 'src/utils/data.js'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import LocationChip from 'components/LocationChip.vue'
import PageHeader from 'components/PageHeader.vue'

const partnerColumns = [
  { name: 'name', field: 'name', align: 'left', label: 'Group Name', sortable: true },
  { name: 'locations', field: 'locations', align: 'left', label: 'Locations' },
  {
    name: 'pricePerAdd',
    field: 'price_per_30_day_add',
    align: 'left',
    label: 'Sponsored 30-Day Add Cost',
    sortable: true,
    format: (val) => `$${val}`
  },
  { name: 'weeklyPageViews', field: 'weekly_page_views', align: 'left', label: 'Weekly Page Views', sortable: true },
  { name: 'tags', field: 'tags', align: 'left', label: 'Tags' }
]

const partnerRows = [
  {
    id: 1,
    name: 'Utah Product Guild',
    logo: '/logos/utahProductGuild_logo.png',
    locations: [{ state: 'Utah' }],
    tags: [{ type: 'skill', name: 'Product Management' }],
    weekly_page_views: 231,
    price_per_30_day_add: 200
  },
  {
    id: 2,
    name: 'Product Institute',
    logo: '/logos/productInstituteLogo.png',
    locations: [{ country: 'USA' }],
    tags: [{ type: 'skill', name: 'Product Management' }],
    weekly_page_views: 454,
    price_per_30_day_add: 200
  },
  {
    id: 3,
    name: 'AIPMM',
    logo: '/logos/aipmmLogo.jpeg',
    locations: [{ country: 'USA' }, { country: 'UK' }, { country: 'France' }],
    tags: [{ type: 'skill', name: 'Product Management' }, { type: 'skill', name: 'Product Marketing' }],
    weekly_page_views: 578,
    price_per_30_day_add: 150
  },
  {
    id: 4,
    name: 'Association of Product Professionals',
    logo: '/logos/appLogo.svg',
    locations: [{ country: 'USA' }],
    tags: [{ type: 'skill', name: 'Product Management' }],
    weekly_page_views: 578,
    price_per_30_day_add: 500
  },
  {
    id: 5,
    name: 'Mind the Product',
    logo: '/logos/mindtheproductLogo.png',
    locations: [{ country: 'USA' }],
    tags: [{ type: 'skill', name: 'Product Management' }],
    weekly_page_views: 891,
    price_per_30_day_add: 400
  }
]

export default {
  name: 'JobAddPage',
  components: { LocationChip, CollapsableCard, PageHeader, SelectJobCity, SelectJobState, SelectJobCountry },
  data () {
    return {
      tab: 'search',
      groupFilters: {
        text: null,
        city_ids: [],
        state_ids: [],
        country_ids: []
      },
      partnerColumns,
      partnerRows,
      partnersSelected: [],
      dataUtil
    }
  }
}
</script>
