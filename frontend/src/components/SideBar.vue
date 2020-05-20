<template>
  <v-navigation-drawer
    app
    clipped
    permanent
    :mini-variant="mini"
  >
    <v-list>
      <v-list-item-title class="title text-uppercase">
        <span>Cool video</span>
      </v-list-item-title>
    </v-list>

    <navigation />
  </v-navigation-drawer>
</template>

<script>
  import Navigation from './SideBar/Navigation'

  export default {
    name: 'SideBar',
    components: { Navigation },
    data: function () {
      return {
        mini: false,
      }
    },
  }
</script>
