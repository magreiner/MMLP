<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-layout column>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Select the Model Version:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="modelVersions"
      :pagination.sync="pagination"
      :total-items="modelVersionCount"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <tr @click="$emit('select', props.item)">
          <td>{{ props.item.id }}</td>
          <td class="text-xs-left">{{ convertDate(props.item.created) }}</td>
          <td class="text-xs-left">{{ props.item.author }}</td>
          <td class="text-xs-left">{{ props.item.description }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../../common'

export default {
  name: 'ViewModelVersions',
  props: {
    modelId: {
      required: true,
      type: String
    }
  },
  data () {
    return {
      pagination: {
        sortBy: 'Created',
        descending: true
      },
      headers: [
        { text: 'Version ID', align: 'left', sortable: false, value: 'id' },
        { text: 'Created', value: 'date', align: 'left' },
        { text: 'Author', value: 'author', align: 'left' },
        { text: 'Description', value: 'description', align: 'left', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({
      modelVersions: 'getModelVersions',
      modelVersionCount: 'getModelVersionCount',
      loading: 'getLoading'
    })
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  },
  watch: {
    pagination: {
      handler () {
        const query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadModelVersions', { modelId: this.modelId, query: query })
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
