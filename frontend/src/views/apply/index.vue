<template>
  <v-container fluid>
    <v-dialog v-model="uploadPC" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Uploading Patient Cohort for Analysis</span>
        </v-card-title>
        <v-container>
          <div class="text-xs-center">
            <v-spacer></v-spacer>
            <v-progress-circular
              :size="100"
              :width="15"
              :value="currentUploadChunk"
              color="teal"
            >
              {{ currentUploadChunk }}
            </v-progress-circular>
            <v-card-text v-if="currentUploadChunk < 100">Uploading data, please wait ...</v-card-text>
            <v-card-text v-else-if="loading">Processing, please wait.</v-card-text>
            <v-spacer></v-spacer>
          </div>
        </v-container>
      </v-card>
    </v-dialog>

    <v-stepper v-model="step">
      <v-stepper-header>
        <v-stepper-step :complete="step > 1" step="1">Patient Cohort</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="step > 2" step="2">Method</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="step > 3" step="3">Deploy</v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card>
            <v-toolbar flat color="cyan">
<!--              <v-icon></v-icon>-->
              <v-toolbar-title>Please select your patient cohort:</v-toolbar-title>

              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-title>
              <span class="headline"></span>
            </v-card-title>
            <FileUploadSelector @select="selectFile"></FileUploadSelector>
          </v-card>

          <v-btn color="primary" @click="step = 2" :disabled="!patientCohortFile">Next</v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <SelectMethod v-model="method" @select="onSelectMethod"></SelectMethod>
          <v-btn color="primary" @click="step = 1">Back</v-btn>
          <v-btn color="primary" @click="step = 3" :disabled="!method">Next</v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <MethodApplicationDeployment
            :patientCohortFile="patientCohortFile"
            :method="method"
          ></MethodApplicationDeployment>
          <v-btn color="primary" @click="step=2">Back</v-btn>
          <v-btn color="primary" @click="applyMethod">Analyze</v-btn>
        </v-stepper-content>

      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import FileUploadSelector from '../../components/FileUploadSelector'
import SelectMethod from './method'
import MethodApplicationDeployment from './deploy'

export default {
  name: 'ApplyModel',
  components: { MethodApplicationDeployment, SelectMethod, FileUploadSelector },
  data () {
    return {
      step: 1,
      uploadPC: false,
      patientCohortFile: null,
      // patientCohortFile: {
      //   name: 'not_set'
      // },
      method: null
    }
  },
  computed: {
    ...mapGetters({ loading: 'getLoading', currentUploadChunk: 'getCurrentUploadChunk' })
  },
  methods: {
    onSelectMethod (method) {
      this.method = method
      this.step = 3
    },
    selectFile (file) {
      this.patientCohortFile = file
      // console.log(JSON.stringify(file, null, 2))
    },
    onDestroy () {
      this.method = null
      this.step = null
      this.patientCohortFile = null
    },
    uploadDialogCloser () {
      if (this.dialogPollingMonitor) {
        if (!this.loading) {
          this.uploadPC = false
          clearInterval(this.dialogPollingMonitor)
          this.$router.push('/results')
        }
      }
    },
    applyMethod () {
      // console.log(JSON.stringify(this.modelVersion, null, 2))
      this.uploadPC = true
      this.dialogPollingMonitor = setInterval(() => {
        this.uploadDialogCloser()
      }, 1000)
      this.$store.dispatch('uploadPatientCohortAndApplyMethod', {
        patientCohortFile: this.patientCohortFile,
        method: this.method
      })
    }
  },
  destroyed () {
    this.onDestroy()
  }
}
</script>
