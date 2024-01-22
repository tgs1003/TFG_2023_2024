<template>
    <vue-pdf-app pdf="manual_de_usuario.pdf" @open="openHandler"></vue-pdf-app>
  </template>
  
  <script>
  // VuePdfApp component is registered in src/main.js
  
  export default {
    name: "Basic",
    methods: {
      openHandler(pdfApp) {
        window._pdfApp = pdfApp;
      },
    },
  };
  </script>