<template>
    <div>   
        <Stats :datasetId="this.datasetId"></Stats>
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
              <Reviews :datasetId="this.datasetId"></Reviews>
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
import Stats from './Stats.vue'
import Reviews from './Reviews.vue'

export default {
  name: 'StatsReview',
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
  props: {
      datasetId:
      {
        type: Number,
        default:1
      }
    },
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