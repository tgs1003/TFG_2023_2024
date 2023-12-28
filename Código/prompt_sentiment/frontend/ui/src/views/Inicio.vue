<template>
<div>
<p>Análisis de sentimientos.</p>
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
          <v-file-input
            accept=".json,.txt,.csv"
            label="Fichero de reseñas de usuarios:" v-model="file">
          </v-file-input>
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
          <span><strong>Nombre del fichero: </strong>{{ file_info.file_name }}</span>
        </v-row>
        <v-row>
          <span><strong>Formato: </strong>{{ file_info.file_format }}</span>
        </v-row>
        <v-row>
          <v-select 
                v-model="selectedColumn"
                v-show="file_info != null" 
                label="Campo que contiene las reseñas: "
                :items="file_info.header"
                >    
          </v-select>
        </v-row>
      </v-container>
      </v-card>
      <v-btn
        color="primary"
        @click="e6 = 3"
      >
        Continuar
      </v-btn>
      <v-btn text>
        Cancelar
      </v-btn>
    </v-stepper-content>

    <v-stepper-step
      :complete="e6 > 3"
      step="3"
    >
      Confirmación
    </v-stepper-step>

    <v-stepper-content step="3">
      <v-card
        color="grey lighten-1"
        class="mb-12"
        height="200px"
      ></v-card>
      <v-btn
        color="primary"
        @click="e6 = 4"
      >
        Confirmar
      </v-btn>
      <v-btn text>
        Cancelar
      </v-btn>
    </v-stepper-content>

    <v-stepper-step step="4">
      Resultados
    </v-stepper-step>
    <v-stepper-content step="4">
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
  export default {
    name: "Inicio",
    data () {
      return {
        file:null,
        e6: 1,
        file_info: null,
        selectedColumn: null
      }
    },
    methods:
    {
      submitFiles() {
        
        if (this.file) {
          
            let formData = new FormData();
            formData.append("file", this.file, this.file.name);
            api
                .post("/datasets/upload", formData)
                .then(response => {
                    this.file_info = response.data['file_info']
                    if (this.file_info.header.length == 1)
                      this.selectedColumn = this.file_info.header[0]
                    if (this.file_info.file_format != "unknown")
                      this.e6=2
                    console.log("Success!");
                    console.log({ response });
                })
                .catch(error => {
                    console.log({ error });
                });
                
        } else {
            console.log("there are no files.");
        }
      }
    }
  }
</script>

<style scoped>

</style>
