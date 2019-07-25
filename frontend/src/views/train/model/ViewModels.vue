<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-layout column>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Select the Model:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="models"
      :pagination.sync="pagination"
      :total-items="modelCount"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <tr @click="$emit('select', props.item.id)">
          <td>{{ props.item.name }}</td>
          <td>{{ convertDate(props.item.created) }}</td>
          <td>{{ props.item.maintainer }}</td>
          <td>{{ props.item.source_url }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../../common'

export default {
  name: 'Models',
  components: {},
  data () {
    return {
      pagination: {
        sortBy: 'created',
        descending: true
      },
      headers: [
        { text: 'Model Name', value: 'name', align: 'left', sortable: true },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Maintainer', value: 'maintainer', align: 'left' },
        { text: 'Origin', value: 'source_url', align: 'left' }
      ]
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  },
  computed: {
    ...mapGetters({ models: 'getModels', modelCount: 'getModelCount', loading: 'getLoading' })
  },
  watch: {
    pagination: {
      handler () {
        const query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadModels', query)
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
