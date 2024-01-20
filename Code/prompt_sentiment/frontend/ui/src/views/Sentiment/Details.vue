<template>
    <div>
        <v-toolbar>
        <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
        <v-toolbar-title>{{$formatMessage('details.title')}}</v-toolbar-title>
        </v-toolbar>   
        <StatsReview :dataset-id="this.dataset_id"></StatsReview>
    </div>
</template>

<script>
import StatsReview from '../../components/StatsReview.vue'

export default {
  data: () => ({
    dialog: false,
    dataset_id: 0,
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
    StatsReview
  },
  created() {
    this.initialize()
  },
  methods: {
    initialize(){
    this.dataset_id = this.$route.params['dataset_id'];
    }
  }
}
</script>