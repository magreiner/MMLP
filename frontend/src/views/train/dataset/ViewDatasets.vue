<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <v-layout column>
      <v-toolbar flat color="cyan">
        <v-toolbar-title>Select the Dataset:</v-toolbar-title>

        <v-spacer></v-spacer>
      </v-toolbar>
      <v-data-table
        :headers="headers"
        :items="datasets"
        :pagination.sync="pagination"
        :total-items="datasetCount"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:items="props">
          <tr @click="$emit('select', props.item.id)">
            <td>{{ props.item.name }}</td>
            <td class="text-xs-left">{{ convertDate(props.item.created) }}</td>
            <td class="text-xs-left">{{ props.item.maintainer }}</td>
            <td class="text-xs-left">{{ props.item.origin }}</td>
            <td class="text-xs-left">{{ props.item.license }}</td>
          </tr>
        </template>
      </v-data-table>
    </v-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../../common'

export default {
  name: 'SelectDataset',
  data () {
    return {
      pagination: {
        sortBy: 'created',
        descending: true
      },
      headers: [
        {
          text: 'Dataset Name',
          align: 'left',
          sortable: true,
          value: 'name'
        },
        { text: 'Creation Date', value: 'created', align: 'left' },
        { text: 'Maintainer', value: 'maintainer', align: 'left' },
        { text: 'Data Origin', value: 'origin', align: 'left' },
        { text: 'License', value: 'license', align: 'left' }
      ]
    }
  },
  computed: {
    ...mapGetters({ datasets: 'getDatasets', datasetCount: 'getDatasetCount', loading: 'getLoading' })
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  },
  watch: {
    pagination: {
      handler () {
        const query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadDatasets', query)
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
