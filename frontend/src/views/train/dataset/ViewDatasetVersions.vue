<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-layout column>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Select the Dataset Version:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="datasetVersions"
      :pagination.sync="pagination"
      :total-items="datasetVersionCount"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <tr @click="$emit('select', props.item)">
          <td>{{ props.item.id }}</td>
          <td class="text-xs-left">{{ convertDate(props.item.created) }}</td>
          <td class="text-xs-left">{{ props.item.description }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import { formatDate } from '../../../common'

export default {
  name: 'SelectDatasetVersion',
  props: {
    datasetId: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      pagination: {
        sortBy: 'created',
        descending: true
      },
      headers: [
        {
          text: 'Version Id',
          align: 'left',
          sortable: false,
          value: 'id'
        },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Description', value: 'description', align: 'left', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({
      datasetVersions: 'getDatasetVersions',
      datasetVersionCount: 'getDatasetVersionCount',
      loading: 'getLoading'
    })
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  },
  watch: {
    pagination: {
      handler () {
        // TODO: Update this with the utility function
        const query = {
          limit: this.pagination.rowsPerPage,
          offset: this.pagination.page - 1,
          sortby: this.pagination.sortBy,
          order: this.pagination.descending ? 'desc' : 'asc'
        }
        this.$store.dispatch('loadDatasetVersions', { datasetId: this.datasetId, query: query })
      },
      deep: true
    }
  }
}
</script>

<style scoped>
  td {
    cursor: pointer;
  }
</style>
