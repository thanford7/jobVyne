import { defineStore } from 'pinia'

const breakpointXS = 599
const breakpointSM = 1023
const breakpointMD = 1439
const breakpointLG = 1919

export const useUtilStore = defineStore('util', {
  state: () => ({
    windowWidth: window.innerWidth,
    elId: 0
  }),

  actions: {
    getNewElId () {
      this.elId++
      return this.elId
    },
    setWindowWidth () {
      this.windowWidth = window.innerWidth
    },
    isUnderBreakPoint (breakpointName) { // xs sm md lg xl
      if (breakpointName === 'xl') {
        return this.windowWidth <= breakpointLG
      } else if (breakpointName === 'lg') {
        return this.windowWidth <= breakpointMD
      } else if (breakpointName === 'md') {
        return this.windowWidth <= breakpointSM
      } else if (breakpointName === 'sm') {
        return this.windowWidth <= breakpointXS
      }
    },
    redirectUrl (url, isNewTab = false) {
      if (isNewTab) {
        window.open(url, '_blank')
      } else {
        this.$router.push(url)
      }
    }
  }
})

const utilStore = useUtilStore()
window.addEventListener('resize', () => utilStore.setWindowWidth())
