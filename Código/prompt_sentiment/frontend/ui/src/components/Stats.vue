<template>
{{ datasetId }}
</template>
<script>
export default {
    name: "Stats",
    data: () => ({    
    }),
    components: {

    },
    props: {
      datasetId:
      {
        type: Number,
        default:0
      }
    }
}
</script>