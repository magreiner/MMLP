<template>
  <v-card>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Verify the selected model snapshot:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text>
      <v-list two-line="">
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model Version Snapshot Id:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ snapshot.id }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Creation Date:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ convertDate(snapshot.created) }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Snapshot Dataset:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ snapshot.dataset_version.id }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Snapshot Model Id:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ snapshot.model.id }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { formatDate } from '../../../common'
export default {
  name: 'SnapshotInfo',
  props: {
    snapshot: {
      type: Object,
      required: true
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  }
}
</script>
