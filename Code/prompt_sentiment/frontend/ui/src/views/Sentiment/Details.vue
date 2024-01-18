<template>
    <div>
        <v-toolbar>
        <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
        <v-toolbar-title>{{$formatMessage('navbar.menu.home')}}</v-toolbar-title>
        </v-toolbar>   
        <Stats :datasetId="this.dataset"></Stats>
        <Reviews :datasetId="this.dataset"></Reviews>
    </div>
</template>

<script>
import Stats from '../../components/Stats.vue'
import Reviews from '../../components/Reviews.vue'


export default {
  data: () => ({
    dataset: 0,
    datasets: [
      
    ],
    items: [
    {
        title: 'Inicio',
        disabled: false,
        href:'Home'
    },

    ],
  }),
  components:{
    Stats,
    Reviews
  },
  created() {
    this.initialize()
  },
  methods: {
    initialize(){
    this.dataset = this.$route.params['dataset_id'];
    }
  }
}
</script>