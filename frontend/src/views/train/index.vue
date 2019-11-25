<template>
  <v-container fluid>
    <v-stepper v-model="step">
      <v-stepper-header>
        <v-stepper-step :complete="step > 1" step="1">Dataset</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="step > 2" step="2">Model</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="step > 3" step="3">Use Snapshot</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="step > 4" step="4">Model Parameters</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="5">Deploy</v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <SelectDatasetVersion v-model="datasetVersion"></SelectDatasetVersion>
          <v-btn color="purple" @click="onReSelectDataset">Reset Selection</v-btn>
          <v-btn color="primary" @click="step = 2" :disabled="!datasetVersion">Next</v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <SelectModelVersion v-model="modelVersion"></SelectModelVersion>
          <v-btn color="primary" @click="step = 1">Back</v-btn>
          <v-btn color="purple" @click="onReSelectModel">Reset Selection</v-btn>
          <v-btn color="primary" @click="step = 3" :disabled="!modelVersion">Next</v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <SelectSnapshot v-if="modelVersion" :modelVersion="modelVersion" v-model="snapshot"></SelectSnapshot>
          <v-btn color="primary" @click="step = 2">Back</v-btn>
          <v-btn color="purple" @click="onReSelectSnapshot">Reset Selection</v-btn>
          <v-btn color="green" @click="onNewSnapshot">New</v-btn>
          <v-btn color="primary" :disabled="!snapshot" @click="onTrainWithSnapshot()">Next</v-btn>
        </v-stepper-content>

        <v-stepper-content step="4">
          <ModelParameters></ModelParameters>
          <v-btn color="primary" @click="step=3">Back</v-btn>
          <v-btn color="primary" @click="step=5">Next</v-btn>
        </v-stepper-content>

        <v-stepper-content step="5">
          <ModelTrainingDeploy
            :datasetVersion="datasetVersion"
            :modelVersion="modelVersion"
            :snapshot="snapshot"
          ></ModelTrainingDeploy>
          <v-btn color="primary" @click="step=4">Back</v-btn>
          <v-btn color="primary" @click="train">Train</v-btn>
        </v-stepper-content>

      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script>
import SelectDatasetVersion from './dataset'
import SelectModelVersion from './model/index'
import SelectSnapshot from './snapshot/index'
import ModelParameters from './parameters/index'
import ModelTrainingDeploy from './deploy/index'
import { mapGetters } from 'vuex'
import { treeToParameters } from '../../common'

export default {
  name: 'TrainModel',
  components: { ModelTrainingDeploy, ModelParameters, SelectSnapshot, SelectModelVersion, SelectDatasetVersion },
  data () {
    return {
      step: 1,
      datasetVersion: null,
      modelVersion: null,
      snapshot: null
    }
  },
  computed: {
    ...mapGetters({ modelParameterTree: 'getModelParameterTree' })
  },
  methods: {
    onReSelectDataset () {
      this.datasetVersion = null
    },
    onReSelectModel () {
      this.modelVersion = null
    },
    onReSelectSnapshot () {
      this.snapshot = null
    },
    onTrainWithSnapshot () {
      this.$store.dispatch('loadModelVersionParameters', {
        modelId: this.modelVersion.model,
        gitCommitId: this.modelVersion.git_commit_id
      })
      this.step = 4
    },
    onNewSnapshot () {
      this.snapshot = null
      this.$store.dispatch('loadModelVersionParameters', {
        modelId: this.modelVersion.model,
        gitCommitId: this.modelVersion.git_commit_id
      })
      this.step = 4
    },
    train () {
      // console.log(JSON.stringify(this.modelVersion, null, 2))
      this.$store.dispatch('trainModel', {
        datasetVersionId: this.datasetVersion ? this.datasetVersion.id : '',
        modelId: this.modelVersion ? this.modelVersion.model : '',
        modelGitCommit: this.modelVersion.git_commit_id,
        snapshotId: this.snapshot ? this.snapshot.id : '',
        parameters: treeToParameters(this.modelParameterTree)
      })
      this.$router.push('/snapshots')
    }
  }
}
</script>
