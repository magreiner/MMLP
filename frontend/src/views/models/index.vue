<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
  <v-container fluid>

    <v-dialog v-model="deleteDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Delete Model</span>
        </v-card-title>
        <v-card-text>
          Would you like to delete model: {{this.selectedModel.name}} ?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-toolbar flat color="cyan">
      <v-toolbar-title>Model Overview</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-dialog v-model="importDialog" max-width="800px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark class="mb-2" v-on="on">Import Model</v-btn>
        </template>
        <v-card>
          <v-card-title>Import Model</v-card-title>
          <v-container>
            <v-layout row wrap>
              <ModelForm v-model="importModel"></ModelForm>
            </v-layout>
            <v-layout row wrap>
              <v-btn color="primary" @click="importDialog = false">Cancel</v-btn>
              <v-btn color="green" @click="importModelDialog">Import Model</v-btn>
            </v-layout>
          </v-container>
        </v-card>
      </v-dialog>
      <v-btn color="green" dark class="mb-2" @click="$router.push('/train')">Train Model</v-btn>
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
        <tr>
          <td @click="showVersions(props.item.id)">{{ props.item.name }}</td>
          <td @click="showVersions(props.item.id)">{{ convertDate(props.item.created) }}</td>
          <td>
<!--            <a :href="props.item.source_url">{{ props.item.source_url }}</a>-->
            {{ props.item.source_url }}
          </td>
          <td class="justify-center layout px-0">
<!--            <v-icon small class="mr-2" @click="showVersions(props.item.id)"> format_list_numbered </v-icon>-->
            <v-icon small class="mr-2" @click="updateModel(props.item)"> refresh </v-icon>
<!--            <v-icon small class="mr-2"> edit </v-icon>-->
            <v-icon small class="mr-2" @click="deleteItem(props.item)"> delete </v-icon>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../common'
import ModelForm from './ModelForm'

export default {
  name: 'Models',
  components: { ModelForm },
  data () {
    return {
      selectedModel: '',
      deleteDialog: false,
      importModel: {
        source_url: 'git@github.com:magreiner/unet-docker.git',
        name: 'Import Test Model'
      },
      importDialog: false,
      pagination: {
        sortBy: 'created',
        descending: true
      },
      headers: [
        { text: 'Model Name', value: 'name', align: 'left', sortable: true },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Origin', value: 'source_url', align: 'left' },
        { text: 'Actions', value: 'actions', align: 'center', sortable: false }
      ]
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate),
    async importModelDialog () {
      if (this.importModel.source_url) {
        this.importDialog = false
        await this.$store.dispatch('importModel', this.importModel)
      } else {
        this.$store.commit('setAlert', { show: true, type: 'error', message: 'Please provide a source url!' })
      }
    },
    deleteItem (item) {
      this.selectedModel = item
      this.deleteDialog = true
    },
    async confirmDelete () {
      console.log('--- delete confirmed ---')
      // console.log(JSON.stringify(this.selectedModel, null, 2))
      await this.$store.dispatch('deleteModel', this.selectedModel.id)
      this.deleteDialog = false
    },
    updateModel (item) {
      console.log('--- update model --')
      this.$store.dispatch('updateModel', item.id)
    },
    showVersions (modelId) {
      this.$router.push(`/models/${modelId}`)
    }
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
