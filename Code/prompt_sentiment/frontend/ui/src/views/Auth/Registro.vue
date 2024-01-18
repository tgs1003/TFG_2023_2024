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
                            <v-toolbar-title>{{$formatMessage('register.title')}}</v-toolbar-title>
                            <v-spacer/>

                        </v-toolbar>
                        <v-card-text>
                            <v-form>
                                <v-text-field
                                        v-model="name"
                                        :label="$formatMessage('register.name')"
                                        name="name"
                                        autocomplete="off"
                                        required
                                        :error-messages="nameErrors"
                                        prepend-icon="person"
                                        type="text"
                                        value=""
                                        
                                />
                                <v-text-field
                                        v-model="email"
                                        :label="$formatMessage('register.email')"
                                        name="email"
                                        autocomplete="off"
                                        required
                                        :error-messages="emailErrors"
                                        prepend-icon="mail_outline"
                                        type="text"
                                        value=""
                                        
                                />

                                <v-text-field
                                        v-model="password"
                                        id="password"
                                        :label="$formatMessage('register.password')"
                                        autocomplete="new-password"
                                        required
                                        :error-messages="passwordErrors"
                                        name="password"
                                        prepend-icon="lock"
                                        type="password"
                                />
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn color="secondary" @click="cancel">{{$formatMessage('register.cancel')}}</v-btn>
                            <v-spacer/>
                            <v-btn color="primary" @click="register">{{$formatMessage('register.ok')}}</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>

<script>
    import { validationMixin } from 'vuelidate'
    import { required, email, minLength } from 'vuelidate/lib/validators'
    export default {
        
        mixins: [validationMixin],
        validations: {
        name: {required},
        email: { required, email },
        password: { required, minLength: minLength(6) },
        
        },
        data() {
            return {
                email: "",
                password: "",
                name: "",
                fieldTypes: { // add this for change input type
                    name:"text",
                    email:"text",
                    password: "text",
                },
                errorMessage: ""
            };
        },
        computed:{
            emailErrors () {
                const errors = []
                if (!this.$v.email.$dirty) return errors
                !this.$v.email.email && errors.push(this.$formatMessage('register.error.email.invalid'))
                !this.$v.email.required && errors.push(this.$formatMessage('register.error.email.required'))
                return errors
            },
            nameErrors(){
                const errors = []
                if (!this.$v.name.$dirty) return errors
                !this.$v.name.required && errors.push(this.$formatMessage('register.error.name.required'))
                return errors
            },
            passwordErrors(){
                const errors = []
                if (!this.$v.password.$dirty) return errors
                !this.$v.password.required && errors.push(this.$formatMessage('register.error.password.required'))
                return errors
            
            }
        },
        methods:{
            register(){
                this.errorMessage=""
                this.$v.$touch()
                if (this.$v.$invalid)
                    return
                let email = this.email
                let password = this.password
                let name = this.name
                this.$store.dispatch('register', {name, email, password})
                .then(response=>{
                    if(response.status == 201)
                        this.$router.push('/')
                    this.errorMessage = this.$formatMessage('register.error.user.exists')
                })    
            },
            
            cancel(){
                this.$router.push('/login')
            }
        }
    }
</script>

<style scoped>

</style>
