<template>
    <div>
        <v-data-table
                :headers="headers"
                :items="users"
                class="elevation-1"
                sort-by="email"
                :items-per-page="5"
                
        >
            <template v-slot:top>
                <v-toolbar color="white" flat>
                    <v-toolbar-title>Lista de usuarios</v-toolbar-title>
                    <v-divider
                            class="mx-4"
                            inset
                            vertical
                    ></v-divider>
                    <v-spacer></v-spacer>
                    <v-dialog max-width="500px" v-model="dialog">
                        <template v-slot:activator="{ on }">
                            <v-btn class="mb-2" color="primary" dark v-on="on">Crear usuario</v-btn>
                        </template>
                        <v-card>
                            <v-card-title>
                                <span class="headline">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text>
                                <v-container>
                                    <v-row>
                                        <v-col cols="12" md="12" sm="12">
                                            <v-text-field label="Username" v-model="editedItem.name"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="12" sm="12">
                                            <v-text-field label="Email" v-model="editedItem.email"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="12" sm="12" v-if="editedIndex === -1">
                                            <v-text-field type="password" label="Password" v-model="editedItem.password"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="12" sm="12">
                                            <v-select label="Rol" v-model="editedItem.rol" :items="roles"></v-select>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn @click="close" color="blue darken-1" text>Cancelar</v-btn>
                                <v-btn @click="save" color="blue darken-1" text>Guardar</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-icon
                        @click="editItem(item)"
                        small
                >
                    mdi-pencil
                </v-icon>
                <v-icon
                        @click="deleteItem(item)"
                        small
                >
                    mdi-delete
                </v-icon>
            </template>
            <template v-slot:no-data>
                <v-btn @click="initialize" color="primary">Reset</v-btn>
            </template>
        </v-data-table>
    
        <v-data-table
                    :items-per-page="5"
                    :headers="headers_datasets"
                    :items="datasets"
                    class="elevation-1"
                    sort-by="name"
                    
            >
                <template v-slot:top>
                    <v-toolbar color="white" flat>
                        <v-toolbar-title>Lista de datasets</v-toolbar-title>
                        <v-divider
                                class="mx-4"
                                inset
                                vertical
                        ></v-divider>
                        <v-spacer></v-spacer>
                        <v-dialog max-width="500px" v-model="dialog_dataset">
                            <template v-slot:activator="{ on }">
                                <v-btn class="mb-2" color="primary" dark v-on="on">Crear dataset</v-btn>
                            </template>
                            <v-card>
                                <v-card-title>
                                    <span class="headline">{{ formTitle_dataset }}</span>
                                </v-card-title>

                                <v-card-text>
                                    <v-container fluid>
                                        <v-row>
                                            <v-col cols="12" md="12" sm="12">
                                                <v-text-field label="Nombre" v-model="editedItem.name"></v-text-field>
                                            </v-col>
                                            <v-col cols="12" md="12" sm="12">
                                                <v-select label="Tipo" v-model="editedItem.type" :items="types"></v-select>
                                            </v-col>
                                            <v-col cols="12" md="12" sm="12">
                                                <v-textarea label="Configuración" v-model="editedItem.config"></v-textarea>
                                            </v-col>
                                        </v-row>
                                    </v-container>
                                </v-card-text>

                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn @click="close_dataset" color="blue darken-1" text>Cancelar</v-btn>
                                    <v-btn @click="save_dataset" color="blue darken-1" text>Guardar</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        <v-dialog max-width="800px" v-model="dialog_dataset_load">
                            <v-card>
                                <v-card-title>
                                    <span class="headline">Cargar dataset</span>
                                </v-card-title>

                                <v-card-text>
                                    <v-container>
                                        <v-row>
                                    
                                            <v-col cols="12" md="12" sm="12">
                                                
                                                <v-slider 
                                                    class="align-down"
                                                    label="Muestra a cargar (%):"
                                                    :step="10"
                                                    v-model="sample" 
                                                    :max="100" 
                                                    :min="10" 
                                                    hide-details
                                                    single-line
                                                    ticks
                                                    :tick-labels="percent"
                                                    >
                                                </v-slider>
                                            </v-col> 
                                        </v-row>
                                    </v-container>
                                </v-card-text>

                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn @click="close_dataset_load" color="blue darken-1" text>Cancelar</v-btn>
                                    <v-btn @click="load_dataset" color="blue darken-1" text>Cargar</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-toolbar>
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon title="Cargar dataset" v-if="item.total == '0' && item.status != 'Cargando'"
                            @click="loadDataset(item)"
                            class="mr-2"
                            small
                    >
                        mdi-upload
                    </v-icon>
                    <v-icon title="Procesar dataset" v-if="item.total != '0' && item.processed == '0'"
                            @click="processDataset(item)"
                            class="mr-2"
                            small
                    >
                        mdi-lightbulb-outline
                    </v-icon>
                    <v-icon title="Ver resultados" v-if="item.processed != '0'"
                            @click="viewResults(item)"
                            class="mr-2"
                            small
                    >
                        mdi-lightbulb-outline
                    </v-icon>
                    
                    <v-icon
                            @click="editDataset(item)"
                            small
                    >
                        mdi-pencil
                    </v-icon>
                    <v-icon
                            @click="deleteDataset(item)"
                            small
                    >
                        mdi-delete
                    </v-icon>
                    
                </template>
                <template v-slot:no-data>
                    <v-btn @click="initialize" color="primary">Reset</v-btn>
                </template>
            </v-data-table>
    </div>
    
</template>

<script>
    import axios from 'axios'
    import api from '../../services/api'
    export default {
        name: "UserList",
        data: () => ({
            dialog: false,
            dialog_dataset: false,
            dialog_dataset_load: false,
            percent: ["10","20","30","40","50","60","70","80","90","100"],
            roles:[
                "Admin",
                "Gestor"
            ],
            types:[
                "Hugging face"
            ],
            headers: [
                {
                    text: 'Nombre',
                    align: 'start',
                    sortable: false,
                    value: 'name',
                },
                {text: 'Correo', value: 'email'},
                {text: 'Rol', value: 'rol'},
                {text: 'Acciones', value: 'actions', sortable: false},
            ],
            headers_datasets: [
                {
                    text: 'Nombre',
                    align: 'start',
                    sortable: false,
                    value: 'name',
                },
                {text: 'Tipo', value: 'type'},
                {text: 'Reseñas totales', value: 'total'},
                {text: 'Reseñas procesadas', value: 'processed'},
                {text: 'Acciones', value: 'actions', sortable: false},
            ],
            users: [],
            datasets:[],
            sample:10,
            selectedDataset:{
                name: '',
                type: '',
                sample:''
                
            },
            editedIndex: -1,
            editedItem: {
                username: '',
                email: '',
                password:'',
                rol:''
            },
            defaultItem: {
                username: '',
                email: '',
                password:'',
                rol:''
            },
            
        }),

        computed: {
            formTitle_dataset() {
                return this.editedIndex === -1 ? 'Crear dataset' : 'Editar dataset'
            },
            formTitle() {
                return this.editedIndex === -1 ? 'Nuevo usuario' : 'Editar usuario'
            },
        },

        watch: {
            dialog_dataset_load(val) {
                val || this.close()
            },
            dialog_dataset(val) {
                val || this.close()
            },
            dialog(val) {
                val || this.close()
            },
        },

        created() {
            this.initialize()
            this.timer = setInterval(this.initialize, 10000);
        },
        beforeDestroy(){
            clearInterval(this.timer)
        },
        methods: {

            initialize() {
                api.get('/users').then((resp)=>{
                    this.users = resp.data
                })
                api.get('/datasets').then((resp)=>{
                    this.datasets = resp.data
                })
                
            },
            viewResults(item) {
                this.editedIndex = this.datasets.indexOf(item)
                this.editedItem = Object.assign({}, item)
            },

            editItem(item) {
                this.editedIndex = this.users.indexOf(item)
                this.editedItem = Object.assign({}, item)
                this.dialog = true
            },

            deleteItem(item) {
                var deletedIndex = this.users.indexOf(item)
                deletedIndex = Object.assign({}, item)
                confirm('¿Está seguro de que quiere borrar este usuario?') &&  
                api.delete('/users/' + deletedIndex.id)
                    .then(resp => {
                        console.log(resp.data.message)
                        this.initialize()
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            editDataset(item) {
                this.editedIndex = this.datasets.indexOf(item)
                this.editedItem = Object.assign({}, item)
                this.dialog_dataset = true
            },

            deleteDataset(item) {
                var deletedIndex = this.datasets.indexOf(item)
                deletedIndex = Object.assign({}, item)
                confirm('¿Está seguro de que quiere borrar este conjunto de datos?') &&  
                api.delete('/datasets/' + deletedIndex.id)
                    .then(resp => {
                        console.log(resp.data.message)
                        this.initialize()
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            close_dataset_load(){
                this.dialog_dataset_load = false
            },
            
            loadDataset(item) {
                this.selectedDataset = item
                this.dialog_dataset_load = true
            },
            load_dataset() {
                let datasetData = {
                    "sample": this.sample
                }
                api.put('/datasets/' + this.selectedDataset.id + '/load', datasetData)
                    .then(resp => {
                        console.log(resp.data.message)
                        this.initialize()
                    })
                    .catch(err => {
                        console.log(err)
                    })
                this.dialog_dataset_load = false
            },

            processDataset(item) {
                api.put('/datasets/' + item.id + '/process')
                    .then(resp => {
                        console.log(resp.data.message)
                        this.initialize()
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            close_dataset(){
                this.dialog_dataset = false
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem)
                    this.editedIndex = -1
                })

            },
            close() {
                this.dialog = false
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem)
                    this.editedIndex = -1
                })
            },
            save_dataset(){
                
                let datasetData = {
                    "name": this.editedItem.name,
                    "type": this.editedItem.type,
                    "payload": this.editedItem.payload
                }
                api.post('/datasets', datasetData) .then(resp => {
                            console.log(resp.data.message)
                            this.initialize()
                        })
                        .catch(err => {
                            console.log(err)
                        })
                this.close_dataset()
                }
            
                  
            ,
            save() {
                if (this.editedIndex > -1) {
                    let userData= {
                        "email": this.editedItem.email,
                        "name": this.editedItem.name,
                        "password":this.editedItem.password,
                        "rol":this.editedItem.rol
                    }
                    api.put('/users/' + this.editedItem.id, userData)
                    .then(resp => {
                            console.log(resp.data.message)
                            this.initialize()
                        })
                        .catch(err => {
                            console.log(err)
                        })
                    
                } else {
                    let userData= {
                        "email": this.editedItem.email,
                        "name": this.editedItem.name,
                        "password":this.editedItem.password,
                        "rol":this.editedItem.rol
                    }
                    axios({ url: process.env.VUE_APP_API_URL + '/users', data: userData, method: 'POST' })
                        .then(resp => {
                            console.log(resp.data.message)
                            this.initialize()
                        })
                        .catch(err => {
                            console.log(err)
                        })
                }
                this.close()
            },
        },
    }
</script>

<style scoped>

</style>
