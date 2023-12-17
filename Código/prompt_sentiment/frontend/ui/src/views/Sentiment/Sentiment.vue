<template>
    <div>
        <div>    
            
        </div>
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
                    :items-per-page="5"
                    :headers="headers_sentiments"
                    :items="sentiments"
                    class="elevation-1"
                    sort-by="name"
                    @click:row="rowClick"
                >
                
                </v-data-table>
                <v-card v-if="selectedReview != null">
                    {{selectedReview.reviewText}}
                </v-card>
            </v-col>
            <v-col cols="3">
                <v-card class="mx-auto" max-width="300">
                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title class="text-h5">
                                San Francisco
                            </v-list-item-title>
                            <v-list-item-subtitle>Mon, 12:30 PM, Mostly sunny</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                    <v-card-text>
                        <v-row align="center">
                            <v-col
                            class="text-h2"
                            cols="6"
                            >23&deg;C</v-col>
                            <v-col cols="6">
                                <v-img
                                    src="https://cdn.vuetifyjs.com/images/cards/sun.png"
                                    alt="Sunny image"
                                    width="92"
                                ></v-img>
                            </v-col>
                        </v-row>
                    </v-card-text>
                    <v-list-item>
                    <v-list-item-icon>
                        <v-icon>mdi-send</v-icon>
                    </v-list-item-icon>
                    <v-list-item-subtitle>23 km/h</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                    <v-list-item-icon>
                        <v-icon>mdi-cloud-download</v-icon>
                    </v-list-item-icon>
                    <v-list-item-subtitle>48%</v-list-item-subtitle>
                    </v-list-item>

                    <v-slider
                    v-model="currentTab"
                    :max="6"
                    :tick-labels="datasets"
                    class="mx-4"
                    ticks
                    ></v-slider>

                    <v-list class="transparent">
                    <v-list-item
                        v-for="item in datasets"
                        :key="item.day"
                    >
                        <v-list-item-title>{{ item.day }}</v-list-item-title>

                        <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-icon>

                        <v-list-item-subtitle class="text-right">
                        {{ item.temp }}
                        </v-list-item-subtitle>
                    </v-list-item>
                    </v-list>

                    <v-divider></v-divider>

                    <v-card-actions>
                    <v-btn text>
                        Full Report
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
            currentTab:0,
            selectedItem:null,
            selectedDataset:null,
            selectedUser:null,
            selectedProduct:null,
            selectedReview:null,
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
