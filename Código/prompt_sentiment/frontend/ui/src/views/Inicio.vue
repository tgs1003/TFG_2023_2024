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
              Análisis de reseñas
            </v-card-title>

            <v-card-subtitle>Para analizar un fichero de reseñas, haga clic aquí.</v-card-subtitle>

            <v-card-actions>
              <v-btn text>
                Analizar reseñas
              </v-btn>
            </v-card-actions>
          </v-card>
          
        </div>
        <div class="my-2">
          <v-card
            
          >
            <v-card-title class="text-h5">
              {{ $formatMessage('home.history') }}
            </v-card-title>

            <v-card-subtitle>Para ver el histórico de análisis de reseñas haga clic aquí.</v-card-subtitle>

            <v-card-actions>
              <v-btn text>
                Ver histórico
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
}
</script>