<template>
    <div>
        <v-card>
            <v-card-title id="details_reviews_title">this.$formatMessage('details.reviews_title)</v-card-title>
            <v-data-table
                :items-per-page="5"
                :headers="headers"
                :items="reviews"
                class="elevation-1"
                sort-by="id"
            >
            <template v-slot:item.review_text="{ item }">
                <tr :title = "item.review_text"><td class="truncate" style="overflow:hidden;text-overflow:ellipsis;white-space: nowrap; max-width: 400px;">
                    {{ item.review_text }}
                </td></tr>
            </template>
            <template v-slot:item.stars="{ item }">
                <v-rating
                    :value="item.stars"
                    readonly
                >
                </v-rating>
            </template>
            </v-data-table>
        </v-card>
    </div>
</template>

<script>
import api from '../services/api'


export default {
    name: "Reviews",
    data: () => ({
        
        reviews: [],
        headers:[]
    }),
    components:{
        
    },
    props: {
      datasetId:
      {
        type: Number,
        default:1
      }
    },
    created() {
        this.initialize()
    },
    methods: {
        initialize(){
            this.headers.push({text: this.$formatMessage('details.id_review'), align: 'start', sortable: false, value: 'review_id'},
                 {text: this.$formatMessage('details.review_text'), value: 'review_text'},
                 {text: this.$formatMessage('details.rating'), value: 'stars'})
            api.get('/sentiments/dataset/' + this.datasetId).then((resp)=>{    
                this.reviews = resp.data
                })
        }
    }
}
</script>