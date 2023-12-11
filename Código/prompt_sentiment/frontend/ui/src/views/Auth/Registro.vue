<template>
    <v-main>
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
                            <v-toolbar-title>Registro</v-toolbar-title>
                            <v-spacer/>

                        </v-toolbar>
                        <v-card-text>
                            <v-form>
                                <v-text-field
                                        v-model="nombre"
                                        label="Nombre"
                                        name="name"
                                        prepend-icon="person"
                                        type="text"
                                />
                                <v-text-field
                                        v-model="email"
                                        label="Email"
                                        name="login"
                                        prepend-icon="mail_outline"
                                        type="text"
                                />

                                <v-text-field
                                        v-model="password"
                                        id="password"
                                        label="Password"
                                        name="password"
                                        prepend-icon="lock"
                                        type="password"
                                />
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn color="secondary" @click="cancel">Cancelar</v-btn>
                            <v-spacer/>
                            <v-btn color="primary" @click="register">Aceptar</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>

<script>
    export default {
        name: "Register",
        data() {
            return {
                email: "",
                password: "",
                nombre: ""
            };
        },
        methods:{
            register(){
                let email = this.email
                let password = this.password
                let name = this.nombre
                this.$store.dispatch('register', {name, email, password})
                    .then(() => this.$router.push('/'))
                    .catch(err => console.log(err))
            },
            
            cancel(){
                this.$router.push('/login')
            }
        }
    }
</script>

<style scoped>

</style>
