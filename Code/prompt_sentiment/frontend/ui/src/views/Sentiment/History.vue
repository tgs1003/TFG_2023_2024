<template>
  <div>
      <v-toolbar>
        <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
        <v-toolbar-title>{{$formatMessage('home.history.title')}}</v-toolbar-title>
      </v-toolbar>
      <v-carousel v-model="dataset"  height="600">
        <v-carousel-item
          v-for="(dataset) in datasets"
          :key="dataset.id"
        >
          <Stats :datasetId="dataset.id"></Stats>
        </v-carousel-item>
    </v-carousel>
  </div>
    
</template>

<script>
import Stats from '../../components/Stats.vue'
import api from '../../services/api'

export default {
  data: () => ({
    dataset: 0,
    datasets: [
      
    ],
  }),
  components:{
    Stats,
  },
  created() {
    this.initialize()
  },
  methods: {
    initialize(){
    api.get('/datasets/user').then((resp)=>{
                  this.datasets = resp.data
              })
    }
  }
}
</script>