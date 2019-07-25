<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
  <v-container fluid>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Current System Status</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="statusRunning"
      :pagination.sync="pagination"
      :total-items="statusRunningCount"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <td>{{ props.item.name }}</td>
        <td class="text-xs-left">{{ convertDate(props.item.start) }}</td>
        <td class="text-xs-left">{{ props.item.runtime }}</td>
        <td class="justify-center layout px-0">
          <v-icon
            small
            class="mr-2"
            @click="$store.dispatch('stopExperiment', props.item)"
          >
            stop
          </v-icon>
        </td>
      </template>
    </v-data-table>
  </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../common'

export default {
  name: 'Experiments',
  data () {
    return {
      pagination: {},
      headers: [
        { text: 'Name', align: 'left', sortable: true, value: 'name' },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Run Time', value: 'runtime', align: 'left' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  },
  computed: {
    ...mapGetters({
      statusRunning: 'getStatusRunning',
      statusRunningCount: 'getStatusRunningCount',
      loading: 'getLoading'
    })
  },
  watch: {
    pagination: {
      handler () {
        // this.$store.dispatch('loadExperiments', {
        //   limit: this.pagination.rowsPerPage,
        //   offset: this.pagination.page - 1,
        //   sortby: this.pagination.sortBy,
        //   order: this.pagination.descending ? 'desc' : 'asc'
        // })
        const query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadStatus', query)
      },
      deep: true
    }
  }
}
</script>
