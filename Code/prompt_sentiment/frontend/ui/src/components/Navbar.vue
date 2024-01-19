<template>
    <nav>
        <v-app-bar :dark="this.$store.state.dark" app color="gray">

            <v-toolbar-title>
                <v-img :src="require('../assets/logo_sentiment3_trans.png')" :width="160"></v-img>
            </v-toolbar-title>
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-spacer>
            </v-spacer>
            <v-menu offset-y>
                <template v-slot:activator="{ on }">
                    <v-btn
                            text
                            v-on="on"
                    >
                        <v-icon left>expand_more</v-icon>
                        <span>{{$formatMessage('navbar.menu')}}</span>
                    </v-btn>
                </template>
                <v-list flat>
                    <v-list-item :key="link.text" :to="link.route" active-class="border" router v-for="link in links">
                        <v-list-item-title>{{link.text}}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <v-btn @click="logout" text>
                <span>{{ $formatMessage('navbar.logout') }}</span>
                <v-icon right>exit_to_app</v-icon>
            </v-btn>
        </v-app-bar>
        <v-navigation-drawer left :dark="this.$store.state.dark" app class="gray darken-4" v-model="drawer">
            <v-list flat>
                <v-switch :label="$formatMessage('navbar.darkmode')" @change="switchColor" v-model="mode"></v-switch>
                <v-list-item :key="link.text" :to="link.route" active-class="border" router v-for="link in links">
                    <v-list-item-action>
                        <v-icon>{{link.icon}}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>{{link.text}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                <v-list-item>
                    
                </v-list-item>
            </v-list>
            <template v-slot:append>
          <div class="pa-2">
            <v-select :label="$formatMessage('navbar.language')" @change="selectLang($event)" v-model="selectedLang" :items="langs">
            </v-select>
          </div>
        </template>
        </v-navigation-drawer>
    </nav>
</template>

<script>
    import TokenService from '../services/token.service'
    import api from '../services/api'
    export default {
        name: "Navbar",
        data() {
            return{
            selectedLang: null,
            langs: ['English','Español'],
            mode: true,
            drawer: false,
            menuHome: this.$formatMessage('navbar.menu.home'),
            menuAdmin: this.$formatMessage('navbar.menu.admin'),
            links: [
            ],
            };
        },
        computed: {
            isLoggedIn: function () {
                return this.$store.getters.isLoggedIn
            }
        },
        created() {
            if(this.$root.$i18n.locale == 'en')
                this.selectedLang = 'English'
            else
                this.selectedLang = 'Español'

            this.links.push({"icon": "dashboard", "text": this.$formatMessage('navbar.menu.home'), "route": "/"})
            api.get('/auth/status').then((resp)=>
            {
            var user = resp.data
            if (user.rol == 'Admin'){
                this.links.push({"icon": "shield", "text": 
                this.$formatMessage('navbar.menu.admin'), "route": "/admin-home"})
                }
            this.links.push({"icon": "help_outline", "text": this.$formatMessage('help.title'), "route": this.$formatMessage('help.url')})
            this.links.push({"icon": "info_outline", "text": this.$formatMessage('about.title'), "route": "/about"})
            })
            
        },
        methods: {
            selectLang(event){
                let locale = ''
                if (event=='English'){
                    locale = 'en'
                }
                else{
                    locale = 'es'
                }
                TokenService.setlocale(locale)
                location.reload()
            },
            logout: function () {
                this.$store.dispatch('logout')
                    .then(() => {
                        this.$router.push('/login')
                    })
            },
            switchColor(event) {
                this.$store.state.dark = event
            }
        },
    }
</script>

<style>
    .border {
        border-left: 4px solid cyan;
    }
</style>
