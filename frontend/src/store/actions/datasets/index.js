import axios from 'axios'
import uuid from 'uuid/v4'
import { buildApiUrl } from '@/common'

export async function loadDatasets ({ commit }, query) {
  console.log('--- loadDatasets ---')
  const url = buildApiUrl('datasets')
  const countUrl = `${url}/count`
  // Loading indicator active
  commit('setLoading', true)
  try {
    // Get the total number of items and retrieve a single page according to the table parameters
    const datasetCount = await axios.get(countUrl)
    commit('setDatasetCount', datasetCount.data.count)
    const datasetList = await axios.get(url, { params: query })
    commit('setDatasets', datasetList.data)
  } catch (error) {
    console.log('ERROR: Datasets.load_datasets()')
    console.error(error)
  }
  // Loading indicator inactive
  commit('setLoading', false)
}

export async function uploadDataset ({ commit }, file) {
  console.log('--- uploadDataset ---')
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
      const url = buildApiUrl(`datasets?id=${fileId}&size=${fileSize}&offset=${offset}&chunk=${chunkSize}`)
      const result = await axios.post(url, event.target.result)
      console.log(result)
      // The chunk has been read
      if (next < fileSize) {
        console.log(`next: ${next}`)
        uploadChunk(next)
      } else {
        // We are finished here
        if (result.data.id) {
          commit('addDataset', result.data)
          commit('incrementDatasetCount')
        } else {
          commit('setAlert', { show: true, type: 'error', message: `Failed to add dataset: ${result.data.error}` })
        }
        commit('setLoading', false)
      }
    }
    reader.readAsArrayBuffer(chunk)
  }

  uploadChunk(0)
  // const reader = new FileReader()
  // commit('setLoading', true)
  // reader.onload = async function (event) {
  //   const buffer = event.target.result
  //   const url = buildApiUrl('datasets')
  //   const result = await axios.post(url, buffer)
  //   if (result.data.id) {
  //     commit('addDataset', result.data)
  //     commit('incrementDatasetCount')
  //   } else {
  //     commit('setAlert', { show: true, type: 'error', message: `Failed to add dataset: ${result.data.error}` })
  //   }
  //   commit('setLoading', false)
  // }
  // reader.onerror = async function (event) {
  //   const message = file ? `Failed to read file : ${file.name}` : 'Failed to read file'
  //   commit('setAlert', { show: true, type: 'error', message: message })
  //   commit('setLoading', false)
  // }
  // reader.readAsArrayBuffer(file)
}

export async function deleteDataset ({ commit }, datasetId) {
  console.log('--- action deleteDataset ---')
  const url = buildApiUrl(`datasets/${datasetId}`)
  console.log(url)
  commit('setLoading', true)
  try {
    const result = await axios.delete(url)
    if (result.data.id) {
      commit('removeDataset', datasetId)
      commit('decrementDatasetCount')
    } else {
      commit('setAlert', { show: true, type: 'error', message: `Failed to delete dataset: ${result.data.error}` })
    }
  } catch (error) {
    commit('setAlert', { show: true, type: 'error', message: `Failed to delete dataset: ${datasetId}: ${error}` })
  }
  commit('setLoading', false)
  console.log(datasetId)
}
