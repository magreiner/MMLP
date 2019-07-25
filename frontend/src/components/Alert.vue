<template>
  <v-flex fluid>
  <v-alert :type="alert.type" dismissible @input="onClose" :value="alert.show">
    {{ alert.text }}
  </v-alert>
  </v-flex>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters({ alert: 'getAlert' })
  },
  methods: {
    onClose () {
      this.$emit('dismissed')
    }
  }
}
</script>
