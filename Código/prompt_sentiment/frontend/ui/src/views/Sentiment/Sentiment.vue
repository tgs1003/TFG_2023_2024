<template>
    <div>
        <div>    
            
        </div>
        <v-card>
        <v-card-title>
            Reseñas
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
