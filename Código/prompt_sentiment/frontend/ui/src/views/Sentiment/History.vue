<template>
    <v-carousel v-model="dataset">
      <v-carousel-item
        v-for="(dataset, i) in datasets"
        :key="dataset"
      >
        <v-sheet
          :color="dataset"
          height="100%"
          tile
        >
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <div class="text-h2">
              Slide {{ i + 1 }}
            </div>
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
  </template>

<script>
export default {
  data: () => ({
    dataset: 0,
    datasets: [
      1,
      2,
      3,
      4,
      5,
    ],
  }),
}
</script>