<template>
  <div class="row q-gutter-y-md">
    <div v-for="part in section.section_parts" class="col-12 col-sm-6 col-md-4 col-lg-3 q-px-sm">
      <q-card class="h-100">
        <q-card-section>
          <div class="flex items-center justify-center">
            <q-icon v-if="part.icon" :name="part.icon.code" size="50px"/>
          </div>
          <h5 class="text-center">{{ part.header }}</h5>
          <q-separator/>
          <div class="q-py-md" v-html="part.html_content"></div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IconSection',
  props: {
    section: {
      type: [Object, null]
    }
  }
}
</script>
