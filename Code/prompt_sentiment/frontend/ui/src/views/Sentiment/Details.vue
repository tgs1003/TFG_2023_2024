<template>
    <div>
        <v-toolbar>
        <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
        <v-toolbar-title>{{$formatMessage('details.title')}}</v-toolbar-title>
        </v-toolbar>   
        <Stats :datasetId="this.dataset"></Stats>
        <div class="text-center">
        <v-dialog
          v-model="dialog"
          width="800"
          >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              dark
              v-bind="attrs"
              v-on="on"
            >
            {{ $formatMessage('details.view_reviews') }}
            </v-btn>
            
          </template>

          <v-card>
            <v-card-title class="text-h5 grey lighten-2">
              {{ $formatMessage('details.reviews_title') }}
            </v-card-title>
            <v-card-text>
              <Reviews :datasetId="this.dataset"></Reviews>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                text
                @click="dialog = false"
              >
              {{ $formatMessage('details.reviews.close') }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
        
    </div>
</template>

<script>
import Stats from '../../components/Stats.vue'
import Reviews from '../../components/Reviews.vue'


export default {
  data: () => ({
    dialog: false,
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