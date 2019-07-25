<template>
  <v-container fluid grid-list-md>
    <v-data-iterator
      :items="items"
      :rows-per-page-items="rowsPerPageItems"
      :pagination.sync="pagination"
      content-tag="v-layout"
      loading
      row
      wrap
      no-data-text='Generating some data for you ...'
    >
      <v-toolbar
        slot="header"
        class="mb-2"
        color="indigo darken-5"
        dark
        flat
      >
        <v-toolbar-title>{{ title }}</v-toolbar-title>
      </v-toolbar>

      <v-flex
        slot="item"
        slot-scope="props"
        xs12
        sm6
        md4
        lg3
      >
        <v-card>
          <v-card-title class="subheading font-weight-bold">{{ props.item.name }}</v-card-title>

          <v-divider></v-divider>

          <v-list>
            <div v-for="(value, key, index) in props.item.meta" :key="index">
              <!--<div v-if="key !== 'training' && key !== 'test'"></div>-->

              <!--Show errors instead of displaying nonsense-->
              <div v-if="key.toLowerCase() === 'error'">
                <v-alert :value="true" color="error" icon="warning">
                  Sorry: <b>'{{ value }}'</b>
                </v-alert>
              </div>

              <!--Make a drop down menu for all objects -->
              <div v-else-if="typeof(value) == 'object'">
                <v-expansion-panel focusable popout>
                  <v-expansion-panel-content>
                    <div slot="header">{{ key }}</div>
                    <div v-for="(value2, key2, index2) in value" :key="index2">

                      <!--Support nested objects till second degree-->
                      <div v-if="typeof(value2) == 'object'">
                        <v-expansion-panel focusable popout>
                          <v-expansion-panel-content>
                            <div slot="header">{{ key2 }}</div>
                            <div v-for="(value3, key3, index3) in value2" :key="index3">
                              <v-list-tile>
                                <v-list-tile-content>{{ key3 }}:</v-list-tile-content>
                                <v-list-tile-content class="align-end">{{ value3 }}</v-list-tile-content>
                              </v-list-tile>
                            </div>
                          </v-expansion-panel-content>
                        </v-expansion-panel>
                      </div>

                      <!--2. layer is no object-->
                      <div v-else>
                        <v-list-tile>
                          <v-list-tile-content>{{ key2 }}:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ value2 }}</v-list-tile-content>
                        </v-list-tile>
                      </div>
                    </div>

                  </v-expansion-panel-content>
                </v-expansion-panel>
              </div>

              <!--Default action for entries without further objects-->
              <div v-else>
                <v-list-tile>
                  <v-list-tile-content>{{ key }}:</v-list-tile-content>
                  <v-list-tile-content class="align-end">
                    {{ value }}
                  </v-list-tile-content>
                </v-list-tile>
              </div>
            </div>
          </v-list>
        </v-card>
      </v-flex>
      <v-toolbar
        slot="footer"
        class="mt-2"
        color="indigo"
        dark
        dense
        flat
      >
        <v-toolbar-title class="subheading">{{ subheader }}</v-toolbar-title>
      </v-toolbar>
    </v-data-iterator>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      rowsPerPageItems: [4, 8, 16],
      pagination: {
        rowsPerPage: 4
      }
    }
  },
  props: {
    items: {
      type: Array
    },
    title: {
      default: 'Some title'
    },
    subheader: {
      type: String,
      default: 'Some subheader'
    }
  }
}
</script>

<style scoped>

</style>
