<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-card color="white">
    <v-toolbar flat color="cyan">
      <v-icon>list_alt</v-icon>
      <v-toolbar-title>Adjust the model configuration as needed:</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>

    <v-layout>
      <v-flex>
        <v-card-text>
          <v-treeview
            v-model="tree"
            :items="modelParameterTree.children"
            activatable
            active-class="grey lighten-4 indigo--text"
            selected-color="indigo"
            selectable
            open-on-click
            expand-icon="expand_more"
            light
          >
            <template v-slot:prepend="{ item, open }">
              <v-icon v-if="item.children && !open">folder</v-icon>
              <v-icon v-if="item.children && open">folder_open</v-icon>
            </template>
            <template v-slot:label="{ item }">
              <span class="body-1">{{item.name}}</span>
            </template>
          </v-treeview>

        </v-card-text>
      </v-flex>

      <v-divider vertical light></v-divider>

      <v-flex xs12 md6>

        <v-layout row wrap v-if="showEditBox" align-center>
          <v-flex xs11 md11 pl-3 pt-2>
            <v-text-field :label="selected.name" light flat v-model="selected.value"></v-text-field>
          </v-flex>
          <v-flex xs1 md1 pt-2>
            <v-icon small light @click="save">save</v-icon>
            <v-icon small light @click="reset">clear</v-icon>
          </v-flex>
        </v-layout>

        <v-layout row wrap>
          <v-card-text>

            <v-list dense light>
              <v-list-tile v-for="parameter in selections" :key="parameter.id">
                <v-list-tile-content>
                  <v-list-tile-title>{{parameter.name}}</v-list-tile-title>
                  <v-list-tile-sub-title>{{parameter.value}}</v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-icon v-if="parameter.id !== selected.id" small @click="onEdit(parameter)" >
                    edit
                  </v-icon>
                  <v-icon v-else>chevron_left</v-icon>
                </v-list-tile-action>
              </v-list-tile>
            </v-list>

          </v-card-text>
        </v-layout>

      </v-flex>
    </v-layout>

    <v-divider></v-divider>
  </v-card>

</template>

<script>
import { mapGetters } from 'vuex'
import { findTreeNodeById } from '../../../common'

export default {
  name: 'ModelParameters',
  data: () => ({
    tree: [],
    selected: {
      id: 0,
      name: '',
      value: ''
    }
  }),
  computed: {
    ...mapGetters({ modelParameterTree: 'getModelParameterTree' }),
    selections () {
      // Selected items ids are held in the [tree] Array
      return this.tree
        .map(id => findTreeNodeById(id, this.modelParameterTree))
        .filter(node => !node.children)
    },
    showEditBox () {
      return this.selections.find(p => p.id === this.selected.id)
    }

  },
  methods: {
    onEdit (parameter) {
      this.selected = {
        id: parameter.id,
        name: parameter.name,
        value: parameter.value
      }
    },
    reset () {
      this.selected = {
        id: 0,
        name: '',
        value: ''
      }
    },
    save () {
      this.$store.commit('setModelParameterValue', { id: this.selected.id, value: this.selected.value })
      this.reset()
    }
  }
}
</script>

<style scoped>

</style>
