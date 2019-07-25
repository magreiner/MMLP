<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
  <v-container fluid>

    <v-dialog v-model="deleteDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Delete Method</span>
        </v-card-title>
        <v-card-text>
          Would you like to delete method: {{this.selectedItem.name}} ?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-toolbar flat color="cyan">
      <v-toolbar-title>Method Overview</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-btn color="green" @click="$router.push('/analyze')"> Go To Analyze ...</v-btn>
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
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.description }}</td>
        <td>{{ props.item['model_snapshot'].model.name }}</td>
        <td>{{ convertDate(props.item.created) }}</td>
        <td class="justify-center layout px-0">
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
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate),
    async confirmDelete () {
      console.log('--- delete method confirmed ---')
      // console.log(JSON.stringify(this.selectedItem, null, 2))
      await this.$store.dispatch('deleteMethod', this.selectedItem.id)
      this.deleteDialog = false
    },
    deleteItem (item) {
      this.selectedItem = item
      this.deleteDialog = true
    }
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
