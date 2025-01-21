<template>
  <div id="app">
    <AdminNavbar />
    <router-view />
  </div>
</template>

<script>
import AdminNavbar from './components/AdminNavbar.vue';
import { mapActions } from 'vuex';

export default {
  name: "App",
  components: {
    AdminNavbar
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      this.get_user(); // Fetch the user if the token is present
    }
  },
  methods: {
    ...mapActions(['get_user']),
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
