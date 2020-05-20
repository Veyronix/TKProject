<template>
  <v-list>
    <v-list-item
      v-for="(section, index) in sections"
      :key="index"
      :to="{path: section.path}"
    >
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
            title: 'Convert video',
          },
          {
            path: '/editor',
            title: 'Edit video',
          },
        ],
      }
    },
  }
</script>
