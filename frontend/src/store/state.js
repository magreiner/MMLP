export default {
  // Loading and Alert
  alert: {
    show: false,
    type: 'error',
    message: ''
  },
  loading: false,
  currentUploadChunk: 100,

  // Navigation (two modes - 'app' for application and 'lab' for researchers
  mode: 'lab',
  navAreas: [
    // { title: 'Status', icon: 'timelapse', link: '/status', mode: ['app', 'lab'] },
    { title: 'Data Sets', icon: 'dns', link: '/datasets', mode: ['lab'] },
    { title: 'Models', icon: 'dashboard', link: '/models', mode: ['lab'] },
    { title: 'Train', icon: 'build', link: '/train', mode: ['lab'] },
    { title: 'Snapshots', icon: 'save', link: '/snapshots', mode: ['lab'] },
    { title: 'Analyze', icon: 'insert_chart_outlined', link: '/analyze', mode: ['app'] },
    { title: 'Methods', icon: 'developer_board', link: '/methods', mode: ['app', 'lab'] },
    { title: 'Results', icon: 'description', link: '/results', mode: ['app', 'lab'] }
    // { title: 'Dashboard', icon: 'dashboard', link: 'Dashboard', mode: [] },
    // { title: 'Patient Cohorts', icon: 'photo_library', link: 'PatientCohorts', mode: [] },
    // { title: 'Run Experiment', icon: 'style', link: 'Experiments', mode: [] },
    // { title: 'Experiment History', icon: 'style', link: 'ExperimentHistory', mode: [] }
  ],
  // Datasets
  datasets: {
    count: 0,
    collection: []
  },
  datasetVersions: {
    count: 0,
    collection: []
  },

  // Models
  models: {
    count: 0,
    collection: []
  },
  modelVersions: {
    count: 0,
    collection: []
  },

  // Model Parameters
  // modelParameterTree: parameterTree(treeparams)
  modelParameterTree: {},

  snapshots: {
    count: 0,
    collection: []
  },

  // Methods
  methods: {
    count: 0,
    collection: []
  },

  // Results
  results: {
    count: 0,
    collection: []
  },

  // Status
  status: {
    running: {
      count: 0,
      collection: []
    }
  }
  // -------------------------------------------------------------------------------------------------------------------
  // Old State
  // -------------------------------------------------------------------------------------------------------------------
  // patientCohortList: [],
  // methodList: [],
  // experimentList: [],
  // successfulExperimentList: [],
  // statusLog: 'System ready.',
  // alertParameters: {
  //   show: false,
  //   type: 'success',
  //   message: 'something is going on somewhere'
  // },
  // systemUtilization: {
  //   'cpu': -1,
  //   'memory': -1,
  //   'disk': -1,
  //   'gpu_usage': -1,
  //   'gpu_memory': -1,
  //   'gpu_temperature': -1,
  //   'running_experiments': ['loading ...']
  // },
  // cpuHistory: [],
  // memoryHistory: [],
  // diskHistory: [],
  // gpuUsageHistory: [],
  // gpuMemoryHistory: [],
  // gpuTemperatureHistory: [],
}
