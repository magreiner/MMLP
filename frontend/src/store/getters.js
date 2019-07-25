export default {
  // Loading and Alert
  getAlert: state => state.alert,
  getLoading: state => state.loading,

  getCurrentUploadChunk: state => state.currentUploadChunk,

  // Navigation
  getMode: state => state.mode,
  getSideNav: state => state.sideNav,
  getNavAreas (state) {
    return state.navAreas.filter(area => area.mode.includes(state.mode))
  },

  // Datasets
  getDatasets: state => state.datasets.collection,
  getDatasetCount: state => state.datasets.count,
  getDatasetById: state => id => state.datasets.collection.find(m => m.id === id),

  // Dataset Version
  getDatasetVersions: state => state.datasetVersions.collection,
  getDatasetVersionCount: state => state.datasetVersions.count,

  // Models
  getModels: state => state.models.collection,
  getModelCount: state => state.models.count,
  getModelById: state => id => state.models.collection.find(m => m.id === id),

  // Model Version
  getModelVersions: state => state.modelVersions.collection,
  getModelVersionCount: state => state.modelVersions.count,
  getModelVersionByGitCommitId: state => gitCommitId => state.modelVersions.collection.find(m => m.git_commit_id === gitCommitId),

  // Model Parameters
  getModelParameterTree: state => state.modelParameterTree,

  // Snapshots
  getSnapshots: state => state.snapshots.collection,
  getSnapshotCount: state => state.snapshots.count,

  // Methods
  getMethods: state => state.methods.collection,
  getMethodCount: state => state.methods.count,

  // Results
  getResults: state => state.results.collection,
  getResultCount: state => state.results.count,

  // Status
  getStatusRunning: state => state.status.running.collection,
  getStatusRunningCount: state => state.status.running.count

  // -------------------------------------------------------------------------------------------------------------------
  // Old Getters
  // -------------------------------------------------------------------------------------------------------------------
  // getPatientCohortList: state => state.patientCohortList,
  // getMethodList: state => state.methodList,
  // getExperimentList: state => state.experimentList,
  // getSuccessfulExperimentList: state => state.successfulExperimentList,
  // getSystemUtilization: state => state.systemUtilization,
  // getCpuHistory: state => state.cpuHistory,
  // getMemoryHistory: state => state.memoryHistory,
  // getDiskHistory: state => state.diskHistory,
  // getGpuUsageHistory: state => state.gpuUsageHistory,
  // getGpuMemoryHistory: state => state.gpuMemoryHistory,
  // getGpuTemperatureHistory: state => state.gpuTemperatureHistory,
  // getStatusLog: state => state.statusLog,
}
