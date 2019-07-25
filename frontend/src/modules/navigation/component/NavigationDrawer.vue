<template>
  <v-navigation-drawer :navAreas="navAreas" v-model="sideNavModel" temporary app>
    <v-list dense>
      <v-list-tile
        v-for="area in navAreas"
        :key="area.title"
        :to="area.link"
      >
        <v-list-tile-action>
          <v-icon>{{ area.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ area.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>

    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'NavigationDrawer',
  data () {
    return {
      sideNavModel: false
    }
  },
  watch: {
    sideNavModel: function (value) {
      this.$store.commit('$nav/setSideNav', value)
    },
    sideNavProp: function (value) {
      this.sideNavModel = value
    }
  },
  props: {
    navAreas: {
      type: Array
    },
    authenticated: {
      type: Boolean
    },
    sideNavProp: {
      type: Boolean
    }
  },
  computed: {
    ...mapGetters({ sideNav: '$nav/getSideNav' })
  }
}
</script>
