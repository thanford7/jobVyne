import { scroll } from 'quasar'
const { getScrollTarget } = scroll

const SCROLL_PADDING = 40

class ScrollUtil {
  // !Make sure to add the "scroll" class to the scroll container
  scrollToElement (el) {
    const target = getScrollTarget(el)
    const offset = el.offsetTop - target.offsetTop - SCROLL_PADDING
    window.scrollTo({ top: offset, behavior: 'smooth' })
  }
}

const scrollUtil = new ScrollUtil()

export default scrollUtil
