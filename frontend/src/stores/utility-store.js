import { defineStore } from 'pinia'

const mobileBreakPoint = 768 // In px
const isMobileFn = () => window.innerWidth < mobileBreakPoint

export const useUtilStore = defineStore('util', {
  state: () => ({
    mobileBreakPoint,
    isMobile: isMobileFn(),
    elId: 0
  }),

  actions: {
    getNewElId () {
      this.elId++
      return this.elId
    },
    updateIsMobile () {
      this.isMobile = isMobileFn()
    }
  }
})

const counterStore = useUtilStore()
window.addEventListener('resize', () => counterStore.updateIsMobile())
