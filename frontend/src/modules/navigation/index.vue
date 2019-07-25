<template>
  <div>
  <!-- Navigation for smaller devices -->
  <!-- NavigationDrawer :navAreas="navAreas" :sideNavProp="sideNav"></NavigationDrawer -->
  <!-- Toolbar for medium/larger devices -->
  <Toolbar :navAreas="navAreas" ></Toolbar>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import Toolbar from './component/Toolbar'
// import NavigationDrawer from './component/NavigationDrawer'
export default {
  name: 'Navigation',
  components: {
    // NavigationDrawer,
    Toolbar
  },
  computed: {
    ...mapGetters({ navAreas: 'getNavAreas', sideNav: 'getSideNav' })
  }
}
</script>
