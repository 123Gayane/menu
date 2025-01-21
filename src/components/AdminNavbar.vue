<template>
  <nav v-if="user" class="navbar">
    <div class="navbar-brand">
      <img src="https://image.similarpng.com/very-thumbnail/2021/07/Chef-restaurant-logo-illustrations-template-on-transparent-background-PNG.png" width="40px" class="logo-pic">
    </div>
    <div class="navbar-links">
      <router-link :to="{name:'products'}">Products</router-link>
      <router-link v-if="user && user.user_type === 'chef'" :to="{name:'addProduct'}">Add Product</router-link>
      <router-link v-if="user && user.user_type === 'manager'" :to="{name:'manager'}">Manager</router-link>
      <router-link v-if="!user" :to="{name:'signup'}">Register</router-link>
      <div class="hello">
        <button @click="handleLogout" class="logout-button">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState(['user']),
    
    
  },

  
  methods: {
    ...mapActions(['logout']),
    handleLogout() {
      this.logout();
      this.$router.push({ name: 'signin' });

      
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #323c6fb9; 
  color: #fff;
}

.navbar-brand {
  flex: 1; 
}

.navbar-links {
  display: flex;
  gap: 20px;
}

.navbar-links router-link {
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
}

.logout-button {
  padding: 8px 16px;
  background-color: #170b2bad;
  color: #fff;
  border: none;
  border-radius: 40px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #1c431e; /* Darker shade on hover */
}

.logo-pic {
  border-radius: 80px;
}

.hello {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-right: 400px;
}
</style>
