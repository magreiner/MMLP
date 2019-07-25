<template>
  <v-container>
    <v-layout column>
      <v-toolbar
        color="indigo"
        dark
        scroll-off-screen
        scroll-target="#scrolling-techniques"
      >
        <v-toolbar-title>Running Experiments</v-toolbar-title>
      </v-toolbar>
      <v-list light
              header
              three-line
      >

      <v-container fluid class="pa-0">
        <v-layout colum wrap>
          <v-flex md6 sm12>
            <div v-if="!Object.keys(status.running_experiments).length">
              <v-chip color="green" text-color="white">
                No experiments are running now - happy working :)
              </v-chip>
            </div>
            <div v-for="(value, key, index) in status.running_experiments"
                 :key="index" class="text-xs-center">
              <v-chip :key="index" color="green" text-color="white" close @input="deleteRunningExperiment(key, status.running_experiments[key])">
                {{ key }} [ Status: {{ value.status }} ]
              </v-chip>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
      </v-list>
      <v-list light
              header
              three-line
      >
        <v-toolbar
          color="indigo"
          dark
          scroll-off-screen
          scroll-target="#scrolling-techniques"
        >
          <v-toolbar-title>Current statistics</v-toolbar-title>
        </v-toolbar>
        <v-subheader class="text-md-center"> We are going to provide a page to monitor the running experiments, system
          load, news, etc. for you!
        </v-subheader>

        <v-layout v-if="typeof(status) === 'undefined'" column>
          <h3>loading ... </h3>
        </v-layout>
        <v-layout v-else row>
          <v-layout column justify-space-between fill-height>
            <div class="text-xs-center">
              <h2 class="pa-3"> CPU usage percentage:</h2>
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="status.cpu"
                color="blue"
              >
                {{ status.cpu }}
              </v-progress-circular>
            </div>
            <div class="text-xs-center">
              <h2 class="pa-3"> Memory usage percentage:</h2>
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="status.memory"
                color="green"
              >
                {{ status.memory }}
              </v-progress-circular>
            </div>
          </v-layout>
          <v-layout column justify-space-between fill-height>
            <div class="text-xs-center">
              <h2 class="pa-3"> Disk usage percentage:</h2>
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="status.disk"
                color="purple"
              >
                {{ status.disk }}
              </v-progress-circular>
            </div>
            <div class="text-xs-center">
              <h2 class="pa-3"> GPU usage percentage:</h2>
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="status.gpu_usage"
                color="red lighten-3"
              >
                {{ status.gpu_usage }}
              </v-progress-circular>
            </div>
          </v-layout>
          <v-layout column justify-space-between fill-height>
            <div class="text-xs-center">
              <h2 class="pa-3"> GPU memory usage percentage:</h2>
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="status.gpu_memory"
                color="red darken-1"
              >
                {{ status.gpu_memory }}
              </v-progress-circular>
            </div>
            <div class="text-xs-center">
              <h2 class="pa-3"> GPU temperature:</h2>
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="status.gpu_temperature"
                color="red darken-3"
              >
                {{ status.gpu_temperature }}
              </v-progress-circular>
            </div>
          </v-layout>
        </v-layout>
        <v-toolbar
          color="indigo"
          dark
          scroll-off-screen
          scroll-target="#scrolling-techniques"
        >
          <v-toolbar-title>Statistics Trend</v-toolbar-title>
        </v-toolbar>
    <v-card light>
      <h2> CPU usage trend:</h2>
    <trend
      :data="cpuHistory"
      :gradient="['#6fa8dc', '#ff6400', '#ff0000']"
      auto-draw :max=100 :min=0
      smooth>
    </trend>
    </v-card>
    <v-card>
      <h2> Memory usage trend:</h2>
    <trend
      :data="memoryHistory"
      :gradient="['#6fa8dc', '#ff6400', '#ff0000']"
      auto-draw :max=100 :min=0
      smooth>
    </trend>
    </v-card>
    <v-card>
      <h2> Disk space trend:</h2>
    <trend
      :data="diskHistory"
      :gradient="['#6fa8dc', '#ff6400', '#ff0000']"
      auto-draw :max=100 :min=0
      smooth>
    </trend>
    </v-card>
    <v-card>
      <h2> GPU usage trend:</h2>
    <trend
      :data="gpuUsageHistory"
      :gradient="['#6fa8dc', '#ff6400', '#ff0000']"
      auto-draw :max=100 :min=0
      smooth>
    </trend>
    </v-card>
    <v-card>
      <h2> GPU memory trend:</h2>
    <trend
      :data="gpuMemoryHistory"
      :gradient="['#6fa8dc', '#ff6400', '#ff0000']"
      auto-draw :max=100 :min=0
      smooth>
    </trend>
      </v-card>
    <v-card>
    <h2> GPU temperature trend:</h2>
    <trend
      :data="gpuTemperatureHistory"
      :gradient="['#6fa8dc', '#ff6400', '#ff0000']"
      auto-draw :max=100 :min=0
      smooth>
    </trend>
    </v-card>
      </v-list>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data () {
    return {
      polling: null
    }
  },
  computed: {
    ...mapGetters({
      status: 'getSystemUtilization',
      cpuHistory: 'getCpuHistory',
      memoryHistory: 'getMemoryHistory',
      diskHistory: 'getDiskHistory',
      gpuUsageHistory: 'getGpuUsageHistory',
      gpuMemoryHistory: 'getGpuMemoryHistory',
      gpuTemperatureHistory: 'getGpuTemperatureHistory'
    })
  },
  methods: {
    loadResourceData: function () {
      this.$store.dispatch('retrieveSystemUtilization')
    },
    updateData () {
      this.loadResourceData()
    },
    pollData () {
      this.polling = setInterval(() => {
        this.updateData()
      }, 1000)
    },
    deleteRunningExperiment (experiment, experimentDetails) {
      // console.log(`delete called ${item}`)
      this.$store.dispatch('deleteRunningExperiment', {
        'name': experiment,
        'expInfo': experimentDetails
      })
    }
  },
  beforeDestroy () {
    clearInterval(this.polling)
  },
  created () {
    // console.info('Created')
    this.loadResourceData()
    this.pollData()
  }
}
</script>

<style lang="stylus" scoped>
  .v-progress-circular
    margin: 1rem
  .echarts {
    width: 100%;
    height: 100%;
  }
</style>
