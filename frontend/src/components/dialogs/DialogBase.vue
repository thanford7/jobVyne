<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div v-if="titleText" class="text-h6">
          {{titleText}}
        </div>
        <q-btn
          flat unelevated
          icon="close"
          text-color="grey-5"
          @click="onDialogCancel"
          class="q-pr-sm"
          style="position: absolute; top: 0; right: 0"
        />
      </q-card-section>

      <slot name="fullWidthBody"/>

      <q-card-section class="q-pt-none">
        <slot/>
      </q-card-section>

      <q-card-actions v-if="isIncludeButtons" align="right" class="text-primary">
        <slot name="buttons">
          <q-btn class="bg-grey-7" flat text-color="white" label="Cancel" @click="onDialogCancel" />
          <q-btn class="bg-accent" flat text-color="white" :label="primaryButtonText" @click="onDialogOK"/>
        </slot>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from 'quasar'

export default {
  name: 'DialogBase',
  props: {
    primaryButtonText: {
      type: String,
      default: 'Submit'
    },
    titleText: {
      type: [String, null]
    },
    isIncludeButtons: {
      type: Boolean,
      default: true
    }
  },
  emits: [
    // REQUIRED; need to specify some events that your
    // component will emit through useDialogPluginComponent()
    ...useDialogPluginComponent.emits
  ],

  setup () {
    // https://quasar.dev/quasar-plugins/dialog#invoking-custom-component
    // REQUIRED; must be called inside of setup()
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
    // dialogRef      - Vue ref to be applied to QDialog
    // onDialogHide   - Function to be used as handler for @hide on QDialog
    // onDialogOK     - Function to call to settle dialog with "ok" outcome
    //                    example: onDialogOK() - no payload
    //                    example: onDialogOK({ /*.../* }) - with payload
    // onDialogCancel - Function to call to settle dialog with "cancel" outcome

    return {
      // This is REQUIRED;
      dialogRef,
      onDialogHide,
      onDialogOK,
      onDialogCancel
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
