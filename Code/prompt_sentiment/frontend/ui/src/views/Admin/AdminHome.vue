<template>
    <div>
        <v-toolbar>
            <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
            <v-toolbar-title>{{$formatMessage('admin.title')}}</v-toolbar-title>
        </v-toolbar>
        <v-data-table
                :headers="headers"
                :items="users"
                class="elevation-1"
                sort-by="email"
                :items-per-page="5"
                
        >
            <template v-slot:top>
                <v-toolbar color="white" flat>
                    <v-toolbar-title>{{ $formatMessage('admin.users.list') }}</v-toolbar-title>
                    <v-divider
                            class="mx-4"
                            inset
                            vertical
                    ></v-divider>
                    <v-spacer></v-spacer>
                    <v-dialog max-width="500px" v-model="dialog">
                        <template v-slot:activator="{ on }">
                            <v-btn class="mb-2" color="primary" dark v-on="on">{{$formatMessage('admin.users.create')}}</v-btn>
                        </template>
                        <v-card>
                            <v-card-title>
                                <span class="headline">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text>
                                <v-container>
                                    <v-row>
                                        <v-col cols="12" md="12" sm="12">
                                            <v-text-field 
                                                id="admin_users_username" 
                                                :label="$formatMessage('admin.users.username')" 
                                                autocomplete="off"
                                                name="name"
                                                value="" 
                                                v-model="name"
                                                required
                                                :error-messages="nameErrors"
                                                >
                                            </v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="12" sm="12">
                                            <v-text-field 
                                            id="admin_users_email"
                                            autocomplete="off" 
                                            name="email"
                                            value=""
                                            required
                                            :error-messages="emailErrors"
                                            :label="$formatMessage('admin.users.email')" 
                                            v-model="email"
                                            ></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="12" sm="12" 
                                            v-if="editedIndex === -1">
                                            <v-text-field 
                                            id="admin.users.password"
                                            type="password" 
                                            autocomplete="off"
                                            name="pass"
                                            required
                                            value=""
                                            :error-messages="passwordErrors"
                                            :label="$formatMessage('admin.users.password')" 
                                            v-model="password"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="12" sm="12">
                                            <v-select
                                            id="admin_users_rol"  
                                            :label="$formatMessage('admin.users.rol')" 
                                            :error-messages="rolErrors"
                                            v-model="rol" 
                                            value=""
                                            required 
                                            :items="roles"
                                            ></v-select>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn @click="close" color="blue darken-1" text>{{ $formatMessage('admin.users.cancel') }}</v-btn>
                                <v-btn @click="save" color="blue darken-1" text>{{ $formatMessage('admin.users.save') }}</v-btn>
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
                <v-btn @click="initialize" color="primary">{{ $formatMessage('admin.users.reset') }}</v-btn>
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
                        <v-toolbar-title>{{ $formatMessage('admin.datasets.list') }}</v-toolbar-title>
                        <v-divider
                                class="mx-4"
                                inset
                                vertical
                        ></v-divider>
                        <v-spacer></v-spacer>
                        <v-dialog max-width="500px" v-model="dialog_dataset">
                            <template v-slot:activator="{ on }">
                                <v-btn class="mb-2" color="primary" dark v-on="on">{{$formatMessage('admin.datasets.create')}}</v-btn>
                            </template>
                            <v-card>
                                <v-card-title>
                                    <span class="headline">{{ formTitle_dataset }}</span>
                                </v-card-title>

                                <v-card-text>
                                    <v-container fluid>
                                        <v-row>
                                            <v-col cols="12" md="12" sm="12">
                                                <v-text-field 
                                                id="admin_datasets_name" 
                                                :label="$formatMessage('admin.datasets.name')" 
                                                v-model="dataset_name"
                                                :error-messages="datasetNameErrors"
                                                required
                                                ></v-text-field>
                                            </v-col>
                                            <v-col cols="12" md="12" sm="12">
                                                <v-select 
                                                id="admin_datasets_type" 
                                                :label="$formatMessage('admin.datasets.type')" 
                                                v-model="dataset_type" :items="types"
                                                :error-messages="datasetTypeErrors" 
                                                required
                                                ></v-select>
                                            </v-col>
                                            <v-col cols="12" md="12" sm="12">
                                                <v-textarea 
                                                id="admin_datasets_configuration" 
                                                :label="$formatMessage('admin.datasets.configuration')" 
                                                :error-messages="datasetConfigErrors" 
                                                v-model="dataset_config"
                                                required
                                                ></v-textarea>
                                            </v-col>
                                        </v-row>
                                    </v-container>
                                </v-card-text>

                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn @click="close_dataset" color="blue darken-1" text>{{ $formatMessage('admin.users.cancel') }}</v-btn>
                                    <v-btn @click="save_dataset" color="blue darken-1" text>{{ $formatMessage('admin.users.save') }}</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        <v-dialog max-width="800px" v-model="dialog_dataset_load">
                            <v-card>
                                <v-card-title>
                                    <span class="headline">{{ $formatMessage('admin.datasets.load.title') }}</span>
                                </v-card-title>

                                <v-card-text>
                                    <v-container>
                                        <v-row>
                                    
                                            <v-col cols="12" md="12" sm="12">
                                                
                                                <v-slider 
                                                    class="align-down"
                                                    :label="$formatMessage('admin.datasets.sample')"
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
                                    <v-btn @click="close_dataset_load" color="blue darken-1" text>{{ $formatMessage('admin.users.cancel') }}</v-btn>
                                    <v-btn @click="load_dataset" color="blue darken-1" text>{{ $formatMessage('admin.datasets.load.btn') }}</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-toolbar>
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon :title="$formatMessage('admin.datasets.load.title')" v-if="item.total == '0' && item.status != 'Cargando'"
                            @click="loadDataset(item)"
                            class="mr-2"
                            small
                    >
                        mdi-upload
                    </v-icon>
                    <v-icon :title="$formatMessage('admin.datasets.process')" v-if="item.total != '0' && item.processed == '0'"
                            @click="processDataset(item)"
                            class="mr-2"
                            small
                    >
                        mdi-lightbulb-outline
                    </v-icon>
                    <v-icon :title="$formatMessage('admin.datasets.viewresults')" v-if="item.processed != '0'"
                            @click="viewResults(item)"
                            class="mr-2"
                            small
                    >
                        mdi-chart-line
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
                    <v-btn @click="initialize" color="primary">{{ $formatMessage('admin.users.reset') }}</v-btn>
                </template>
            </v-data-table>
    </div>
    
</template>

<script>
    import api from '../../services/api';
    import { validationMixin } from 'vuelidate';
    import { required, email, minLength} from 'vuelidate/lib/validators';
    export default {
        mixins: [validationMixin],
        validations: {
        name: {required},
        email: { required, email },
        rol: { required },
        password: { required, minLength: minLength(6), },
        dataset_name: {required},
        dataset_type: {required},
        dataset_config: {required}
        },
        name: "UserList",
        data: () => ({
            email: "",
            password: "",
            name: "",
            rol: "",
            user_id: "",
            dataset_id: "",
            dataset_name: "",
            dataset_type: "",
            dataset_config: "",
            fieldTypes: { // add this for change input type
                name:"text",
                email:"text",
                password: "text",
                rol:"text",
                dataset_name: "text",
                dataset_type: "text",
                dataset_config: "text",
            },
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
            headers: [],
            headers_datasets: [],
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
            emailErrors () {
                const errors = [];
                if (!this.$v.email.$dirty) return errors;
                !this.$v.email.email && errors.push(this.$formatMessage("register.error.email.invalid"));
                !this.$v.email.required && errors.push(this.$formatMessage("register.error.email.required"));
                return errors;
            },
            nameErrors(){
                const errors = [];
                if (!this.$v.name.$dirty) return errors;
                !this.$v.name.required && errors.push(this.$formatMessage("register.error.name.required"));
                return errors;
            },
            passwordErrors(){
                const errors = []
                if (!this.$v.password.$dirty) return errors
                !this.$v.password.required && errors.push(this.$formatMessage("register.error.password.required"))
                return errors
            
            },
            rolErrors(){
                const errors = []
                if (!this.$v.rol.$dirty) return errors
                !this.$v.rol.required && errors.push(this.$formatMessage("admin.users.rol.required"))
                return errors
            
            },
            datasetNameErrors(){
                const errors = []
                if (!this.$v.dataset_name.$dirty) return errors
                !this.$v.dataset_name.required && errors.push(this.$formatMessage("admin.datasets.name.required"))
                return errors
            
            },
            datasetTypeErrors(){
                const errors = []
                if (!this.$v.dataset_type.$dirty) return errors
                !this.$v.dataset_type.required && errors.push(this.$formatMessage("admin.dataset.type.required"))
                return errors
            
            },
            datasetConfigErrors(){
                const errors = []
                if (!this.$v.dataset_config.$dirty) return errors
                !this.$v.dataset_config.required && errors.push(this.$formatMessage("admin.datasets.configuration.required"))
                return errors
            
            },
            formTitle_dataset() {
                return this.editedIndex === -1 ? this.$formatMessage("admin.datasets.create") : this.$formatMessage("admin.datasets.edit") 
            },
            formTitle() {
                return this.editedIndex === -1 ? this.$formatMessage("admin.users.new") : this.$formatMessage("admin.users.edit") 
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
            this.headers.push({
                    text: this.$formatMessage("admin.users.name"),
                    align: "start",
                    sortable: false,
                    value: "name",
                },
                {text: this.$formatMessage("admin.users.email"), value: "email"},
                {text: this.$formatMessage("admin.users.rol"), value: "rol"},
                {text: this.$formatMessage("admin.users.actions"), value: "actions", sortable: false});
                this.headers_datasets.push(
                {
                    text: this.$formatMessage("admin.datasets.name"),
                    align: "start",
                    sortable: false,
                    value: "name",
                },
                {text: this.$formatMessage("admin.datasets.type"), value: "type"},
                {text: this.$formatMessage("admin.datasets.total_reviews"), value: "total"},
                {text: this.$formatMessage("admin.datasets.total_processed"), value: "processed"},
                {text: this.$formatMessage("admin.users.actions"), value: "actions", sortable: false});
            
            this.initialize()
            this.timer = setInterval(this.initialize, 10000);
        },
        beforeDestroy(){
            clearInterval(this.timer)
        },
        methods: {
            initialize() {
                
                api.get("/users").then((resp)=>{
                    this.users = resp.data
                })
                api.get("/datasets").then((resp)=>{
                    this.datasets = resp.data
                })
                
            },
            viewResults(item) {
                this.$router.push({name: "Details", params:{dataset_id: item.id}})
            },
            editItem(item) {
                this.editedIndex = this.users.indexOf(item)
                this.user_id = item.id;
                this.name = item.name;
                this.email = item.email;
                this.password = "dummypasswordavoidsvalidation";
                this.rol = item.rol;
                this.dialog = true
            },

            deleteItem(item) {
                confirm(this.$formatMessage("admin.users.confirm.delete")) &&  
                api.delete("/users/" + item.id)
                    .then(resp => {
                        console.log(resp.data.message)
                        this.initialize()
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            editDataset(item) {
                this.dataset_id = item.id;
                this.dataset_name = item.name;
                this.dataset_type = item.type;
                this.dataset_config = item.config;
                this.editedIndex = this.datasets.indexOf(item)
                this.editedItem = Object.assign({}, item)
                this.dialog_dataset = true
            },

            deleteDataset(item) {
                var deletedIndex = this.datasets.indexOf(item)
                deletedIndex = Object.assign({}, item)
                confirm(this.$formatMessage("admin.datasets.confirm.delete")) &&  
                api.delete("/datasets/" + deletedIndex.id)
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
                api.put("/datasets/" + this.selectedDataset.id + "/load", datasetData)
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
                api.put("/datasets/" + item.id + "/process")
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
                    this.rol="";
                    this.name="";
                    this.email="";
                    this.password="";
                    this.editedItem = Object.assign({}, this.defaultItem)
                    this.editedIndex = -1
                })
            },
            save_dataset(){
                this.$v.dataset_name.$touch();
                this.$v.dataset_type.$touch();
                this.$v.dataset_config.$touch();
                if (this.$v.dataset_name.$invalid || 
                    this.$v.dataset_type.$invalid || 
                    this.$v.dataset_config.$invalid)
                    return;
                let datasetData = {
                    "name": this.dataset_name,
                    "type": this.dataset_type,
                    "config": this.dataset_config
                }
                api.post("/datasets", datasetData) .then(resp => {
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
                this.$v.name.$touch();
                this.$v.email.$touch();
                this.$v.rol.$touch();
                if (this.$v.name.$invalid || this.$v.email.$invalid || this.$v.rol.$invalid)
                    return;
                if (this.editedIndex > -1) {
                    let userData= {
                        "email": this.email,
                        "name": this.name,
                        "rol":this.rol
                    }
                    api.put("/users/" + this.user_id, userData)
                    .then(resp => {
                            console.log(resp.data.message)
                            this.initialize()
                        })
                        .catch(err => {
                            console.log(err)
                        })
                    
                } else {
                    this.$v.password.$touch();
                    if (this.$v.password.$invalid)
                        return;
                    let userData= {
                        "email": this.email,
                        "name": this.name,
                        "password":this.password,
                        "rol":this.rol
                    }
                    api.post("/users", userData)
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
