<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
    <v-container fluid>

      <v-dialog v-model="deleteDialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Delete Model Snapshot</span>
          </v-card-title>
          <v-card-text>
            Would you like to delete snapshot: {{this.selectedItem.id}} ?
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="deleteDialog = false">Cancel</v-btn>
            <v-btn color="red" @click="confirmDelete">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="createMethodDialog" max-width="600px">
        <v-card>
          <v-card-title>Create Method from Snapshot</v-card-title>
          <v-container>
            <v-layout row wrap>
              <MethodForm v-model="newMethod"></MethodForm>
            </v-layout>
            <v-layout row wrap>
              <v-btn color="primary" @click="createMethodDialog = false">Cancel</v-btn>
              <v-btn color="red" @click="confirmCreateMethod">Create Method</v-btn>
            </v-layout>
          </v-container>
        </v-card>
      </v-dialog>

      <v-card light>
        <v-toolbar color="cyan" dark>
          <v-toolbar-items>
            <router-link to="/models" tag="button">
              <v-icon>arrow_back</v-icon>
            </router-link>
          </v-toolbar-items>
          <v-toolbar-title v-if="providedModelId">Available Snapshots</v-toolbar-title>
          <v-toolbar-title v-else>Model Snapshots Overview<template v-if="loading"> (Creating training pipeline - please be patient)</template></v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn icon>
            <v-icon>search</v-icon>
          </v-btn>
        </v-toolbar>
        <v-list v-if="modelVersion" two-line >
          <v-layout row>
            <v-spacer></v-spacer>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Model Version ID:</v-list-tile-title>
                <v-list-tile-sub-title v-text="modelVersion.id"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Model Commit ID:</v-list-tile-title>
                <v-list-tile-sub-title v-text="modelVersion['git_commit_id']"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Model Version Description:</v-list-tile-title>
                <v-list-tile-sub-title v-text="modelVersion.description"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Model Version Author:</v-list-tile-title>
                <v-list-tile-sub-title v-text="modelVersion.author"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Model Version Creation Date:</v-list-tile-title>
                <v-list-tile-sub-title v-text="convertDate(modelVersion.created)"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
          </v-layout>
        </v-list>
      </v-card>

      <v-data-table
        :headers="headers"
        :items="Snapshots"
        :pagination.sync="pagination"
        :total-items="SnapshotCount"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:items="props">
          <td>{{ props.item.id }}</td>
          <td class="text-xs-left">{{ convertDate(props.item['created']) }}</td>
          <td class="text-xs-left">{{ props.item['dataset_version'].name }}</td>
          <td class="text-xs-left">{{ props.item['model'].name }}</td>
          <td class="text-xs-left">{{ props.item.status }}</td>
          <td class="text-xs-left">{{ props.item.success }}</td>
          <td class="justify-center layout px-0">
            <v-btn v-if="props.item.success === 'True' && props.item.status === 'finished'" color="green" @click="createMethod(props.item.id)">Create Method</v-btn>
            <v-btn v-else color="blue" @click="$store.commit('setAlert', { show: true, type: 'info', message: `Snapshot failed or is not ready yet.` })">Create Method</v-btn>
            <v-icon v-if="props.item.status === 'finished'" small @click="downloadItem(props.item)"> get_app </v-icon>
            <v-icon v-else small @click="$store.commit('setAlert', { show: true, type: 'info', message: `Snapshot is not finished yet. Please be patient.` })"> get_app </v-icon>
            <v-icon small @click="deleteItem(props.item)"> delete </v-icon>
          </td>
        </template>
      </v-data-table>
    </v-container>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import { paginationToQuery, formatDate } from '../../common'
import MethodForm from './MethodForm'
import { buildApiUrl } from '@/common'

export default {
  name: 'Snapshots',
  components: { MethodForm },
  data () {
    return {
      providedModelId: null,
      providedGitCommitId: null,
      deleteDialog: false,
      createMethodDialog: false,
      selectedItem: '',
      editedIndex: '',
      query: '',
      newMethod: {
        name: 'Segmentation Method',
        description: 'Hippocampus Segmenting Method',
        snapshotId: ''
      },
      pagination: {
        sortBy: 'created',
        descending: true
      },
      headers: [
        { text: 'Model Snapshot ID', value: 'created', align: 'left', sortable: true },
        { text: 'Created', value: 'date', align: 'left', sortable: true },
        { text: 'Dataset Name', value: 'dataset', align: 'left', sortable: true },
        { text: 'Model Name', value: 'modelId', align: 'left', sortable: true },
        { text: 'Status', value: 'status', align: 'left', sortable: true },
        { text: 'Success', value: 'success', align: 'left', sortable: true },
        { text: 'Actions', value: 'actions', align: 'center', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({
      Snapshots: 'getSnapshots',
      SnapshotCount: 'getSnapshotCount',
      loading: 'getLoading'
    }),
    modelVersion () {
      return this.$store.getters['getModelVersionByGitCommitId'](this.providedGitCommitId)
    },
    formTitle () {
      return this.editedIndex === '' ? 'Add Version' : 'Edit Version'
    }
  },
  methods: {
    downloadItem (downloadResultObject) {
      console.log('--- downloadItem ---')
      clearInterval(this.polling)
      window.open(buildApiUrl(`snapshot/${downloadResultObject.id}/download`))
      this.pollData()
    },
    loadParams () {
      this.providedModelId = this.$route.params.modelId
      this.providedGitCommitId = this.$route.params.gitCommitId

      // this.$store.dispatch('loadModelVersions', { modelId: this.providedModelId, query: paginationToQuery(this.pagination) })

      // console.log(JSON.stringify(this.providedModelId, null, 2))
      // console.log(JSON.stringify(this.providedGitCommitId, null, 2))
    },
    destroyParams () {
      this.providedModelId = null
      this.providedGitCommitId = null
      this.query = ''
    },
    convertDate: strDate => formatDate(strDate),
    editItem (item) {
      // console.log('--- editItem ---')
      // console.log(JSON.stringify(item, null, 2))
    },
    createMethod (modelSnapshotId) {
      this.newMethod.snapshotId = modelSnapshotId
      this.createMethodDialog = true
    },
    async confirmCreateMethod () {
      if (this.newMethod.name && this.newMethod.description) {
        this.createMethodDialog = false
        console.log('--- create Method confirmed ---')
        // console.log(JSON.stringify(this.selectedItem, null, 2))
        await this.$store.dispatch('createMethod', {
          'name': this.newMethod.name,
          'description': this.newMethod.description,
          'modelSnapshotId': this.newMethod.snapshotId
        })
      } else {
        this.$store.commit('setAlert', { show: true, type: 'error', message: 'Please provide a name and a description for the method!' })
      }
    },
    deleteItem (item) {
      this.selectedItem = item
      this.deleteDialog = true
    },
    async confirmDelete () {
      console.log('--- delete snapshot confirmed ---')
      // console.log(JSON.stringify(this.selectedItem, null, 2))
      await this.$store.dispatch('deleteSnapshot', this.selectedItem.id)
      this.deleteDialog = false
    },
    updateSnapshotStatus () {
      if (this.providedModelId) {
        this.$store.dispatch('loadModelVersionSnapshots', {
          modelId: this.providedModelId,
          gitCommitId: this.providedGitCommitId,
          query: this.query,
          loading: false
        })
      } else {
        this.$store.dispatch('loadSnapshots', {
          query: this.query,
          loading: false
        })
      }
    },
    pollData () {
      this.polling = setInterval(() => {
        this.updateSnapshotStatus()
      }, 2000)
    }
  },
  created () {
    this.loadParams()
    this.pollData()
  },
  beforeDestroy () {
    this.destroyParams()
    clearInterval(this.polling)
  },
  watch: {
    pagination: {
      handler () {
        this.query = paginationToQuery(this.pagination)
        if (this.providedModelId) {
          this.$store.dispatch('loadModelVersionSnapshots', {
            modelId: this.providedModelId,
            gitCommitId: this.providedGitCommitId,
            query: this.query,
            loading: true
          })
        } else {
          this.$store.dispatch('loadSnapshots', {
            query: this.query,
            loading: true
          })
        }
      },
      deep: true
    }
  }
}
</script>
