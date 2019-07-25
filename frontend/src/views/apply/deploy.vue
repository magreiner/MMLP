<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
    <v-layout row wrap mb-1>
      <v-flex>
        <v-card light>
          <v-toolbar flat dark color="cyan">
            <v-icon>storage</v-icon>
            <v-toolbar-title>Analyze Details:</v-toolbar-title>

            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-list two-line>
              <v-list-tile v-if="patientCohortFile">
                <v-list-tile-content>
                  <v-list-tile-title>Patient Cohort Archive:</v-list-tile-title>
                  <v-list-tile-sub-title>{{patientCohortFile.name}}</v-list-tile-sub-title>

                </v-list-tile-content>
              </v-list-tile>
              <v-list-tile v-if="method">
                <v-list-tile-content>
                  <v-list-tile-title>Selected Method -  <span class="caption">{{method.id}}</span></v-list-tile-title>
                  <v-list-tile-sub-title>{{convertDate(method.created)}} - {{method.description}}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-content>
</template>

<script>
import { formatDate } from '../../common'
import { mapGetters } from 'vuex'

export default {
  name: 'MethodApplicationDeployment',
  props: {
    patientCohortFile: {
      required: true
    },
    method: {
      required: true
    },
    computed: {
      ...mapGetters({ mode: 'getMode' })
    }
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  }
}
</script>
