
class MathUtil {
  getPercentage (numerator, denominator, { round = 2, asDecimal = false } = {}) {
    let val = numerator / denominator
    if (asDecimal) {
      val = val.toFixed(round)
      return val
    }
    val = (val * 100).toFixed(round)
    return `${val}%`
  }
}

const mathUtil = new MathUtil()
export default mathUtil
