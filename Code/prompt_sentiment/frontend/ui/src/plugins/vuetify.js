// src/plugins/vuetify.js
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify)

const opts = {
    icons:{
        iconfont:'md'
    },
    themes:{
        light: {
            primary: colors.red.darken1,
        },
        dark:{
            primary: colors.red.darken1,
        }
    }
}

export default new Vuetify(opts)
