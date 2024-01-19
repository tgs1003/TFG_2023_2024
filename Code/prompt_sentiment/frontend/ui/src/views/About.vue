<template>
    <div>
    <v-toolbar>
        <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
        <v-toolbar-title>{{$formatMessage('about.title')}}</v-toolbar-title>
      </v-toolbar>
    </div>
  </template>
  
  <script>
  export default {
  data: () => ({
   
  }),
  methods:{
    history(){
      this.$router.push('/history')
    },
    analysis(){
      this.$router.push('/analysis')
    },
  }
  }
  </script>