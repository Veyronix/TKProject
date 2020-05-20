<template>
  <v-app>
    <side-bar />
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
  import SideBar from './components/SideBar'

  export default {
    name: 'App',
    components: { SideBar },
    data () {
      return {

      }
    },
  }
</script>
