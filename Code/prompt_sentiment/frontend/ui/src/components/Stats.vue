<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-card
          class="mx-auto"
          outlined
        >
        <v-card-title> {{ stats.name }} ({{ stats.total }} {{ $formatMessage('stats.reviews') }})</v-card-title>
          <v-card-text>
            <p><strong>{{ $formatMessage('stats.positives') }}</strong>: {{stats.positive}}, <strong>{{ $formatMessage('stats.anger') }}</strong>: {{stats.anger}}</p>
            <p><strong>{{ $formatMessage('stats.mean') }}</strong>: {{ stats.mean }}, <strong>{{ $formatMessage('stats.variance') }}</strong>: {{ stats.variance }}</p>
            <p><strong>{{ $formatMessage('stats.median') }}</strong>: {{ stats.median }}, <strong>{{ $formatMessage('stats.mode') }}</strong>: {{ stats.mode }}</p>
          </v-card-text>
        </v-card>
        <v-card
          class="mx-auto"
          outlined
        >
        <v-card-title>{{ $formatMessage('stats.review_by_punc') }}</v-card-title>
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
        <v-card-title>{{ $formatMessage('stats.positive_vs_negative') }}</v-card-title>
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
      labels:[],    
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
              this.processResults = {datasets: [{label: this.$formatMessage('stats.review_number'),
                                                 backgroundColor: 'green',
                                                 data:resp.data['ocurrences']}]
                                                ,labels: this.labels}
              this.stats = resp.data
              this.chartData = {datasets: [{label: this.$formatMessage('stats.review_number'),
                                                 backgroundColor: ['green', 'red'],
                                                 data:[this.stats["positive"],
                                                       this.stats["total"]-this.stats["positive"]]}]
                                                ,labels: [this.$formatMessage('stats.positives'), this.$formatMessage('stats.negatives')]}
              
              })
              this.labels.push(1 + " " + this.$formatMessage('stats.star'))
              let i = 0
              for(i=2;i<=5;i++)
              {
                this.labels.push(i + " " + this.$formatMessage('stats.stars'))
              }
      }
    }
}
</script>