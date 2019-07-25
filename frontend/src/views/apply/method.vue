<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
    <v-container fluid>
      <v-toolbar flat color="cyan">
        <v-toolbar-title>Please select the method:</v-toolbar-title>

        <v-spacer></v-spacer>
      </v-toolbar>
      <v-data-table
        :headers="headers"
        :items="methods"
        :pagination.sync="pagination"
        :total-items="methodCount"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:items="props">
          <tr @click="$emit('select', props.item)">
            <td>{{ props.item.name }}</td>
            <td>{{ props.item.description }}</td>
            <td>{{ props.item['model_snapshot'].model.name }}</td>
            <td>{{ convertDate(props.item.created) }}</td>
          </tr>
        </template>
      </v-data-table>
    </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../common'

export default {
  name: 'Methods',
  data () {
    return {
      pagination: {
        sortBy: 'created',
        descending: true
      },
      deleteDialog: false,
      selectedItem: '',
      headers: [
        { text: 'Method Name', value: 'name', align: 'left', sortable: true },
        { text: 'Description', value: 'description', align: 'left' },
        { text: 'Model Name', value: 'model', align: 'left' },
        { text: 'Created', value: 'created', align: 'left' }
      ]
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  },
  computed: {
    ...mapGetters({ methods: 'getMethods', methodCount: 'getMethodCount', loading: 'getLoading' })
  },
  watch: {
    pagination: {
      handler () {
        const query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadMethods', query)
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
