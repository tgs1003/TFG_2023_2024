<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-card
          class="mx-auto"
          outlined
        >
        <v-card-title>Nombre ({{ stats.total }} reseñas)</v-card-title>
          <v-card-text>
            <p><strong>Positivas</strong>: {{stats.positive}}, <strong>Usuarios enojados</strong>: {{stats.anger}}</p>
            <p><strong>Puntuación media</strong>: {{ stats.mean }}, <strong>Varianza</strong>: {{ stats.variance }}</p>
            <p><strong>Mediana</strong>: {{ stats.median }}, <strong>Moda</strong>: {{ stats.mode }}</p>
          </v-card-text>
        </v-card>
        <v-card
          class="mx-auto"
          outlined
        >
        <v-card-title>Reseñas por puntuación</v-card-title>
          <v-card-text>
            <Bar :chart-options="chartOptions"
            :chart-data="processResults"/>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6"><v-card
          class="mx-auto"
          outlined
        >
        <v-card-title>Reseñas positivas vs negativas</v-card-title>
          <v-card-text>
            <Pie :chart-options="chartOptions"
          :chart-data="chartData"></Pie>
          </v-card-text>
        </v-card></v-col>
     
    </v-row>
  </v-container>
</template>
<script>
  import { Pie, Bar } from 'vue-chartjs'
  import api from '../services/api'
  
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)
  

export default {
    name: "Stats",
    data: () => ({
      processResults:{},
      labels:["Una estrella","Dos estrellas", "Tres estrellas", "Cuatro estrellas", "Cinco estrellas"],    
      chartData: {
          labels: ['Positivas', 'Negativas'],
          datasets: [
            {
              backgroundColor: ['#41B883', '#E46651'],
              data: [40, 20]
            }
          ]
        },
        
      chartOptions: {
          responsive: true,
          maintainAspectRatio: false
      },
      stats: {}      
       
    }),
    components: {
      Pie,
      Bar
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
      api.get('/datasets/' + this.datasetId + "/stats").then((resp)=>{
              this.processResults = {datasets: [{label: 'Número de reseñas',
                                                 backgroundColor: 'green',
                                                 data:resp.data['ocurrences']}]
                                                ,labels: this.labels}
              this.stats = resp.data
              this.chartData = {datasets: [{label: 'Número de reseñas',
                                                 backgroundColor: ['green', 'red'],
                                                 data:[this.stats["positive"],
                                                       this.stats["total"]-this.stats["positive"]]}]
                                                ,labels: ['Positivas', 'Negativas']}
              
              })
      }
    }
}
</script>