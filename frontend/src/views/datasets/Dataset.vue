<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
    <v-container fluid>

      <v-dialog v-model="deleteDialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Delete Dataset Version</span>
          </v-card-title>
          <v-card-text>
            Would you like to delete dataset version: {{this.selectedItem.id}} ?
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="deleteDialog = false">Cancel</v-btn>
            <v-btn color="red" @click="confirmDelete">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
        <v-card light>
          <v-toolbar color="cyan" dark>
            <v-toolbar-items>
              <router-link to="/datasets" tag="button">
                <v-icon>arrow_back</v-icon>
                </router-link>
            </v-toolbar-items>
            <v-toolbar-title>Dataset Version Overview</v-toolbar-title>

            <v-spacer></v-spacer>
            <v-dialog v-model="uploadDialog" max-width="600px">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" dark class="mb-2" v-on="on">Add Version</v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">Upload Dataset Version</span>
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
                    <v-btn color="green" @click="uploadDatasetVersion()">Upload</v-btn>
                  </v-card-actions>
                </v-container>
              </v-card>
            </v-dialog>
            <v-btn icon>
              <v-icon>search</v-icon>
            </v-btn>
          </v-toolbar>
          <v-list two-line >
            <v-layout row>
              <v-spacer></v-spacer>
              <v-list-tile >
                <v-list-tile-content>
                  <v-list-tile-title>Dataset Name:</v-list-tile-title>
                  <v-list-tile-sub-title v-text="dataset.name"></v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-spacer></v-spacer>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Dataset ID:</v-list-tile-title>
                  <v-list-tile-sub-title v-text="dataset.id"></v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-spacer></v-spacer>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Dataset Description:</v-list-tile-title>
                  <v-list-tile-sub-title v-text="dataset.description"></v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-spacer></v-spacer>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Dataset License:</v-list-tile-title>
                  <v-list-tile-sub-title v-text="dataset.license"></v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-spacer></v-spacer>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Dataset Maintainer:</v-list-tile-title>
                  <v-list-tile-sub-title v-text="dataset.maintainer"></v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-spacer></v-spacer>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Dataset Creation Time:</v-list-tile-title>
                  <v-list-tile-sub-title v-text="convertDate(dataset.created)"></v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-spacer></v-spacer>
            </v-layout>
          </v-list>
        </v-card>

      <v-data-table
        :headers="headers"
        :items="datasetVersions"
        :pagination.sync="pagination"
        :total-items="datasetVersionCount"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:items="props">
          <td>{{ props.item.id }}</td>
          <td class="text-xs-left">{{ convertDate(props.item.created) }}</td>
          <td class="text-xs-left">{{ props.item.description }}</td>
          <td class="justify-center layout px-0">
            <v-icon small class="mr-2" @click="editItem(props.item)"> edit </v-icon>
            <v-icon small @click="deleteItem(props.item)"> delete </v-icon>
          </td>
        </template>
      </v-data-table>
    </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import FileUploadSelector from '../../components/FileUploadSelector'
import { formatDate } from '../../common'

export default {
  name: 'Datasets',
  components: { FileUploadSelector },
  data () {
    return {
      selectedFile: null,
      deleteDialog: false,
      selectedItem: '',
      uploadDialog: false,
      pagination: {},
      headers: [
        { text: 'Version Id', align: 'left', sortable: false, value: 'id' },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Description', value: 'description', align: 'left', sortable: false },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({
      datasetVersions: 'getDatasetVersions',
      datasetVersionCount: 'getDatasetVersionCount',
      loading: 'getLoading',
      currentUploadChunk: 'getCurrentUploadChunk'
    }),
    formTitle () {
      return this.editedIndex === '' ? 'Add Version' : 'Edit Version'
    },
    dataset () {
      // console.log('hello', this.$route.params.datasetId, this.$store.getters['getDatasetById'](this.$route.params.datasetId))
      return this.$store.getters['getDatasetById'](this.$route.params.datasetId)
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate),
    editItem (item) {
      // console.log('--- editItem ---')
      // console.log(JSON.stringify(item, null, 2))
      this.selectedItem = item
    },
    deleteItem (item) {
      this.selectedItem = item
      this.deleteDialog = true
    },
    async confirmDelete () {
      console.log('--- delete confirmed ---')
      // console.log(JSON.stringify(this.selectedItem, null, 2))
      await this.$store.dispatch('deleteDatasetVersion', {
        datasetId: this.$route.params.datasetId,
        versionId: this.selectedItem.id
      })
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
    async uploadDatasetVersion () {
      if (this.selectedFile) {
        await this.$store.dispatch('uploadDatasetVersion', {
          datasetId: this.$route.params.datasetId,
          file: this.selectedFile
        })
        this.dialogPollingMonitor = setInterval(() => {
          this.uploadDialogCloser()
        }, 1000)
      } else {
        this.$store.commit('setAlert', { show: true, type: 'error', message: 'Please, select a dataset file first!' })
      }
    }
  },
  watch: {
    pagination: {
      handler () {
        const query = {
          limit: this.pagination.rowsPerPage,
          offset: this.pagination.page - 1,
          sortby: this.pagination.sortBy,
          order: this.pagination.descending ? 'desc' : 'asc'
        }
        this.$store.dispatch('loadDatasetVersions', { datasetId: this.$route.params.datasetId, query: query })
      },
      deep: true
    }
  }
}
</script>
