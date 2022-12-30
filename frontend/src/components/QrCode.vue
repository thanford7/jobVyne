<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'QrCode',
  props: {
    qrValue: String,
    width: {
      type: String,
      default: '80%'
    }
  },
  watch: {
    qrValue () {
      this.updateQrCode()
    }
  },
  methods: {
    updateQrCode () {
      const canvas = this.$refs.canvas
      QRCode.toCanvas(canvas, this.qrValue, function (error) {
        if (error) console.error(error)
        console.log('success!')
      })
    }
  },
  mounted () {
    this.updateQrCode()
  }
}
</script>
