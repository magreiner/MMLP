<template>
  <v-card>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Verify your selection:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text>
      <v-list two-line>
        <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>Dataset Name:</v-list-tile-title>
          <v-list-tile-sub-title class="align-end">{{ datasetVersion.name }}</v-list-tile-sub-title>
        </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Dataset ID:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ datasetVersion.parent_id }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Description:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ datasetVersion.description }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Dataset Version ID:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ datasetVersion.id }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Version Created At:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ convertDate(datasetVersion.created) }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { formatDate } from '../../../common'
export default {
  name: 'DatasetVersionInfo',
  props: {
    datasetVersion: {
      type: Object,
      required: true
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  }
}
</script>
