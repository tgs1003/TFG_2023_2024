<template>
    <div>
    <v-card>
    <v-card-title>
        Análisis de reseñas
        <v-spacer></v-spacer>
        <v-select 
            @change="onChangeDataset($event)"
            label="Dataset: "
            :items="datasets"
            item-text="name"
            item-value="id"
            >    
        </v-select>
        <v-spacer></v-spacer>
        <v-select 
            @change="onChangeSearchBy($event)"
            label="Búsqueda por: "
            :items="searchby"
            item-text="name"
            item-value="id"
            >    
        </v-select>
        <v-spacer></v-spacer>
        <v-select 
            @change="onChangeUser($event)"
            v-show="selectedSearch==='Usuario'" 
            label="Usuario: "
            :items="users"
            item-text="name"
            item-value="id"
            >    
        </v-select>
        <v-select 
            @change="onChangeProduct($event)"
            v-show="selectedSearch==='Producto'"
            label="Producto: "
            :items="products"
            item-text="title"
            item-value="productId"
            >    
        </v-select>
    </v-card-title>
    <v-container fluid>
        <v-row dense>
        <v-col>
            <v-data-table
                :single-expand=true
                :expanded.sync="expanded"
                :items-per-page="5"
                :headers="headers_sentiments"
                :items="sentiments"
                class="elevation-1"
                sort-by="name"
                @click:row="rowClick"
                show-expand
            >
            <template v-slot:expanded-item="{headers, item}">
                    <td :colspan="headers.length">
                        <v-card>
                            <v-card-text>
                                <v-row align="center">
                                    <v-col
                                    cols="2"
                                    ><strong>Reseña:</strong></v-col>
                                    <v-col cols="10">
                                        {{item.reviewText}}
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                        
                    </td>
            </template>
            </v-data-table>
        </v-col>
        <v-col cols="3">
            <v-card class="mx-auto" max-width="300">
                <v-list-item two-line>
                    <v-list-item-content>
                        <v-list-item-title class="text-h5">
                            Resumen del proceso
                        </v-list-item-title>
                        <v-list-item-subtitle></v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                <v-card-text>
                    <v-row align="center">
                        <v-col
                        cols="4"
                        ><strong>API:</strong></v-col>
                        <v-col cols="8">
                            OpenAI
                        </v-col>
                    </v-row>
                    <v-row align="center">
                        <v-col
                        cols="4"
                        ><strong>Modelo:</strong></v-col>
                        <v-col cols="8">
                            ChatGpt 3.5 Turbo
                        </v-col>
                    </v-row>
                    <v-row align="center">
                        <v-col
                        cols="4"
                        ><strong>Fecha:</strong></v-col>
                        <v-col cols="8">
                            18 dic. 2023
                        </v-col>
                    </v-row>
                    <v-row align="center">
                        <v-col
                        cols="4"
                        ><strong>Tiempo:</strong></v-col>
                        <v-col cols="8">
                            20 minutos
                        </v-col>
                    </v-row>
                    <v-row align="center">
                        <v-col
                        cols="4"
                        ><strong>Coste:</strong></v-col>
                        <v-col cols="8">
                            ??
                        </v-col>
                    </v-row>
                    <v-row align="center" v-if="datasetInfo != null">
                        <v-col
                        cols="4"
                        ><strong>Dataset:</strong></v-col>
                        <v-col cols="8">
                            {{ datasetInfo.name }}
                        </v-col>
                    </v-row>
                    <v-row align="center" v-show="datasetInfo != null">
                        <v-col
                        cols="4"
                        ><strong>Origen:</strong></v-col>
                        <v-col cols="8">
                            {{ datasetInfo != null? datasetInfo.type:"" }}
                        </v-col>
                    </v-row>
                </v-card-text>
                

                <v-divider></v-divider>

                <v-card-actions>
                <v-btn text>
                    Ver Modelo
                </v-btn>
                <v-btn text>
                    Ver Dataset
                </v-btn>
                </v-card-actions>
            </v-card>
            
        </v-col>
    </v-row>
    
    </v-container>
    </v-card>
        
</div>
    
</template>

<script>
    import api from '../../services/api'
    export default {
        name: "SentimentList",
        data: () => ({
            expanded:[],
            currentTab:0,
            selectedItem:null,
            selectedDataset:null,
            selectedUser:null,
            selectedProduct:null,
            selectedReview:null,
            selectedSearch:null,
            datasetInfo: null,
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
            rowClick(item){
                api.get('reviews/' +item.id).then((resp)=>{
                        this.selectedReview = resp.data
                    });
            },
            onChangeSearchBy(event){
                //borramos reseñas
                //reseteamos variables
                this.selectedSearch=event;
                if(this.selectedDataset != null)
                    this.updateData();
            },
            onChangeDataset(event){
                this.selectedDataset=event;
                api.get('datasets/' +this.selectedDataset).then((resp)=>{
                        this.datasetInfo = resp.data
                    });
                if(this.selectedSearch != null)
                    this.updateData();
            },
            updateData(){
                //leer usuarios y productos
                if (this.selectedSearch === 'Producto')
                    api.get('products/sentiment/' +this.selectedDataset).then((resp)=>{
                        this.products = resp.data
                    });
                if (this.selectedSearch === 'Usuario')
                    api.get('review_users/sentiment/' +this.selectedDataset).then((resp)=>{
                        this.users = resp.data
                    });
            },
            onChangeUser(event){
                //actualizamos sentiments
                this.selectedUser = event;
                api.get('/sentiments/by_user_and_dataset/' + this.selectedUser + '/'+this.selectedDataset).then((resp)=>{
                    this.sentiments = resp.data
                })
            },
            onChangeProduct(event){
                //actualizamos sentiments
                this.selectedProduct=event;
                api.get('/sentiments/by_product_and_dataset/' + this.selectedProduct+'/'+this.selectedDataset).then((resp)=>{
                    this.sentiments = resp.data
                })
            },
            selectItem(selectedUser){
                //Devuelve las reseñas de un usuario procesadas y correctas.
                api.get('/sentiments/by_user/' + selectedUser.id).then((resp)=>{
                    this.sentiments = resp.data
                })
                
            },
            initialize() {
                
                api.get('/datasets').then((resp)=>{
                    this.datasets = resp.data
                })
            },            
        },
    }
</script>

<style scoped>

</style>
