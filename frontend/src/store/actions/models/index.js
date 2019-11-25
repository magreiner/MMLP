import axios from 'axios'
import { buildApiUrl } from '@/common'

export async function loadModels ({ commit }, query) {
  const url = buildApiUrl('models')
  const countUrl = `${url}/count`
  commit('setLoading', true)
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const countResult = await axios.get(countUrl)
    commit('setModelCount', countResult.data.count)
    const modelResult = await axios.get(url, { params: query })
    commit('setModels', modelResult.data)
  } catch (error) {
    // TODO: Add Alert
    console.log('ERROR: Datasets.load_datasets()')
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function importModel ({ commit }, model) {
  console.log('--- importModel ---')
  commit('setLoading', true)
  const url = buildApiUrl('models')
  const result = await axios.post(url, model)
  if (!result.data.id) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to import model: ${result.data.error}` })
  } else {
    commit('addModel', result.data)
    commit('incrementModelCount')
  }
  commit('setLoading', false)
}

export async function deleteModel ({ commit }, modelId) {
  const url = buildApiUrl(`models/${modelId}`)
  commit('setLoading', true)
  try {
    const result = await axios.delete(url)
    console.log('--- deleteModel result --')
    // console.log(JSON.stringify(result, null, 2))
    if (result.data.id) {
      commit('removeModel', modelId)
      commit('decrementModelCount')
    } else {
      commit('setAlert', { show: true, type: 'error', message: `Failed to delete model: ${result.data.error}` })
    }
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to delete model: ${modelId}, ${error}` })
  }
  commit('setLoading', false)
}

export async function updateModel ({ commit }, modelId) {
  const url = buildApiUrl(`models/${modelId}/update`)
  commit('setLoading', true)
  try {
    const result = await axios.get(url)
    // console.log(JSON.stringify(result, null, 2))
    commit('setAlert', { show: true, type: 'info', message: `Updated model ${result.data.name} to version: ${result.data.version}` })
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to update model: ${modelId}, error: ${error}` })
  }
  commit('setLoading', false)
}

export async function trainModel ({ commit }, { datasetVersionId, modelId, modelGitCommit, snapshotId, parameters }) {
  const url = buildApiUrl('compute/train')
  commit('setLoading', true)
  try {
    // Return status object
    const result = await axios.post(url, {
      datasetVersionId: datasetVersionId,
      modelId: modelId,
      modelGitCommit: modelGitCommit,
      snapshotId: snapshotId,
      parameters: parameters
    })
    commit('setAlert', { show: true, type: 'info', message: `Training started, snapshot ID: ${result.data.id}.` })
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to train model: ${modelId}, error: ${error}` })
  }
  commit('setLoading', false)
}
