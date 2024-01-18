<template>
    <div>
        <v-card>
            <v-card-title> </v-card-title>
            <v-data-table
                
                :items-per-page="5"
                :headers="headers"
                :items="reviews"
                class="elevation-1"
                sort-by="id"
            >
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
        headers:[{text: 'Id. Reseña', align: 'start', sortable: false, value: 'review_id'},
                 {text: 'Text', value: 'review_text'},
                 {text: 'Calificación', value: 'stars'}]
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
            api.get('/sentiments/dataset/' + this.datasetId).then((resp)=>{
                alert(resp.data)    
                this.reviews = resp.data
                })
        }
    }
}
</script>