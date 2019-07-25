import { findTreeNodeById, parameterTree } from '../common'

export default {
  setLoading: (state, loading) => { state.loading = loading },
  setAlert: (state, params) => { state.alert = params },

  setCurrentUploadChunk: (state, chunk) => { state.currentUploadChunk = chunk },

  // Navigation
  setMode: (state, mode) => { state.mode = mode },
  // setSideNav: (state, sideNav) => { state.sideNav = sideNav },

  // Datasets
  addDataset: (state, dataset) => { state.datasets.collection.push(dataset) },
  setDatasets: (state, datasets) => { state.datasets.collection = datasets },
  setDatasetCount: (state, count) => { state.datasets.count = count },
  incrementDatasetCount: (state) => { state.datasets.count += 1 },
  decrementDatasetCount: (state) => { state.datasets.count -= 1 },
  removeDataset: (state, datasetId) => {
    state.datasets.collection = state.datasets.collection.filter(ds => ds.id !== datasetId)
  },

  // Dataset Version
  addDatasetVersion: (state, datasetVersion) => { state.datasetVersions.collection.push(datasetVersion) },
  setDatasetVersions: (state, versions) => { state.datasetVersions.collection = versions },
  setDatasetVersionCount: (state, count) => { state.datasetVersions.count = count },
  incrementDatasetVersionCount: (state) => { state.datasetVersions.count += 1 },
  decrementDatasetVersionCount: (state) => { state.datasetVersions.count -= 1 },
  removeDatasetVersion: (state, versionId) => {
    state.datasetVersions.collection = state.datasetVersions.collection.filter(v => v.id !== versionId)
  },

  // Models
  addModel: (state, model) => { state.models.collection.push(model) },
  setModels: (state, models) => { state.models.collection = models },
  setModelCount: (state, count) => { state.models.count = count },
  incrementModelCount: (state) => { state.models.count += 1 },
  decrementModelCount: (state) => { state.models.count -= 1 },
  removeModel: (state, modelId) => {
    state.models.collection = state.models.collection.filter(model => model.id !== modelId)
  },

  // Model Versions
  setModelVersions: (state, versions) => { state.modelVersions.collection = versions },
  setModelVersionCount: (state, count) => { state.modelVersions.count = count },

  // Model Parameters
  setModelParameters: (state, parameters) => { state.modelParameterTree = parameterTree(parameters) },
  setModelParameterValue: (state, { id, value }) => { findTreeNodeById(id, state.modelParameterTree).value = value },

  // Snapshots
  setSnapshots: (state, snapshots) => { state.snapshots.collection = snapshots },
  setSnapshotCount: (state, count) => { state.snapshots.count = count },
  incrementSnapshotCount: (state) => { state.snapshots.count += 1 },
  decrementSnapshotCount: (state) => { state.snapshots.count -= 1 },
  removeSnapshot: (state, snapshotId) => {
    state.snapshots.collection = state.snapshots.collection.filter(snapshot => snapshot.id !== snapshotId)
  },

  // Methods
  addMethod: (state, method) => { state.methods.collection.push(method) },
  setMethods: (state, methods) => { state.methods.collection = methods },
  setMethodCount: (state, count) => { state.methods.count = count },
  incrementMethodCount: (state) => { state.methods.count += 1 },
  decrementMethodCount: (state) => { state.methods.count -= 1 },
  removeMethod: (state, methodId) => {
    state.methods.collection = state.methods.collection.filter(method => method.id !== methodId)
  },

  // Results
  setResults: (state, results) => { state.results.collection = results },
  setResultCount: (state, count) => { state.results.count = count },
  incrementResultCount: (state) => { state.results.count += 1 },
  decrementResultCount: (state) => { state.results.count -= 1 },
  removeResult: (state, resultId) => {
    state.results.collection = state.results.collection.filter(result => result.id !== resultId)
  },

  // Status
  setStatusRunning: (state, running) => { state.status.running.collection = running },
  setStatusRunningCount: (state, count) => { state.status.running.count = count }

  // -------------------------------------------------------------------------------------------------------------------
  // Old Mutations
  // -------------------------------------------------------------------------------------------------------------------
  //
  // setPatientCohortList (state, value) {
  //   state.patientCohortList = value
  // },
  // setMethodList (state, value) {
  //   state.methodList = value
  // },
  // setExperimentList (state, value) {
  //   state.experimentList = value
  // },
  // setSuccessfulExperimentList (state, value) {
  //   state.successfulExperimentList = value
  // },
  // setSystemUtilization (state, value) {
  //   state.systemUtilization = value
  // },
  // setCpuHistory (state, value) {
  //   state.cpuHistory.push(value)
  // },
  // setMemoryHistory (state, value) {
  //   state.memoryHistory.push(value)
  // },
  // setDiskHistory (state, value) {
  //   state.diskHistory.push(value)
  // },
  // setGpuUsageHistory (state, value) {
  //   state.gpuUsageHistory.push(value)
  // },
  // setGpuMemoryHistory (state, value) {
  //   state.gpuMemoryHistory.push(value)
  // },
  // setGpuTemperatureHistory (state, value) {
  //   state.gpuTemperatureHistory.push(value)
  // },
  // setStatusLog (state, value) {
  //   // context.commit('setStatusLog', 'Loaded patient cohorts successfully')
  //   state.statusLog = value
  // },
  // setAlertParameters (state, payload) {
  //   if (state.alertParameters.show) {
  //     // Message is already displayed, append new message
  //     state.alertParameters.message += '; New Alert: ' + payload.message
  //
  //     // Ensure message is showing error if at least one alert is an error
  //     if (payload.type === 'error' && state.alertParameters.show) {
  //       state.alertParameters.type = payload.type
  //       payload.timeout = -1
  //     }
  //   } else {
  //     state.alertParameters.show = true
  //     state.alertParameters.type = payload.type
  //     state.alertParameters.message = payload.message
  //   }
  //
  //   const timeout = (typeof payload.timeout === 'undefined') ? 5000 : payload.timeout
  //   if (timeout > 0 && state.alertParameters.type !== 'error') {
  //     setTimeout(() => {
  //       state.alertParameters.show = false
  //     }, timeout)
  //   }
  // },
  // logEvent (state, payload) {
  //   if (payload.type === 'error') {
  //     this.commit('setAlertParameters', payload)
  //   } else {
  //     this.commit('setAlertParameters', payload)
  //   }
  // },
}
