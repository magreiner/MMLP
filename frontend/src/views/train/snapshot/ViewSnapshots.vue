<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-layout column>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Select the model snapshot (only matching snapshots are shown):</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="snapshots"
      :pagination.sync="pagination"
      :total-items="snapshotCount"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <tr @click="$emit('select', props.item)">
          <td>{{ props.item.id }}</td>
          <td class="text-xs-left">{{ convertDate(props.item.created) }}</td>
          <td class="text-xs-left">{{ props.item['dataset_version'].name}}</td>
          <td class="text-xs-left">{{ props.item.status}}</td>
        </tr>
      </template>
    </v-data-table>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../../common'

export default {
  name: 'ViewSnapshots',
  props: {
    modelVersion: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      pagination: {
        sortBy: 'Created',
        descending: true
      },
      headers: [
        { text: 'Snapshot ID', align: 'left', sortable: false, value: 'id' },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Dataset Name', value: 'dataset', align: 'left', sortable: false },
        { text: 'Status', value: 'status', align: 'left', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({
      snapshots: 'getSnapshots',
      snapshotCount: 'getSnapshotCount',
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
        this.$store.dispatch('loadModelVersionSnapshots', {
          modelId: this.modelVersion.model,
          gitCommitId: this.modelVersion.git_commit_id,
          query: query,
          loading: true
        })
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
