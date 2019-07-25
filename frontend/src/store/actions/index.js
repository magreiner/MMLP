// import { buildApiUrl } from '@/common'
// import axios from 'axios'

import { loadDatasets, uploadDataset, deleteDataset } from './datasets'
import { loadDatasetVersions, uploadDatasetVersion, deleteDatasetVersion } from './datasets/versions'
import { loadModels, importModel, deleteModel, updateModel, trainModel } from './models'
import { loadModelVersions, loadModelVersionParameters } from './models/versions'
import { loadSnapshots, deleteSnapshot, downloadSnapshot, loadModelVersionSnapshots } from './models/snapshots'
import { createMethod, deleteMethod, loadMethods, uploadPatientCohortAndApplyMethod } from './methods'
import { downloadResult, loadResults, deleteResult } from './results'
import { loadStatus } from './status'

export default {
  // Datasets
  loadDatasets,
  uploadDataset,
  deleteDataset,

  // Dataset Versions
  loadDatasetVersions,
  uploadDatasetVersion,
  deleteDatasetVersion,

  // Models
  loadModels,
  importModel,
  deleteModel,
  updateModel,
  trainModel,

  // Model Versions
  loadModelVersions,
  loadModelVersionParameters,

  // Model Snapshots
  loadSnapshots,
  loadModelVersionSnapshots,
  deleteSnapshot,
  downloadSnapshot,

  // Load Methods
  createMethod,
  deleteMethod,
  loadMethods,
  uploadPatientCohortAndApplyMethod,

  // Load Results
  loadResults,
  downloadResult,
  deleteResult,

  // Status
  loadStatus

  // async function checkGetResult (commit, name, path) {
//   try {
//     // const result = sendGetRequest(path)
//     const url = `${location.protocol}//${location.hostname}:8000/${path}`
//     const result = await axios.get(url)
//     // console.log(JSON.parse(JSON.stringify(result, null, 2)))
//
//     return result
//   } catch (error) {
//     const errorMessage = `Errormessage: ${error.message}, Parameters: ${name}, ${path}`
//     console.error(errorMessage)
//     commit('setAlertParameters', { type: 'error', message: errorMessage })
//
//     return null
//   }
// }
//
// async function checkPostResult (commit, name, path, payload) {
//   try {
//     // const result = sendPostRequest(path, payload)
//     const url = `${location.protocol}//${location.hostname}:8000/${path}`
//     const result = await axios.post(url, payload)
//     // console.log(JSON.parse(JSON.stringify(result, null, 2)))
//
//     return result
//   } catch (error) {
//     const errorMessage = `Errormessage: ${error.message}, Parameters: ${name}, ${path}`
//     console.error(errorMessage)
//     commit('setAlertParameters', { type: 'error', message: errorMessage })
//
//     return null
//   }
// }
//
//   retrieveSystemUtilization: async function ({commit}) {
//     const response = await checkGetResult(commit, 'retrieveSystemUtilization', 'monitor/status')
//
//     commit('setSystemUtilization', response.data)
//     commit('setCpuHistory', response.data.cpu)
//     commit('setMemoryHistory', response.data.memory)
//     commit('setDiskHistory', response.data.disk)
//     commit('setGpuUsageHistory', Math.round(response.data.gpu_usage))
//     commit('setGpuMemoryHistory', response.data.gpu_memory)
//     commit('setGpuTemperatureHistory', response.data.gpu_temperature)
//   },
//
//   retrievePatientCohorts: async function ({commit}) {
//     const response = await checkGetResult(commit, 'retrievePatientCohorts', 'patientcohort/list')
//
//     commit('setPatientCohortList', response.data)
//   },
//
//   importPatientCohort: async function ({commit, dispatch}, patientCohort) {
//     await checkPostResult(commit,
//       'importPatientCohort',
//       'patientcohort/import/',
//       {
//         'repository': patientCohort
//       })
//     await dispatch('retrievePatientCohorts')
//   },
//
//   editPatientCohort: async function ({commit, dispatch}, patientCohort) {
//     await checkPostResult(commit,
//       'editPatientCohort',
//       'patientcohort/edit/',
//       {
//         'repository': patientCohort
//       })
//     await dispatch('retrievePatientCohorts')
//   },
//
//   updatePatientCohort: async function ({commit, dispatch}, patientCohort) {
//     await checkPostResult(commit,
//       'editPatientCohort',
//       'patientcohort/update/',
//       {
//         'repository': patientCohort
//       })
//     await dispatch('retrievePatientCohorts')
//   },
//
//   deletePatientCohort: async function ({commit, dispatch}, patientCohort) {
//     await checkPostResult(commit,
//       'deletePatientCohort',
//       'patientcohort/delete/',
//       {
//         'repository': patientCohort
//       })
//     await dispatch('retrievePatientCohorts')
//   },
//
//   retrieveMethods: async function ({commit}) {
//     const response = await checkGetResult(commit, 'retrieveMethods', 'method/list')
//
//     commit('setMethodList', response.data)
//   },
//
//   importMethod: async function ({commit, dispatch}, method) {
//     await checkPostResult(commit,
//       'importMethod',
//       'method/import/',
//       {
//         'repository': method
//       })
//     await dispatch('retrieveMethods')
//   },
//
//   editMethod: async function ({commit, dispatch}, method) {
//     await checkPostResult(commit,
//       'editMethod',
//       'method/edit/',
//       {
//         'repository': method
//       })
//     await dispatch('retrieveMethods')
//   },
//
//   updateMethod: async function ({commit, dispatch}, method) {
//     await checkPostResult(commit,
//       'updateMethod',
//       'method/update/',
//       {
//         'repository': method
//       })
//     await dispatch('retrieveMethods')
//   },
//
//   deleteMethod: async function ({commit, dispatch}, method) {
//     await checkPostResult(commit,
//       'deleteMethod',
//       'method/delete/',
//       {
//         'repository': method
//       })
//     await dispatch('retrieveMethods')
//   },
//
//   retrieveExperiments: async function ({commit}) {
//     const response = await checkGetResult(commit, 'retrieveExperiments', 'experiment/list')
//
//     commit('setExperimentList', response.data)
//   },
//   retrieveSuccessfulExperiments: async function ({commit}) {
//     const response = await checkGetResult(commit, 'retrieveSuccessfulExperiments', 'experiment/successListInitial')
//
//     commit('setSuccessfulExperimentList', response.data)
//   },
//
//   runExperiment: async function ({commit, dispatch}, newExperiment) {
//     await checkPostResult(commit,
//       'runExperiment',
//       'experiment/run/',
//       newExperiment
//     )
//   },
//
//   deleteRunningExperiment: async function ({commit}, runningExperiment) {
//     console.log(JSON.parse(JSON.stringify(runningExperiment, null, 2)))
//     const result = await checkPostResult(commit,
//       'deleteRunningExperiment',
//       'docker/killContainerProcess',
//       {
//         'container_name': runningExperiment.name,
//         'exp_info': runningExperiment.expInfo
//       })
//
//     if (result.data.status === 'success') {
//       commit('setAlertParameters', {
//         type: 'info',
//         message: `Terminated experiment ${runningExperiment} successfully`
//       })
//     } else {
//       commit('setAlertParameters', {
//         type: 'error',
//         message: `Error terminating experiment "${runningExperiment}": ${result.data.status}`
//       })
//     }
//   },
//   deleteExperiments: async function ({commit, dispatch}, experiments) {
//     const result = await checkPostResult(commit,
//       'deleteExperiments',
//       'experiment/delete/',
//       {
//         'experiments': experiments
//       })
//     // console.log(JSON.stringify(result, null, 2))
//     if (result.data.status === 'success') {
//       commit('setAlertParameters', {
//         type: 'info',
//         message: `Deletion successful for: ${result.data.deletion_successful_list}`
//       })
//     } else {
//       const errorMessage = `The following experiments could not be deleted: ${result.data.deletion_failed_list}`
//       console.error(errorMessage)
//       commit('setAlertParameters', {type: 'error', message: errorMessage})
//     }
//     dispatch('retrieveExperiments')
//   },
//   downloadExperiments: async function ({commit, dispatch}, experimentsZipPath) {
//     // console.log(JSON.stringify(experimentsZipPath, null, 2))
//     const result = await checkGetResult(commit,
//       'downloadExperiments',
//       `fileManager/downloadFile/${btoa(experimentsZipPath)}`)
//     // console.log(JSON.stringify(result, null, 2))
//     return result
//   },
}
