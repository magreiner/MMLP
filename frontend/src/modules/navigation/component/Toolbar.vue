<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-toolbar :navAreas="navAreas" dark class="primary">

    <!-- v-toolbar-side-icon @click.stop="onNavClick" class="hidden-sm-and-up"/ -->

    <v-toolbar-title>
      <router-link to="/" tag="span" style="cursor: pointer">
        <v-icon left dark>home</v-icon>
        Medical Machine Learning Platform
      </router-link>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items class="hidden-xs-only">
      <v-btn
        flat
        v-for="area in navAreas"
        :key="area.title"
        :to="area.link"
      >
        <v-icon left dark>{{ area.icon }}</v-icon>
        {{ area.title }}
      </v-btn>
    </v-toolbar-items>

    <v-spacer/>

    <v-menu bottom left>
      <template v-slot:activator="{ on }">
        <v-btn
          dark
          icon
          v-on="on"
        >
          <v-icon v-if="mode==='app'" dark>assignment_ind</v-icon>
          <v-icon v-else dark>assignment</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-tile @click="setMode('app')">
          <v-icon>person_outline</v-icon>
          <v-list-tile-title>Medical Expert</v-list-tile-title>
        </v-list-tile>
        <v-list-tile @click="setMode('lab')">
          <v-icon>person</v-icon>
          <v-list-tile-title>Clinical Data Scientist</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>

  </v-toolbar>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Toolbar',
  props: {
    navAreas: {
      type: Array
    }
  },
  computed: {
    // ...mapGetters({ sideNav: 'getSideNav', mode: 'getMode' })
    ...mapGetters({ mode: 'getMode' })
  },
  methods: {
    // onNavClick () {
    //   let sideNav = !this.sideNav
    //   this.$store.commit('$nav/setSideNav', sideNav)
    // },
    setMode (mode) {
      this.$store.commit('setMode', mode)
      this.$router.push('/')
    }
  }
}
</script>
