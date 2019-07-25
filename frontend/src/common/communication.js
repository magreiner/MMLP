import axios from 'axios'

export async function sendGetRequest (path) {
  try {
    const url = `${location.protocol}//${location.hostname}:9010/${path}`
    // let a = JSON.parse(JSON.stringify(response, null, 2))
    const result = await axios.get(url)
    return result
  } catch (e) {
    console.log(`Hi ${e}`)
    throw new Error(e)
  }
}

export async function sendPostRequest (path, data) {
  const url = `${location.protocol}//${location.hostname}:9010/${path}`
  const result = await axios.post(url, data)
  return result
}
