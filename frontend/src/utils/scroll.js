import { scroll } from 'quasar'

const { getScrollTarget } = scroll

const SCROLL_PADDING = 40

class ScrollUtil {
  scrollTo (top) {
    window.scrollTo({ top, behavior: 'smooth' })
  }

  // !Make sure to add the "scroll" class to the scroll container
  scrollToElement (el) {
    const target = getScrollTarget(el)
    const offset = el.offsetTop - target.offsetTop - SCROLL_PADDING
    window.scrollTo({ top: offset, behavior: 'smooth' })
  }

  getHasOverflow (el) {
    const curOverf = el.style.overflow

    if (!curOverf || curOverf === 'visible') {
      el.style.overflow = 'hidden'
    }

    const isOverflowing = el.clientWidth < el.scrollWidth || el.clientHeight < el.scrollHeight

    el.style.overflow = curOverf

    return isOverflowing
  }
}

const scrollUtil = new ScrollUtil()

export default scrollUtil
