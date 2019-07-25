import axios from 'axios'
import { buildApiUrl } from '@/common'

export async function loadSnapshots ({ commit }, { query, loading }) {
  console.log(`--- loadSnapshots ---`)
  const url = buildApiUrl('snapshots')
  const countUrl = `${url}/count`
  // Loading indicator active
  if (loading) {
    commit('setLoading', true)
  }
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const count = await axios.get(countUrl)
    // console.log(`count: ${JSON.stringify(count, null, 2)}`)
    commit('setSnapshotCount', count.data.count)
    const list = await axios.get(url, { params: query })
    // console.log(`list: ${JSON.stringify(list, null, 2)}`)
    commit('setSnapshots', list.data)
  } catch (error) {
    console.log(`ERROR: loadSnapshots()`)
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function loadModelVersionSnapshots ({ commit }, { modelId, gitCommitId, query, loading }) {
  console.log(`--- loadModelVersionSnapshots ---`)
  const url = buildApiUrl(`snapshots/${modelId}/commit/${gitCommitId}`)
  const countUrl = `${url}/count`
  // Loading indicator active
  if (loading) {
    commit('setLoading', true)
  }
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const count = await axios.get(countUrl)
    // console.log(`count: ${JSON.stringify(count, null, 2)}`)
    commit('setSnapshotCount', count.data.count)
    const list = await axios.get(url, { params: query })
    // console.log(`list: ${JSON.stringify(list, null, 2)}`)
    commit('setSnapshots', list.data)
  } catch (error) {
    console.log(`ERROR: loadModelVersionSnapshots()`)
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function deleteSnapshot ({ commit }, snapshotId) {
  console.log('--- action deleteSnapshot ---')
  const url = buildApiUrl(`snapshots`)
  commit('setLoading', true)
  try {
    const result = await axios.delete(url, {
      data: {
        'snapshot_id': snapshotId
      }
    })
    if (result.data.id) {
      commit('removeSnapshot', snapshotId)
      commit('decrementSnapshotCount')
    } else {
      commit('setAlert', { show: true, type: 'error', message: `Failed to delete snapshot: ${result.data.error}` })
    }
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to delete snapshot: ${snapshotId}` })
  }
  commit('setLoading', false)
}

export async function downloadSnapshot ({ commit }, snapshotId) {
  const url = buildApiUrl(`snapshot/${snapshotId}/download`)
  console.log('--- downloadSnapshot ---')
  commit('setLoading', true)
  let result = ''
  try {
    result = await axios.get(url)
    // console.log(JSON.stringify(result, null, 2))
  } catch (error) {
    // TODO: Add Alert
    console.log(`ERROR: downloadSnapshot()`)
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
  return result
}
