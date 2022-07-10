<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section v-if="titleText">
        <div class="text-h6">
          {{titleText}}
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <slot/>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <slot name="buttons">
          <q-btn flat label="Cancel" @click="onDialogCancel" />
          <q-btn flat color="accent" :label="primaryButtonText" @click="onDialogOK"/>
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
