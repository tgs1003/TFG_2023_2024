<template>
  <v-row>
    <v-col cols="2"></v-col>
    <v-col
        cols="8"
        sm="8"
      >
      <div class="text-center">
        <div class="my-2">
          <v-card
            
          >
            <v-card-title class="text-h5">
              {{ $formatMessage('home.analysis.title') }}
            </v-card-title>

            <v-card-subtitle>{{ $formatMessage('home.analysis.desc') }}</v-card-subtitle>

            <v-card-actions>
              <v-btn text @click="analysis" color="primary">
                {{ $formatMessage('home.analysis.btn') }}
              </v-btn>
            </v-card-actions>
          </v-card>
          
        </div>
        <div class="my-2">
          <v-card
            
          >
            <v-card-title class="text-h5">
              {{ $formatMessage('home.history.title') }}
            </v-card-title>

            <v-card-subtitle>{{ $formatMessage('home.history.desc') }}</v-card-subtitle>

            <v-card-actions>
              <v-btn text @click="history" color="secondary">
                {{ $formatMessage('home.history.btn') }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
export default {
data: () => ({
 
}),
methods:{
  history(){
    this.$router.push('/history')
  },
  analysis(){
    this.$router.push('/analysis')
  },
}
}
</script>