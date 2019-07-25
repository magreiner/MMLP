import { parse, format } from 'date-fns'
import uuid from 'uuid/v4'

// const apiUrl = 'http://localhost:8000'
const apiUrl = `http://${window.location.hostname}:8000`

export function baseUrl () { return process.env.BASE_URL }
export function buildApiUrl (path) { return `${apiUrl}/${path}` }

export function paginationToQuery (pagination) {
  return {
    limit: pagination.rowsPerPage,
    offset: pagination.page - 1,
    sortby: pagination.sortBy,
    order: pagination.descending ? 'desc' : 'asc'
  }
}

export function formatDate (strIsoDate) {
  return format(parse(strIsoDate), 'YYYY-MM-DD HH:mm:ss')
}
// Returns the node if found, otherwise it returns back the id
export function findTreeNodeById (id, tree) {
  if (tree.id === id) return tree
  else if (tree.children) {
    const result = tree.children
      .map(child => findTreeNodeById(id, child))
      .find(x => x !== id)
    if (result) {
      return result
    } else {
      return id
    }
  } else {
    return id
  }
}

/**
 * Convert the parameters to a tree that can be displayed by the tree view component
 * @param node
 * @returns {{id: *}|Pick<*&{children: *, id: *}, Exclude<keyof *&{children: *, id: *}, "value">>}
 */
export function parameterTree (node) {
  // Id to be able to reference the nodes
  const id = uuid()
  if (node.value instanceof Array) {
    // Augment the node with a 'children' attribute, then destructure it to remove the value attribute. This
    // effectively renames value -> children, but returns a new object:
    let { value, ...result } = { ...node, id: id, children: node.value.map(child => parameterTree(child)) }
    return result
  } else return { ...node, id: id }
}

/**
 * Convert the parameter tree to the original parameter format
 * @param node
 */
export function treeToParameters (node) {
  if (node.children) {
    let { id, children, ...result } = { ...node, value: node.children.map(child => treeToParameters(child)) }
    return result
  } else {
    let { id, ...result } = node
    return result
  }
}
