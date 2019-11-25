import axios from 'axios'
import { buildApiUrl } from '@/common'
import uuid from 'uuid/v4'
// import mockMethods from '../../mock/methods'

// export async function loadMethods ({ commit }, query) {
//   console.log('--- loadMethods ---')
//   console.log(`query: ${JSON.stringify(query, null, 2)}`)
//   // Load mock data
//   commit('setMethodCount', mockMethods.count)
//   commit('setMethods', mockMethods.collection)
// }

export async function loadMethods ({ commit }, { query }) {
  console.log('--- loadMethods ---')
  const url = buildApiUrl('methods')
  const countUrl = `${url}/count`
  // Loading indicator active
  commit('setLoading', true)
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const count = await axios.get(countUrl)
    // console.log(`count: ${JSON.stringify(count, null, 2)}`)
    commit('setMethodCount', count.data.count)
    const list = await axios.get(url, { params: query })
    // console.log(`list: ${JSON.stringify(list, null, 2)}`)
    commit('setMethods', list.data)
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to load Method: ${name}: ${error}` })
    console.log('ERROR: loadMethods()')
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function createMethod ({ commit }, { name, description, modelSnapshotId }) {
  const url = buildApiUrl('methods')
  console.log('--- createMethod ---')
  commit('setLoading', true)
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const newMethod = await axios.post(url, {
      name: name,
      description: description,
      model_snapshot_id: modelSnapshotId
    })
    commit('incrementMethodCount')
    commit('addMethod', newMethod.data)
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to create Method: ${name}: ${error}` })
    console.log('ERROR: createMethod()')
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function deleteMethod ({ commit }, methodId) {
  console.log('--- action deleteMethod ---')
  const url = buildApiUrl('methods')
  commit('setLoading', true)
  try {
    const result = await axios.delete(url, {
      data: {
        method_id: methodId
      }
    })
    if (result.data.id) {
      commit('removeMethod', methodId)
      commit('decrementMethodCount')
    } else {
      commit('setAlert', { show: true, type: 'error', message: `Failed to delete method: ${result.data.error}` })
    }
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to delete method: ${methodId}: ${error}` })
  }
  commit('setLoading', false)
}

export async function uploadPatientCohortAndApplyMethod ({ commit }, { patientCohortFile, method }) {
  console.log('--- uploadPatientCohort ---')
  // console.log(`file size: ${file.size}`)
  // console.log(`file mime-type: ${file.type}`)
  //
  commit('setLoading', true)
  // 100 mb chunk
  const fileId = uuid()
  const chunkSize = 1024 * 1024 * 12
  const fileSize = patientCohortFile.size
  const chunkCount = Math.ceil(fileSize / chunkSize)
  // console.log(`chunk count: ${chunkCount}`)
  commit('setCurrentUploadChunk', 0)
  let currentChunk = 1
  // File Reader
  const reader = new FileReader()
  // If an error occurs, abort the upload
  reader.onerror = async function (event) {
    const message = patientCohortFile ? `Failed to read file : ${patientCohortFile.name}` : 'Failed to read file'
    commit('setAlert', { show: true, type: 'error', message: message })
    commit('setLoading', false)
  }

  // The 'onloadend' callback needs to be inside 'uploadChunk', because it has to increment the 'offset' variable
  function uploadChunk (offset) {
    commit('setCurrentUploadChunk', Math.round((currentChunk * 100) / chunkCount))
    // console.log(`current chunk: ${currentChunk}`)
    currentChunk += 1
    const next = offset + chunkSize + 1
    const chunk = patientCohortFile.slice(offset, next)
    console.log(`chunk: ${offset}:${next}`)
    //
    reader.onloadend = async function (event) {
      if (event.target.readyState !== FileReader.DONE) {
        return
      }
      // Upload this chunk
      console.log(`next: ${offset}`)
      const url = buildApiUrl(`compute/uploadPatientCohort?id=${fileId}&size=${fileSize}&offset=${offset}&chunk=${chunkSize}`)
      const result = await axios.post(url, event.target.result)
      console.log(result)
      // The chunk has been read
      if (next < fileSize) {
        console.log(`next: ${next}`)
        uploadChunk(next)
      } else {
        // We are finished here
        if (result.data.current_dir) {
          // upload successful deploy training
          try {
            const deployUrl = buildApiUrl('compute/apply')
            const deployResult = await axios.post(deployUrl, {
              patient_cohort_location: result.data,
              method_id: method.id,
              issuer: 'Clinical Data Scientist'
            })
            commit('setAlert', {
              show: true,
              type: 'info',
              message: `Analyzing started, result ID: ${deployResult.data.id}.`
            })
          } catch (error) {
            commit('setAlert', {
              show: true,
              type: 'error',
              message: `Failed to apply method: ${method}, error: ${error}`
            })
          }
        } else {
          commit('setAlert', {
            show: true,
            type: 'error',
            message: `Failed to upload patient cohort: ${result.data.error}`
          })
        }
        commit('setLoading', false)
      }
    }
    reader.readAsArrayBuffer(chunk)
  }

  uploadChunk(0)
}
