<template>
  <v-app dark>
    <!-- Navigation -->
    <app-navigation></app-navigation>
    <!-- Alert -->
    <div>
      <v-alert dismissible @input="onClose" :value="alert.show" :type="alert.type">{{alert.message}}</v-alert>
    </div>
    <!-- Content -->
    <router-view></router-view>
    <!-- Footer -->
    <!-- v-footer app
      height="auto"
      color="primary"
      width="10000"
    >
        <v-layout
          fill-height
          row
        >
        <v-flex>Matthias Greiner&#160;&#160;</v-flex>
        <v-flex class="text-xs-center" v-text="statusLog"></v-flex>
        <v-spacer></v-spacer>
        <v-flex class="text-xs-right">
          <span v-text="hours"></span>:
          <span v-text="minutes"></span>:
          <span v-text="seconds"> </span>&#160;
          <span v-text="hourtime"></span>&#160;&#160;
        </v-flex>
      </v-layout>
    </v-footer-->
    <v-footer color="primary" height="auto">
      <v-layout fill-height row>
        <v-flex>Matthias Greiner&#160;&#160;</v-flex>
      </v-layout>
    </v-footer>
  </v-app>
</template>

<script>
// import Alert from './components/Alert'
import { mapGetters } from 'vuex'
export default {
  name: 'App',
  // data: () => {
  //   return {
  //     hours: 0,
  //     minutes: 0,
  //     seconds: 0,
  //     hourtime: ''
  //   }
  // },
  // mounted () {
  //   this.$options.interval = setInterval(this.updateDateTime, 1000)
  // },
  // beforeDestroy () {
  //   clearInterval(this.$options.interval)
  // },
  // created () {
  // },
  computed: {
    ...mapGetters({
      // statusLog: 'getStatusLog',
      alert: 'getAlert'
    })
  },
  methods: {
    onClose () {
      // this.$emit('dismissed')
      this.$store.commit('setAlert', { show: false, type: 'error', message: '' })
    }
    // updateDateTime () {
    //   let now = new Date()
    //   this.hours = now.getHours()
    //   this.minutes = this.getZeroPad(now.getMinutes())
    //   this.seconds = this.getZeroPad(now.getSeconds())
    //   this.hourtime = this.getHourTime(this.hours)
    //   this.hours = this.hours % 12 || 12
    // },
    // getHourTime: function (h) {
    //   return h >= 12 ? 'PM' : 'AM'
    // },
    //
    // getZeroPad: function (n) {
    //   return (parseInt(n, 10) >= 10 ? '' : '0') + n
    // }
  }
}

</script>
