<template>
  <div
    class="draggable"
    :class="draggableClass"
    draggable="true"
    @dragstart="startDrag"
    @dragend="endDrag"
    @mouseup="endDrag"
    :data-item-id="itemId"
  >
    <div class="draggable__handle row items-center justify-center" title="Drag to rearrange">
      <div class="col-12">
        <div class="draggable__handle__circle"></div>
      </div>
      <div class="col-12">
        <div class="draggable__handle__circle"></div>
      </div>
      <div class="col-12">
        <div class="draggable__handle__circle"></div>
      </div>
    </div>
    <slot/>
  </div>
</template>

<script>
export default {
  name: 'DraggableItem',
  props: {
    itemId: [Number, null]
  },
  data () {
    return {
      isDragging: false
    }
  },
  computed: {
    draggableClass () {
      return (this.isDragging) ? ['draggable--active'] : null
    }
  },
  methods: {
    startDrag (e) {
      this.isDragging = true
      e.dataTransfer.dropEffect = 'move'
      e.dataTransfer.effectAllowed = 'move'
      e.dataTransfer.setData('itemId', this.itemId)
      this.$global.$emit('drag-on')
    },
    endDrag () {
      this.isDragging = false
      this.$global.$emit('drag-off')
    }
  }
}
</script>

<style lang="scss">
.draggable {
  cursor: move;
  position: relative;

  &:hover &__handle {
    z-index: 1;
    position: absolute;
    background: $gray-300;
    border-bottom: 1px solid $gray-500;
    border-top: 1px solid $gray-500;
    border-right: 1px solid $gray-500;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    height: 36px;
    width: 12px;
    overflow: hidden;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;

    > * {
      padding-left: 2px;
    }

    & .draggable__handle__circle {
      color: $white;
      background: $white;
      border-radius: 25px;
      width: 5px;
      height: 5px;
    }
  }

  &.draggable--active > * {
    background: $gray-100;
  }
}
</style>
