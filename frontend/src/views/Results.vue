<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
  <v-container fluid>
    <v-dialog v-model="deleteDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Delete Result</span>
        </v-card-title>
        <v-card-text>
          Would you like to delete result: {{this.selectedItem.id}} ?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-toolbar flat color="cyan">
      <v-toolbar-title>Result Overview</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="results"
      :pagination.sync="pagination"
      :total-items="resultCount"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <td>{{ props.item.id }}</td>
        <td>{{ props.item.method.name }}</td>
        <td>{{ convertDate(props.item.created) }}</td>
        <td>{{ props.item.status }}</td>
        <td class="justify-center layout px-0">
          <v-icon v-if="props.item.status === 'finished'" small @click="downloadItem(props.item)"> get_app </v-icon>
          <v-icon v-else small @click="$store.commit('setAlert', { show: true, type: 'info', message: `Result is not finished yet. Please be patient.` })"> get_app </v-icon>
          <v-icon small @click="deleteItem(props.item)"> delete </v-icon>
        </td>
      </template>
    </v-data-table>
  </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../common'
import { buildApiUrl } from '@/common'

export default {
  name: 'Results',
  data () {
    return {
      pagination: {
        sortBy: 'created',
        descending: true
      },
      deleteDialog: false,
      selectedItem: '',
      query: '',
      headers: [
        { text: 'Result ID', value: 'id', align: 'left', sortable: true },
        { text: 'Method', value: 'method', align: 'left' },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Status', value: 'status', align: 'left' },
        { text: 'Actions', value: 'actions', align: 'center', sortable: false }
      ]
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate),
    downloadItem (downloadResultObject) {
      console.log('--- downloadItem ---')
      clearInterval(this.polling)
      window.open(buildApiUrl(`results/${downloadResultObject.id}/download`))
      this.pollData()
    },
    async confirmDelete () {
      console.log('--- delete result confirmed ---')
      // console.log(JSON.stringify(this.selectedItem, null, 2))
      await this.$store.dispatch('deleteResult', this.selectedItem.id)
      this.deleteDialog = false
    },
    deleteItem (item) {
      this.selectedItem = item
      this.deleteDialog = true
    },
    updateResultStatus () {
      this.$store.dispatch('loadResults', {
        query: this.query,
        loading: false
      })
    },
    pollData () {
      this.polling = setInterval(() => {
        this.updateResultStatus()
      }, 2000)
    }
  },
  computed: {
    ...mapGetters({ results: 'getResults', resultCount: 'getResultCount', loading: 'getLoading' })
  },
  created () {
    this.pollData()
  },
  beforeDestroy () {
    clearInterval(this.polling)
    this.query = ''
  },
  watch: {
    pagination: {
      handler () {
        this.query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadResults', {
          query: this.query,
          loading: true
        })
      },
      deep: true
    }
  }
}
</script>
