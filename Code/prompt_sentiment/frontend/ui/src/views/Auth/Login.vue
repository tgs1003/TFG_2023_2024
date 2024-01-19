<template>
    <v-main>
        
        <v-alert v-if="errorMessage != ''"
            color="#f5b7b1"
            variant="outlined"
            >
            <template v-slot:title>
                Error
            </template>
            {{ errorMessage }}
        </v-alert>
        <v-container
                class="fill-height"
                fluid
        >
            <v-row
                    align="center"
                    justify="center"
                >
                <v-col cols = "2"><v-img :src="require('../../assets/logo_sentiment3_trans.png')" :width="160"></v-img></v-col>
                <v-col
                        cols="8"
                        
                >
                <v-card>
                    <v-card-text>
                        <h1>{{ $formatMessage('login.title') }}</h1>
                        <p>{{ $formatMessage('login.subtitle') }}</p>
                        {{ $formatMessage('login.desc') }}
                    </v-card-text>
                </v-card>
                </v-col>
                <v-col cols="2"><v-select :label="$formatMessage('navbar.language')" @change="selectLang($event)" v-model="selectedLang" :items="langs"></v-select></v-col>
            </v-row>
            <v-row
                    align="center"
                    justify="center"
            >
                <v-col
                        cols="12"
                        md="4"
                        sm="8"
                >
                    <v-card class="elevation-12">
                        <v-toolbar
                                color="primary"
                                dark
                                flat
                        >
                            <v-toolbar-title>{{ $formatMessage('login.dialog.title') }}</v-toolbar-title>
                            <v-spacer/>

                        </v-toolbar>
                        <v-card-text>
                            <v-form>
                                <v-text-field
                                        v-model="email"
                                        :label="$formatMessage('login.dialog.email')"
                                        name="email"
                                        prepend-icon="person"
                                        :error-messages="emailErrors"
                                        required
                                        type="text"
                                />

                                <v-text-field
                                        v-model="password"
                                        id="password"
                                        :label="$formatMessage('login.dialog.password')"
                                        name="password"
                                        :error-messages="passwordErrors"
                                        required
                                        prepend-icon="lock"
                                        type="password"
                                />
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn color="primary" @click="register">{{ $formatMessage('login.dialog.register') }}</v-btn>
                            <v-spacer/>
                            <v-btn color="primary" @click="login">{{ $formatMessage('login.dialog.login') }}</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
            
        </v-container>
        
    </v-main>
        
</template>

<script>
    import { validationMixin } from 'vuelidate'
    import { required, email } from 'vuelidate/lib/validators'
    import TokenService from '../../services/token.service'
    export default {
        name: "Login",
        mixins: [validationMixin],

        validations: {
        email: { required, email },
        password: { required },
        
        },
        data() {
            return {
                email: "",
                password: "",
                errorMessage: "",
                selectedLang: null,
                langs: ['English','Español'],
            };
        },
        computed:{
            emailErrors () {
                const errors = []
                if (!this.$v.email.$dirty) return errors
                !this.$v.email.email && errors.push(this.$formatMessage('login.error.email.invalid'))
                !this.$v.email.required && errors.push(this.$formatMessage('login.error.email.required'))
                return errors
            },
            
            passwordErrors(){
                const errors = []
                if (!this.$v.password.$dirty) return errors
                !this.$v.password.required && errors.push(this.$formatMessage('login.error.password.required'))
                return errors
            },
        },
        created() {
                if(this.$root.$i18n.locale == 'en')
                    this.selectedLang = 'English'
                else
                    this.selectedLang = 'Español'
        },
        methods:{
            login(){
                this.$v.$touch()
                if (this.$v.$invalid)
                    return
                this.errorMessage = ""
                let email = this.email
                let password = this.password
                this.$store.dispatch('login', {email, password})
                    .then(response=>{
                        if(response.status == 200)
                            this.$router.push('/')
                        this.errorMessage = this.$formatMessage('login.error.password.incorrect');
                        }
                    )
                    .catch(err => {
                        this.errorMessage = err;
                        console.log(err);
                    })
            },
            
            register(){
                this.$router.push('/registro')
            },
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
            }
        }
    }
</script>

<style scoped>

</style>
