import mockStatus from '../mock/status'
// import axios from 'axios'
// import { buildApiUrl } from '@/common'

export async function loadStatus ({ commit }, query) {
  console.log('--- loadStatus ---')
  // console.log(`query: ${JSON.stringify(query, null, 2)}`)
  // Load mock data
  commit('setStatusRunningCount', mockStatus.running.count)
  commit('setStatusRunning', mockStatus.running.collection)
}

// export async function loadStatus ({ commit }, query) {
//   console.log(`--- loadStatus ---`)
//   const url = buildApiUrl('resources')
//   const countUrl = `${url}/count`
//   // Loading indicator active
//   commit('setLoading', true)
//   try {
//     // Get the total number of items and retrieve a single page according to the table parameters
//     const count = await axios.get(countUrl)
//     commit('setStatusRunningCount', count.data.count)
//     const list = await axios.get(url, { params: query })
//     commit('setStatusRunning', list.data)
//   } catch (error) {
//     console.log(`ERROR: loadStatus()`)
//     console.error(error)
//   }
//   // Loading indicator inactive
//   commit('setLoading', false)
// }

// export async function stop ({ commit }, experiment) {
//  console.log(`experiment: ${JSON.stringify(experiment)}`)
// }
