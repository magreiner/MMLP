<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
    <v-container fluid>
      <v-card light>
        <v-toolbar color="cyan" dark>
          <v-toolbar-items>
            <router-link to="/models" tag="button">
              <v-icon>arrow_back</v-icon>
            </router-link>
          </v-toolbar-items>
          <v-toolbar-title>Model Version Overview</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn icon>
            <v-icon>search</v-icon>
          </v-btn>
        </v-toolbar>
        <v-list two-line >
          <v-layout row>
            <v-spacer></v-spacer>
            <v-list-tile >
              <v-list-tile-content>
                <v-list-tile-title>Model Name:</v-list-tile-title>
                <v-list-tile-sub-title v-text="model.name"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
            <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>Model ID:</v-list-tile-title>
              <v-list-tile-sub-title v-text="model.id"></v-list-tile-sub-title>
            </v-list-tile-content>
            </v-list-tile>
            <v-spacer></v-spacer>
          <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model Description:</v-list-tile-title>
            <v-list-tile-sub-title v-text="model.description"></v-list-tile-sub-title>
          </v-list-tile-content>
          </v-list-tile>
            <v-spacer></v-spacer>
          <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model License:</v-list-tile-title>
            <v-list-tile-sub-title v-text="model.license"></v-list-tile-sub-title>
          </v-list-tile-content>
          </v-list-tile>
            <v-spacer></v-spacer>
          <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model Maintainer:</v-list-tile-title>
            <v-list-tile-sub-title v-text="model.maintainer"></v-list-tile-sub-title>
          </v-list-tile-content>
          </v-list-tile>
            <v-spacer></v-spacer>
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>Model Creation Time:</v-list-tile-title>
              <v-list-tile-sub-title v-text="convertDate(model.created)"></v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
            <v-spacer></v-spacer>
          </v-layout>
        </v-list>
      </v-card>

        <!--        <v-list two-line>-->
<!--          <template v-for="(item, index) in modelVersions">-->
<!--            <v-subheader-->
<!--              v-if="item.header"-->
<!--              :key="item.header"-->
<!--            >-->
<!--              {{ item.header }}-->
<!--            </v-subheader>-->

<!--            <v-divider-->
<!--              v-else-if="item.divider"-->
<!--              :key="index"-->
<!--              :inset="item.inset"-->
<!--            ></v-divider>-->

<!--            <v-list-tile-->
<!--              v-else-->
<!--              :key="item.id"-->
<!--            >-->
<!--              <v-list-tile-content>-->
<!--                <v-list-tile-title>Model Version ID</v-list-tile-title>-->
<!--                <v-list-tile-sub-title v-text="item"></v-list-tile-sub-title>-->
<!--              </v-list-tile-content>-->
<!--            </v-list-tile>-->
<!--          </template>-->
<!--        </v-list>-->
<!--      </v-card>-->

      <v-data-table
        :headers="headers"
        :items="modelVersions"
        :pagination.sync="pagination"
        :total-items="modelVersionCount"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:items="props">
          <tr>
            <td @click="showVersions(props.item.git_commit_id)">{{ props.item.id }}</td>
            <td @click="showVersions(props.item.git_commit_id)" class="text-xs-left">{{ convertDate(props.item.created) }}</td>
            <td @click="showVersions(props.item.git_commit_id)" class="text-xs-left">{{ props.item.author }}</td>
            <td @click="showVersions(props.item.git_commit_id)" class="text-xs-left">{{ props.item.description }}</td>
<!--            <td class="justify-center layout px-0">-->
<!--              <v-icon small class="mr-2" @click="$router.push(`/models/${$route.params.modelId}/versions/${props.item.id}`)" > format_list_numbered </v-icon>-->
<!--            </td>-->
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
  name: 'Model',
  data () {
    return {
      deleteDialog: false,
      editedIndex: '',
      dialog: false,
      pagination: {
        sortBy: 'created',
        descending: true
      },
      headers: [
        { text: 'Version ID', align: 'left', sortable: true, value: 'id' },
        { text: 'Created', value: 'created', align: 'left' },
        { text: 'Author', value: 'author', align: 'left' },
        { text: 'Description', value: 'description', align: 'left' }
        // { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters({
      modelVersions: 'getModelVersions',
      modelVersionCount: 'getModelVersionCount',
      loading: 'getLoading'
    }),
    model () {
      return this.$store.getters.getModelById(this.$route.params.modelId)
    },
    formTitle () {
      return this.editedIndex === '' ? 'Add Version' : 'Edit Version'
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate),
    editItem (item) {
      // console.log('--- editItem ---')
      // console.log(JSON.stringify(item, null, 2))
    },
    deleteItem (item) {
      console.log('--- deleteItem ---')
      // console.log(JSON.stringify(item, null, 2))
      this.deleteDialog = true
    },
    onDelete () {
      console.log('--- onDelete ---')
      this.deleteDialog = false
    },
    showVersions (gitCommitId) {
      const modelId = this.$route.params.modelId
      // console.log(JSON.stringify(`/models/${modelId}/versions/${gitCommitId}`, null, 2))
      this.$router.push(`/models/${modelId}/versions/${gitCommitId}`)
    }
  },
  watch: {
    pagination: {
      handler () {
        const query = paginationToQuery(this.pagination)
        this.$store.dispatch('loadModelVersions', { modelId: this.$route.params.modelId, query: query })
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
