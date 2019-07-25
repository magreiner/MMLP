<template>
  <v-layout row pa-5 >
    <v-flex xs12 sm6 offset-sm3>
      <v-card class="block-example border border-dark">
        <v-toolbar color="indigo" dark>

          <v-toolbar-title>{{ header }}</v-toolbar-title>
        </v-toolbar>
        <v-list light
          header
          three-line
        >
          <v-subheader>Please select one of the following items:</v-subheader>
          <v-layout column wrap pl-4>

            <v-radio-group
              v-model="selection">
              <v-radio
                v-for="item in items"
                :key="item.name"
                :label="`${item.name}`"
                :value="item.name"
                :v-bind:value="item.name"
                v-on:input="$emit('input', item.name)"
                v-on:change="$emit('change', item.name)"
                light

                >

              </v-radio>
            </v-radio-group>
          </v-layout>
        </v-list>
        <v-footer class="pa-3" color="indigo">
          Selection: {{ selection }}
        </v-footer>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'dataRadioList',
  data () {
    return {
      selection: 'None selected'
    }
  },
  props: {
    items: {
      type: Array
    },
    header: {
      type: String,
      default: 'Some header'
    }
  }
}
</script>

<style scoped>

</style>
