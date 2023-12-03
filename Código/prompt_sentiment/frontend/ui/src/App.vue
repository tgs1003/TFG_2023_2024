<template>
    <v-app>
        <Navbar v-if="this.$store.getters.isLoggedIn"/>
        <v-main class="ma-4">
            <router-view></router-view>
        </v-main>
        <Footer v-if="this.$store.getters.isLoggedIn"/>
    </v-app>
</template>
<script>
    import Navbar from "./components/Navbar";
    import Footer from "./components/Footer";

    export default {
        name: 'App',
        components: {Navbar, Footer},
    }
</script>
