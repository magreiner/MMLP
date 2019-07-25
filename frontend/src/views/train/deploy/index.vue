<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-content>
    <v-layout row wrap mb-1>
      <v-flex>
        <v-card light>
          <v-toolbar flat dark color="cyan">
            <v-icon>storage</v-icon>
            <v-toolbar-title>Model Training Selection:</v-toolbar-title>

            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-list two-line>
              <v-list-tile v-if="datasetVersion">
                <v-list-tile-content>
                  <v-list-tile-title>Dataset Version - <span class="caption">{{datasetVersion.id}}</span></v-list-tile-title>
                  <v-list-tile-sub-title>{{convertDate(datasetVersion.created)}} - {{datasetVersion.description}}</v-list-tile-sub-title>

                </v-list-tile-content>
              </v-list-tile>
              <v-list-tile v-if="modelVersion">
                <v-list-tile-content>
                  <v-list-tile-title>Selected Model Version - <span class="caption">{{modelVersion.id}}</span></v-list-tile-title>
                  <v-list-tile-sub-title>{{convertDate(modelVersion.created)}} - {{modelVersion.description}}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-list-tile v-if="snapshot">
                <v-list-tile-content>
                  <v-list-tile-title>Selected Model Snapshot <span class="caption">{{snapshot.id}}</span></v-list-tile-title>
                  <v-list-tile-sub-title>{{convertDate(snapshot.created)}}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex>
        <v-card light>
          <v-toolbar flat dark color="cyan">
            <v-icon>list_alt</v-icon>
            <v-toolbar-title>Model Parameters:</v-toolbar-title>

            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-treeview :items="modelParameterTree.children" expand-icon="expand_more" open-on-click>
              <template v-slot:label="{ item }">
                <span v-if="item.children" class="body-1">{{item.name}}</span>
                <span v-else class="body-1">{{item.name}}: {{item.value}}</span>
              </template>
              <template v-slot:prepend="{ item, open }">
                <v-icon v-if="item.children && !open">folder</v-icon>
                <v-icon v-if="item.children && open">folder_open</v-icon>
              </template>
            </v-treeview>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout v-if="Object.keys(modelParameterTree).length !== 0" row>
      <v-flex>
        <v-list two-line>
          <v-card light>
            <v-toolbar flat dark color="cyan">
              <v-icon>storage</v-icon>
              <v-toolbar-title>Available Experiment Live Tracking Services for this Model:</v-toolbar-title>

              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <!--        v-for="(service, index) in new_experiment.method.monitoring"-->
              <v-list-tile avatar>
                <v-list-tile-avatar>
                  <v-icon class="accessible_forward">live_tv</v-icon>
                </v-list-tile-avatar>

                <v-list-tile-content>
                  <v-list-tile-title>{{ modelParameterTree.children[0].children[0].value }}</v-list-tile-title>
                  <v-list-tile-sub-title><a :href="base_url + ':' + modelParameterTree.children[0].children[2].value" target="_blank">Connect to {{modelParameterTree.children[0].children[0].value}}</a><br></v-list-tile-sub-title>
                </v-list-tile-content>

                <!--            <v-list-tile-action>-->
                <!--              <v-btn icon ripple>-->
                <!--                <v-icon color="grey lighten-1">info</v-icon>-->
                <!--              </v-btn>-->
                <!--            </v-list-tile-action>-->
              </v-list-tile>
            </v-card-text>
          </v-card>
        </v-list>
      </v-flex>
    </v-layout>
  </v-content>
</template>

<script>
import { mapGetters } from 'vuex'
import { formatDate } from '../../../common'

export default {
  name: 'ModelTrainingDeploy',
  data () {
    return {
      base_url: 'http://' + window.location.hostname
    }
  },
  props: {
    datasetVersion: {
      required: true
    },
    modelVersion: {
      required: true
    },
    snapshot: {
      required: true
    }
  },
  computed: {
    ...mapGetters({ modelParameterTree: 'getModelParameterTree' })
  },
  methods: {
    convertDate: strDate => formatDate(strDate)
  }
}
</script>
