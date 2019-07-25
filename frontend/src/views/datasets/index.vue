<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-container fluid>

    <v-dialog v-model="deleteDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Delete Dataset</span>
        </v-card-title>
        <v-card-text>
          Would you like to delete dataset: {{this.selectedDataset.name}} ?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-toolbar flat color="cyan">
      <v-toolbar-title>Dataset Overview</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-dialog v-model="uploadDialog" max-width="600px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark class="mb-2" v-on="on">Upload Dataset</v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">Upload Dataset</span>
          </v-card-title>
          <v-container v-if="loading">
              <div class="text-xs-center">
              <v-spacer></v-spacer>
              <v-progress-circular
                :size="100"
                :width="15"
                :value="currentUploadChunk"
                color="teal"
              >
                {{ currentUploadChunk }}
              </v-progress-circular>
              <v-card-text v-if="currentUploadChunk < 100">Uploading data, please wait ...</v-card-text>
              <v-card-text v-else-if="loading">Processing, please wait.</v-card-text>
              <v-spacer></v-spacer>
              </div>
          </v-container>
          <v-container v-else>
          <FileUploadSelector @select="selectFile"></FileUploadSelector>
          <v-card-actions>
            <v-btn color="primary" @click="uploadDialog = false">Cancel</v-btn>
            <v-btn color="green" @click="uploadDataset()">Upload</v-btn>
          </v-card-actions>
          </v-container>
        </v-card>
      </v-dialog>

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
        <tr>
          <td @click="showVersions(props.item.id)">{{ props.item.name }}</td>
          <td @click="showVersions(props.item.id)" class="text-xs-left">{{ convertDate(props.item.created) }}</td>
          <td @click="showVersions(props.item.id)" class="text-xs-left">{{ props.item.maintainer }}</td>
          <td @click="showVersions(props.item.id)" class="text-xs-left">{{ props.item.origin }}</td>
          <td @click="showVersions(props.item.id)" class="text-xs-left">{{ props.item.license }}</td>
          <td class="justify-center layout px-0">
            <v-icon
              small
              class="mr-2"
              @click="showVersions(props.item.id)"
            >
              format_list_numbered
            </v-icon>
            <v-icon
              small
              class="mr-2"
              @click="editItem(props.item)"
            >
              edit
            </v-icon>
            <v-icon
              small
              @click="deleteItem(props.item)"
            >
              delete
            </v-icon>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../common'
import FileUploadSelector from '../../components/FileUploadSelector'

export default {
  name: 'Datasets',
  components: { FileUploadSelector },
  data () {
    return {
      selectedFile: null,
      selectedDataset: '',
      uploadDialog: false,
      deleteDialog: false,
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
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Maintainer', value: 'maintainer', align: 'left' },
        { text: 'Data Origin', value: 'origin', align: 'left' },
        { text: 'License', value: 'license', align: 'left' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({ datasets: 'getDatasets', datasetCount: 'getDatasetCount', loading: 'getLoading', currentUploadChunk: 'getCurrentUploadChunk' }),
    formTitle () {
      return this.selectedDatasetId === '' ? 'Add Dataset' : 'Edit Dataset'
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate),
    showVersions (datasetId) {
      this.$router.push(`/datasets/${datasetId}`)
    },
    editItem (item) {
      console.log('--- editItem ---')
      // console.log(JSON.stringify(item, null, 2))
      this.selectedDataset = item
      // this.dialog = true
    },
    deleteItem (item) {
      this.selectedDataset = item
      this.deleteDialog = true
    },
    async confirmDelete () {
      console.log('--- delete confirmed ---')
      // console.log(JSON.stringify(this.selectedDataset, null, 2))
      await this.$store.dispatch('deleteDataset', this.selectedDataset.id)
      this.deleteDialog = false
    },
    selectFile (file) { this.selectedFile = file },
    uploadDialogCloser () {
      if (this.dialogPollingMonitor) {
        if (!this.loading) {
          this.uploadDialog = false
          clearInterval(this.dialogPollingMonitor)
        }
      }
    },
    async uploadDataset () {
      if (this.selectedFile) {
        await this.$store.dispatch('uploadDataset', this.selectedFile)
        this.dialogPollingMonitor = setInterval(() => {
          this.uploadDialogCloser()
        }, 1000)
        // this.uploadDialog = false
      } else {
        this.$store.commit('setAlert', { show: true, type: 'error', message: 'Please, select a dataset file first!' })
      }
    }
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
