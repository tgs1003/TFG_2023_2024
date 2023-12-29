<template>
<div>
<p>Análisis de sentimientos.</p>
<v-alert v-if="errorMessage != ''"
      color="yellow"
      variant="outlined"
    >
      <template v-slot:title>
        Outlined Alert
      </template>
      {{ errorMessage }}
      </v-alert>
<v-stepper
    v-model="e6"
    vertical
  >
    <v-stepper-step
      :complete="e6 > 1"
      step="1"
    >
      Seleccione fichero de reseñas
      <small>Seleccione el fichero que contiene las reseñas que quiere analizar.</small>
    </v-stepper-step>

    <v-stepper-content step="1">
        <v-card
          class="mb-12"
          height="100px"
        >
        <v-row>
        <v-col><v-text-field
          v-model="datasetName"
          :error-messages="nameErrors"
          name="datasetName"
          label="Nombre"
          required>

          </v-text-field></v-col>
          <v-col>
            <v-file-input
            :error-messages="fileErrors"
            name="datasetFile"
            accept=".json,.txt,.csv"
            label="Fichero de reseñas de usuarios:" v-model="datasetFile">
          </v-file-input>
          </v-col>
        </v-row>
        </v-card>
      <v-btn
        color="primary"
        @click="submitFiles"
      >
        Continuar
      </v-btn>
      <v-btn text>
        Cancelar
      </v-btn>
    </v-stepper-content>

    <v-stepper-step
      :complete="e6 > 2"
      step="2"
    >
      Configuración del fichero
    </v-stepper-step>

    <v-stepper-content step="2">
      <v-card
        class="mb-12"
        height="200px"
      >
      <v-container v-if="file_info != null">
        <v-row>
          <v-col><span><strong>Nombre del fichero: </strong>{{ file_info.file_name }}</span></v-col>
          <v-col><span><strong>Número de reseñas: </strong>{{ file_info.row_count }} </span></v-col>
        </v-row>
        <v-row>
          <v-col><span><strong>Formato: </strong>{{ file_info.file_format }}</span></v-col><v-col></v-col>
        </v-row>
        <v-row>
          <v-col>
          <v-select 
                v-model="selectedColumn"
                v-show="file_info != null" 
                label="Campo que contiene las reseñas: "
                :items="file_info.header"
                >    
          </v-select>
        </v-col>
        <v-col></v-col>  
        </v-row>
      </v-container>
      </v-card>
      <v-btn
        color="primary"
        @click="processFile"
      >
        Procesar
      </v-btn>
      <v-btn text>
        Cancelar
      </v-btn>
    </v-stepper-content>
    <v-stepper-step step="3">
      Resultados
    </v-stepper-step>
    <v-stepper-content step="3">
      <v-card
        class="mb-12"
        height="200px"
      ></v-card>
      <v-btn
        color="primary"
        @click="e6 = 1"
      >
        Guardar informe
      </v-btn>
      <v-btn text>
        Cancelar
      </v-btn>
    </v-stepper-content>
  </v-stepper>
</div>
</template>

<script>
  import api from '../services/api'
  import { validationMixin } from 'vuelidate'
  import { required} from 'vuelidate/lib/validators'
  
  export default {
    name: "Inicio",
    mixins: [validationMixin],
    validations: {
    datasetName: {required},
    datasetFile: {required}
    },
    data () {
      return {
       
        datasetFile:null,
        e6: 1,
        file_info: null,
        selectedColumn: null,
        datasetName: null,
        datasetId: null,
        errorMessage: '',
        sample: 100
      }
    },
    computed:{
        nameErrors () {
            const errors = []
            if (!this.$v.datasetName.$dirty) return errors
            !this.$v.datasetName.required && errors.push('El nombre del dataset es obligatorio.')
            return errors
        },
        fileErrors(){
          const errors = []
            if (!this.$v.datasetFile.$dirty) return errors
            !this.$v.datasetFile.required && errors.push('Falta el fichero a analizar.')
            return errors
        },
    },
    methods:
    {
      processFile(){
        //Guardamos el dataset
        api.post("/datasets", {"name": this.datasetName, 
                              "type":this.file_info.file_format, 
                              "config": {"fileId": this.file_info.file_id,
                                         "reviewColumn": this.selectedColumn,
                                         "fileFormat": this.file_info.file_format,
                                         "separator": this.file_info.separator
                            }})
        .then(response => {
              this.datasetId = response.data["datasetId"]
              let datasetData = {
                    "sample": this.sample
                }
              api.put("/datasets/" + this.datasetId +"/load", datasetData)
              .then(response => {
                    if (response.status == 200)
                      api.put("/datasets/" + this.datasetId +"/process")
                      .then(response =>{
                        this.processResults = response.data
                        this.e6=3
                      })
                      .catch(error => {
                          console.log({ error });
                      });
                    else
                      console.log(response)
              })
              .catch(error => {
                    console.log({ error });
              });
        })
        .catch(error =>{
            console.log({ error });
        });
      },
      submitFiles() {
        this.errorMessage = ''
        this.$v.$touch()
        if (this.datasetFile) {
          
            let formData = new FormData();
            formData.append("file", this.datasetFile, this.datasetFile.name);
            api
                .post("/datasets/upload", formData)
                .then(response => {
                    this.file_info = response.data['file_info']
                    if (this.file_info.header.length == 1)
                      this.selectedColumn = this.file_info.header[0]
                    if (this.file_info.file_format != "unknown")
                    {
                      this.e6=2
                      console.log("Success!");
                      console.log({ response });
                    }
                    else
                    {
                      this.errorMessage = "El fichero tiene un formato desconocido"
                    }
                })
                .catch(error => {
                    this.errorMessage = error
                    console.log({ error });
                });
                
        } else {
            this.errorMessage = "No hay ficheros."
            console.log("there are no files.");
        }
      }
    }
  }
</script>

<style scoped>

</style>
