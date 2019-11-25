// import mockResults from '../mock/results'
import axios from 'axios'
import { buildApiUrl } from '@/common'

export async function loadResults ({ commit }, { query, loading }) {
  console.log('--- loadResults ---')
  const url = buildApiUrl('results')
  const countUrl = `${url}/count`
  // Loading indicator active
  if (loading) {
    commit('setLoading', true)
  }
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const count = await axios.get(countUrl)
    // console.log(`count: ${JSON.stringify(count, null, 2)}`)
    commit('setResultCount', count.data.count)
    const list = await axios.get(url, { params: query })
    // console.log(`list: ${JSON.stringify(list, null, 2)}`)
    commit('setResults', list.data)
  } catch (error) {
    console.log('ERROR: loadResults()')
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function deleteResult ({ commit }, resultId) {
  console.log('--- action deleteResult ---')
  const url = buildApiUrl('results')
  commit('setLoading', true)
  try {
    const result = await axios.delete(url, {
      data: {
        result_id: resultId
      }
    })
    if (result.data.id) {
      commit('removeResult', resultId)
      commit('decrementResultCount')
    } else {
      commit('setAlert', { show: true, type: 'error', message: `Failed to delete result: ${result.data.error}` })
    }
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to delete result: ${resultId}` })
  }
  commit('setLoading', false)
}

export async function downloadResult ({ commit }, resultId) {
  const url = buildApiUrl(`results/${resultId}/download`)
  console.log('--- downloadResult ---')
  commit('setLoading', true)
  let result = ''
  try {
    result = await axios.get(url)
    // console.log(JSON.stringify(result, null, 2))
  } catch (error) {
    // TODO: Add Alert
    console.log('ERROR: downloadResult()')
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
  return result
}
