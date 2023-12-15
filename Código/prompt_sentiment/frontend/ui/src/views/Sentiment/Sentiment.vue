<template>
    <div>
       
        <div>    
            
        </div>
        <v-card>
        <v-card-title>
            Reseñas
            <v-spacer></v-spacer>
            <v-select 
                v-model="selectedDataset" 
                label="Dataset: "
                :items="datasets"
                item-text="name"
                item-value="id"
                >    
            </v-select>
            <v-spacer></v-spacer>
            <v-select 
                @change="onChange($event)"
                v-model="selectedSearch" 
                label="Búsqueda por: "
                :items="searchby"
                item-text="name"
                item-value="id"
                >    
            </v-select>
            <v-spacer></v-spacer>
            <v-select 
                @change="onChange($event)"
                v-show="selectedSearch==='Usuario'"
                v-model="selectedUser" 
                label="Usuario: "
                :items="users"
                item-text="name"
                item-value="id"
                >    
            </v-select>
            <v-select 
                @change="onChange($event)"
                v-show="selectedSearch==='Producto'"
                v-model="selectedProduct" 
                label="Producto: "
                :items="products"
                item-text="name"
                item-value="id"
                >    
            </v-select>
        </v-card-title>
            <v-data-table
                :items-per-page="5"
                :headers="headers_sentiments"
                :items="sentiments"
                class="elevation-1"
                sort-by="name"
            >
        </v-data-table>
    </v-card>
    </div>
    
</template>

<script>
    import api from '../../services/api'
    export default {
        name: "SentimentList",
        data: () => ({
            currentTab:0,
            selectedItem:null,
            selectedDataset:null,
            selectedUser:null,
            selectedProduct:null,
            selectedSearch:null,
            dialog: false,
            datasets:[],
            users:[],
            products:[],
            sentiments:[],
            searchby:["Usuario", "Producto", "Texto"],
            headers_sentiments:[{
                    text: 'Id. Reseña',
                    align: 'start',
                    sortable: false,
                    value: 'id',
                },
                {text: 'Id. Producto', value: 'productId'},
                {text: 'Puntuación', value: 'originalStars'},
                {text: 'Estimación', value: 'stars'},
                {text: 'Modelo', value: 'model'},
                {text: 'Tiempo de proceso', value: 'processTime'},
                {text: 'Acciones', value: 'actions', sortable: false}]
            
        }),
        created() {
            this.initialize()
        },

        methods: {
            onChange(event){

            },
            selectItem(selectedUser){
                //Devuelve las reseñas de un usuario procesadas y correctas.
                api.get('/sentiments/by_user/' + selectedUser.id).then((resp)=>{
                    this.sentiments = resp.data
                })
                
            },
            initialize() {
                api.get('/review_users/sentiment').then((resp)=>{
                    this.users = resp.data
                })
                api.get('/datasets').then((resp)=>{
                    this.datasets = resp.data
                })
            },            
        },
    }
</script>

<style scoped>

</style>
