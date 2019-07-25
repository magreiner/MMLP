<template>
  <v-card>
    <v-toolbar flat color="cyan">
      <v-toolbar-title>Verify your model selection:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text>
      <v-list two-line>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model Name:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ modelVersion.name }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model Id:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ modelVersion.model }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Author:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ modelVersion.author }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Description:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ modelVersion.description }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Model Version Id:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ modelVersion.id }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title>Created At:</v-list-tile-title>
            <v-list-tile-sub-title class="align-end">{{ convertDate(modelVersion.created) }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { formatDate } from '../../../common'
export default {
  name: 'ModelVersionInfo',
  props: {
    modelVersion: {
      type: Object,
      required: true
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  }
}
</script>
