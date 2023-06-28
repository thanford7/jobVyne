<template>
  <q-page padding>
    <div class="row justify-center">
      <ResponsiveWidth>
        <PageHeader title="Credits">
          Thank you to all of people, packages, libraries, and frameworks that make JobVyne possible
        </PageHeader>
        <q-list>
          <q-item v-for="credit in credits" clickable :href="credit.href" :inset-level="credit.insetLevel || 0">
            <q-item-section avatar>
              <q-avatar icon="auto_awesome"/>
            </q-item-section>
            <q-item-section>
              {{ credit.name }}
            </q-item-section>
          </q-item>
        </q-list>
      </ResponsiveWidth>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'

export default {
  components: { ResponsiveWidth, PageHeader },
  data () {
    return {
      credits: [
        { name: 'Quasar', href: 'https://quasar.dev/' },
        { name: 'Freepik', href: 'https://www.freepik.com/' },
        { name: 'Artist: pch.vector', href: 'https://www.freepik.com/author/pch-vector', insetLevel: 1 },
        { name: 'Artist: flaticon', href: 'https://www.freepik.com/author/flaticon', insetLevel: 1 },
        { name: 'Artist: mariadetarosarinda', href: 'https://www.freepik.com/author/mariadetarosarinda', insetLevel: 1 },
        { name: 'Artist: kiranshastry', href: 'https://www.flaticon.com/authors/kiranshastry', insetLevel: 1 },
        { name: 'GeoLite2 Data created by MaxMind', href: 'https://www.maxmind.com/' }
      ]
    }
  }
}
</script>
