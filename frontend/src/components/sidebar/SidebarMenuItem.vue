<template>
  <q-item
    clickable v-ripple
  >
    <q-item-section avatar>
      <q-icon :name="iconName"/>
    </q-item-section>
    <q-item-section>
      {{ menuLabel }}
    </q-item-section>
  </q-item>
</template>
<script>
export default {
  name: 'SidebarMenuItem',
  props: {
    iconName: String,
    menuLabel: String
  }
}
</script>
