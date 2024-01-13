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
                <v-col
                        cols="8"
                        
                >
                <v-card>
                    <v-card-text>
                        <h1>Bienvenidos a Prompt Sentiment</h1>
                        <p>Una aplicación para análisis de sentimiento.</p>
                        Creada como trabajo de fin de grado del Grado de Ingeniería Informática de la Universidad de Burgos.
                    </v-card-text>
                </v-card>
                </v-col>
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
                            <v-toolbar-title>Login</v-toolbar-title>
                            <v-spacer/>

                        </v-toolbar>
                        <v-card-text>
                            <v-form>
                                <v-text-field
                                        v-model="email"
                                        label="Email"
                                        name="email"
                                        prepend-icon="person"
                                        :error-messages="emailErrors"
                                        required
                                        type="text"
                                />

                                <v-text-field
                                        v-model="password"
                                        id="password"
                                        label="Password"
                                        name="password"
                                        :error-messages="passwordErrors"
                                        required
                                        prepend-icon="lock"
                                        type="password"
                                />
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn color="primary" @click="register">Registro</v-btn>
                            <v-spacer/>
                            <v-btn color="primary" @click="login">Login</v-btn>
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
                errorMessage: ""
            };
        },
        computed:{
            emailErrors () {
                const errors = []
                if (!this.$v.email.$dirty) return errors
                !this.$v.email.email && errors.push('Must be valid e-mail')
                !this.$v.email.required && errors.push('E-mail is required')
                return errors
            },
            
            passwordErrors(){
                const errors = []
                if (!this.$v.password.$dirty) return errors
                !this.$v.password.required && errors.push('Password is required')
                return errors
            
            }
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
                        this.errorMessage = "Usuario o contraseña incorrectos."
                        }
                    )
                    .catch(err => {
                        this.errorMessage = err;
                        console.log(err);
                    })
            },
            
            register(){
                this.$router.push('/registro')
            }
        }
    }
</script>

<style scoped>

</style>
