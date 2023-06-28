<template>
  <div
    class="droppable"
    :class="droppableClass"
    @dragenter.prevent
    @drop="onOrderChange($event)"
  >
    <slot :items="items"/>
  </div>
</template>

<script>
/* eslint-disable vue/no-mutating-props */
import dataUtil from 'src/utils/data.js'

export default {
  name: 'DroppableItem',
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      isActive: false,
      currentItems: dataUtil.deepCopy(this.items)
    }
  },
  computed: {
    droppableClass () {
      return (this.isActive) ? ['droppable--active'] : null
    }
  },
  methods: {
    getElementYOffset (y, el) {
      const box = el.getBoundingClientRect()
      return y - box.top - box.height / 2
    },
    getDragAfterElement (y) {
      const elements = [...this.$el.querySelectorAll('.draggable:not(.draggable--active)')]
      const closest = elements.reduce((closest, element, elIdx) => {
        const offset = this.getElementYOffset(y, element)
        if (offset < 0 && offset > closest.offset) {
          return { offset, element, elIdx }
        }
        return closest
      }, { offset: Number.NEGATIVE_INFINITY, element: null, elIdx: null })

      return closest
    },
    getElementId (el) {
      const itemId = el.dataset.itemId
      return (itemId) ? parseInt(itemId) : itemId
    },
    onOrderChange (e) {
      const currentItemIds = this.currentItems.map((item) => item.id)
      const newItemIds = this.items.map((item) => item.id)
      if (!dataUtil.isArraysEqual(newItemIds, currentItemIds, true)) {
        this.currentItems = dataUtil.deepCopy(this.items)
        this.$emit('order-change', newItemIds)
      }
    }
  },
  mounted () {
    this.$global.$on('drag-on', () => {
      this.isActive = true
    })
    this.$global.$on('drag-off', () => {
      this.isActive = false
    })

    this.$el.addEventListener('dragover', (e) => {
      e.preventDefault()
      const dragItemId = this.getElementId(document.querySelector('.draggable--active'))
      const dragItem = dataUtil.removeItemFromList(
        this.items,
        { itemFindFn: (item) => item.id === dragItemId }
      )
      const { element: nextItem, elIdx } = this.getDragAfterElement(e.clientY)
      if (nextItem) {
        this.items.splice(elIdx, 0, dragItem)
      } else {
        this.items.push(dragItem)
      }
    })
  }
}
</script>

<style scoped lang="scss">
.droppable {
  &.droppable--active {
    border: 1px dashed $gray-500;
    background: $gray-300;
  }
}
</style>
