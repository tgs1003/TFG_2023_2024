<template>
    <nav>
        <v-app-bar :dark="this.$store.state.dark" app color="gray">

            <v-toolbar-title>
                <v-img :src="require('../assets/logo_sentiment2_small.png')" :width="150"></v-img>
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
                        <v-list-item-title>{{ this.$formatMessage(link.text) }}</v-list-item-title>
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
                <v-list-item>
                    <v-select @change="selectLang($event)" v-model="selectedLang" :items="langs">
                        
                    </v-select>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </nav>
</template>

<script>
    import TokenService from '../services/token.service'
    export default {
        name: "Navbar",
        data: () => ({
            selectedLang: null,
            langs: ['English','Español'],
            mode: true,
            drawer: false,
            links: [
                {icon: 'dashboard', text: 'navbar.menu.home', route: '/'},
                {icon: 'verified_user', text: 'navbar.menu.admin', route: '/admin-home'},
                
            ],
        }),
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
