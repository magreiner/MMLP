import axios from 'axios'
import { buildApiUrl } from '@/common'
import uuid from 'uuid/v4'

// Load dataset versions
export async function loadDatasetVersions ({ commit }, { datasetId, query }) {
  const url = buildApiUrl(`datasets/${datasetId}/versions`)
  // Loading indicator active
  commit('setLoading', true)
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    // const countResult = await axios.get(countUrl)
    // commit('setDatasetCount', countResult.data.count)
    const result = await axios.get(url, { params: query })
    commit('setDatasetVersions', result.data)
    // TODO: Remove
    commit('setDatasetVersionCount', result.data.length)
  } catch (error) {
    // TODO: Show alert error
    console.log(`ERROR: Datasets.load_datasets()`)
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function uploadDatasetVersion ({ commit }, { datasetId, file }) {
  console.log('--- uploadDatasetVersion ---')
  // console.log(`file size: ${file.size}`)
  // console.log(`file mime-type: ${file.type}`)
  //
  commit('setLoading', true)
  // 100 mb chunk
  const fileId = uuid()
  const chunkSize = 1024 * 1024 * 12
  const fileSize = file.size
  const chunkCount = Math.ceil(fileSize / chunkSize)
  // console.log(`chunk count: ${chunkCount}`)
  commit('setCurrentUploadChunk', 0)
  let currentChunk = 1
  // File Reader
  const reader = new FileReader()
  // If an error occurs, abort the upload
  reader.onerror = async function (event) {
    const message = file ? `Failed to read file : ${file.name}` : 'Failed to read file'
    commit('setAlert', { show: true, type: 'error', message: message })
    commit('setLoading', false)
  }
  // The 'onloadend' callback needs to be inside 'uploadChunk', because it has to increment the 'offset' variable
  function uploadChunk (offset) {
    commit('setCurrentUploadChunk', Math.round((currentChunk * 100) / chunkCount))
    // console.log(`current chunk: ${currentChunk}`)
    currentChunk += 1
    const next = offset + chunkSize + 1
    const chunk = file.slice(offset, next)
    console.log(`chunk: ${offset}:${next}`)
    //
    reader.onloadend = async function (event) {
      if (event.target.readyState !== FileReader.DONE) {
        return
      }
      // Upload this chunk
      console.log(`next: ${offset}`)
      const url = buildApiUrl(`datasets/${datasetId}/versions?id=${fileId}&size=${fileSize}&offset=${offset}&chunk=${chunkSize}`)
      const result = await axios.post(url, event.target.result)
      console.log(result)
      // The chunk has been read
      if (next < fileSize) {
        console.log(`next: ${next}`)
        uploadChunk(next)
      } else {
        // We are finished here
        if (result.data.id) {
          commit('addDatasetVersion', result.data)
          commit('incrementDatasetVersionCount')
        } else {
          commit('setAlert', { show: true, type: 'error', message: `Failed to add dataset version: ${result.data.error}` })
        }
        commit('setLoading', false)
      }
    }
    reader.readAsArrayBuffer(chunk)
  }

  uploadChunk(0)
}

export async function deleteDatasetVersion ({ commit }, { datasetId, versionId }) {
  const url = buildApiUrl(`datasets/${datasetId}/versions/${versionId}`)
  commit('setLoading', true)
  try {
    const result = await axios.delete(url)
    if (result.data.id) {
      commit('removeDatasetVersion', versionId)
      commit('decrementDatasetVersionCount')
    } else {
      commit('setAlert', { show: true, type: 'error', message: `Failed to delete dataset version: ${result.data.error}` })
    }
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to delete dataset version: ${versionId}: ${error}` })
  }
  commit('setLoading', false)
}
