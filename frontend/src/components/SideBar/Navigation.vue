<template>
  <v-list>
    <v-list-item
      v-for="(section, index) in sections"
      :key="index"
      :to="{path: section.path}"
    >
      <!--      <v-list-item-action>-->
      <!--        <v-icon>{{ section.icon }}</v-icon>-->
      <!--      </v-list-item-action>-->
      <v-list-item-title>{{ section.title }}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script>
  export default {
    name: 'Navigation',
    data () {
      return {
        sections: [
          {
            path: '/',
            // icon: 'dashboard',
            title: 'Convert video',
          },
          {
            path: '/editor',
            // icon: 'dashboard',
            title: 'Edit video',
          },
        ],
      }
    },
  }
</script>
