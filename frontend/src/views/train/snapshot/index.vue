<template>
  <div>
    <ViewSnapshots v-if="!value" :modelVersion="modelVersion" @select="onSelectSnapshot"></ViewSnapshots>
    <SnapshotInfo v-if="value" :snapshot="value"></SnapshotInfo>
  </div>
</template>

<script>
import ViewSnapshots from './ViewSnapshots'
import SnapshotInfo from './SnapshotInfo'
export default {
  name: 'SelectSnapshot',
  components: { SnapshotInfo, ViewSnapshots },
  props: {
    modelVersion: {
      required: true,
      type: Object
    },
    value: {
      required: true
    }
  },
  methods: {
    onSelectSnapshot (snapshot) {
      this.$emit('input', snapshot)
    }
  }
}
</script>

<style scoped>

</style>
