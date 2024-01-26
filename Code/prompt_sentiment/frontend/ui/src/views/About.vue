<template>
    <div>
    <v-toolbar>
        <v-btn icon @click="$router.push('/')"> <v-icon>mdi-arrow-left</v-icon></v-btn>
        <v-toolbar-title id="about_title">{{$formatMessage("about.title")}}</v-toolbar-title>
      </v-toolbar>
      <p></p>
      
    <v-card>
      <v-row><v-col>
      <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          {{ $formatMessage("about.author") }}
        </div>
      <v-list-item-title class="text-h7 mb-1">
          Teodoro Ricardo García Sánchez
        </v-list-item-title>
        <v-list-item-subtitle>tgs1003@alu.ubu.es</v-list-item-subtitle>
      </v-list-item-content>
      </v-list-item>
      </v-col><v-col>
      <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          {{ $formatMessage("about.tutors") }}
        </div>
      <v-list-item-title class="text-h8 mb-1">
          Virginia Ahedo García (vahedo@ubu.es) y
          Jose Ignacio Santos Martín (jisantos@ubu.es)
        </v-list-item-title>
        <v-list-item-subtitle>Departamento de Ingeniería de Organización</v-list-item-subtitle>
      </v-list-item-content>
      </v-list-item>
    </v-col></v-row>
    </v-card>
    <p></p>
    <v-card>
    <v-card-title>Software:</v-card-title>
      <v-row><v-col>
      <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          Backend:
        </div>
      <v-list-item-title class="text-h7 mb-1">
          <a href="https://www.python.org" target="_blank">Python</a>, <a href="https://flask.palletsprojects.com/" target="_blank">Flask</a>, <a href="https://github.com/python-restx/flask-restx" target="_blank">Flask-restx</a>, <a href="https://pytest.org" target="_blank">pytest</a>, <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy</a>, <a href="https://www.postgresql.org/" target="_blank">PostgreSQL</a>, <a href="https://www.openai.com" target="_blank">OpenAI</a>
        </v-list-item-title>
      </v-list-item-content>
      </v-list-item>
      </v-col><v-col>
      <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          Frontend:
        </div>
      <v-list-item-title class="text-h7 mb-1">
          <a href="https://nodejs.org" target="_blank">Node.js</a>, <a href="https://vuejs.org" target="_blank">Vue.js</a>, <a href="http://v2.vuetifyjs.com" target="_blank">VuetifyJS</a>, <a href="https://www.chartjs.org">Chart.js</a>, <a href="https://kazupon.github.io/vue-i18n/">Vue-i18n</a>
        </v-list-item-title>
      </v-list-item-content>
      </v-list-item>
    </v-col></v-row>
    </v-card>
    <p></p>
    <v-card>
    <v-card-title>{{ $formatMessage("about.other") }}</v-card-title>
      <v-row>
      <v-col>
      <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          {{ $formatMessage("about.infrastructure") }}
        </div>
      <v-list-item-title class="text-h7 mb-1">
        <a href="https://www.ubuntu.com" target="_blank">Ubuntu</a>, <a href="https://www.docker.com" target="_blank">Docker</a>, <a href="https://www.contabo.com" target="_blank">Contabo</a>, <a href="https://www.ngix.com" target="_blank">Ngix</a>, <a href="https://www.portainer.io" target="_blank">Portainer</a>, <a href="https://letsencrypt.org" target="_blank">Let's Encrypt</a>
        </v-list-item-title>
      </v-list-item-content>
      </v-list-item>
      </v-col>
      <v-col>
      <v-list-item three-line>
      <v-list-item-content>
        <div class="text-overline mb-4">
          Editor:
        </div>
      <v-list-item-title class="text-h7 mb-1">
          <a href="https://code.visualstudio.com" target="_blank">Visual Studio Code</a>
        </v-list-item-title>
      </v-list-item-content>
      </v-list-item>
      </v-col>

      </v-row>
    </v-card>
    <v-card>
    <v-card-text align="center">
      {{ $formatMessage('about.app') }}<a href="https://www.ubu.es" target="_blank">Universidad de Burgos</a>
    </v-card-text>

    <v-divider></v-divider>
    <v-card-actions>
      <v-btn text @click="viewRepo">
        {{ $formatMessage('about.repository') }}
      </v-btn>
    </v-card-actions>
  </v-card>
    </div>
</template>


  
<script>
export default {
data: () => ({
  
}),
methods:{
  viewRepo(){
    this.$router.push('https://github.com/tgs1003/TFG_2023_2024')
  },
}
}
</script>