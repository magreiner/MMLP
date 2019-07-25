import axios from 'axios'
import { buildApiUrl } from '@/common'

export async function loadModelVersions ({ commit }, { modelId, query }) {
  const url = buildApiUrl(`models/${modelId}/versions`)
  const countUrl = `${url}/count`
  commit('setLoading', true)
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const countResult = await axios.get(countUrl)
    commit('setModelVersionCount', countResult.data.count)
    const modelVersionResult = await axios.get(url, { params: query })
    // console.log(JSON.stringify(modelVersionResult.data, null, 2))
    commit('setModelVersions', modelVersionResult.data)
  } catch (error) {
    // TODO: Add Alert
    console.log(`ERROR: loadModelVersions ${error}`)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function loadModelVersionParameters ({ commit }, { modelId, gitCommitId }) {
  const url = buildApiUrl(`models/${modelId}/versions/${gitCommitId}/parameters`)
  commit('setLoading', true)
  try {
    const parameters = await axios.get(url)
    // console.log(JSON.stringify(parameters.data, null, 2))
    commit('setModelParameters', parameters.data)
  } catch (error) {
    // TODO: Add Alert
    console.log(`ERROR: ModelVersions.loadModelVersionParameters ${error}`)
  }
  commit('setLoading', false)
}
