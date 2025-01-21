<template>
    <div>
      <section class="vh-100 bg-image">
        <div class="mask d-flex align-items-center justify-content-center gradient-custom-3">
          <div class="container h-100 d-flex justify-content-center align-items-center">
            <div class="col-12 col-md-9 col-lg-7 col-xl-6">
              <div class="card">
                <div class="card-body p-5">
                  <h2 class="text-uppercase text-center mb-5">Sign Up</h2>
  
                  <form @submit.prevent="handleSubmit">
                    <div class="form-outline mb-4">
                      <input v-model="form.username" type="text" id="username" class="form-control form-control-lg" required />
                      <label class="form-label" for="username">Username</label>
                    </div>
  
                    <div class="form-outline mb-4">
                      <input v-model="form.email" type="email" id="email" class="form-control form-control-lg" required />
                      <label class="form-label" for="email">Email</label>
                    </div>
  
                    <div class="form-outline mb-4">
                      <input v-model="form.password" type="password" id="password" class="form-control form-control-lg" required />
                      <label class="form-label" for="password">Password</label>
                    </div>
  
                    <div class="form-outline mb-4">
                      <select v-model="form.profile.user_type" class="form-select form-select-lg">
                        <option value="chef">Chef</option>
                        <option value="manager">Manager</option>
                      </select>
                      <label class="form-label">User Type</label>
                    </div>
  
                    <div class="d-flex justify-content-center">
                      <button type="submit" class="btn gradient-custom-4 text-body">Sign Up</button>
                    </div>
  
                    <p class="text-center text-muted mt-5 mb-0">Already have an account?
                      <router-link to="/"><u>Login</u></router-link>
                    </p>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
          profile: {
            user_type: 'chef' 
          }
        }
      };
    },
    methods: {
      ...mapActions(['sign_up']),
      async handleSubmit() {
        try {
          await this.$store.dispatch('sign_up', this.form);

        } catch (error) {
          console.error('Signup failed:', error);

        }
      }
    }
  };
  </script>




<style scoped>
.vh-100 {
    height: 100vh;
}

.bg-image {
    background-image: url('https://img.freepik.com/premium-photo/restaurant-manager-briefing-his-kitchen-staff-commercial-kitchen_109285-2448.jpg');
    background-size: cover;
    background-position: center;
}

.mask {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.gradient-custom-3 {
    background: linear-gradient(to right, rgba(132, 250, 176, 0.5), rgba(143, 211, 244, 0.5));
}

.gradient-custom-4 {
    background: linear-gradient(to right, rgba(132, 250, 176, 1), rgba(143, 211, 244, 1));
}

.container {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.card {
    border-radius: 15px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin-right: 40px;
}

.text-uppercase {
    text-transform: uppercase;
}

.text-center {
    text-align: center;
}

.mb-5 {
    margin-bottom: 3rem;
}

.form-outline {
    position: relative;
    margin-bottom: 1.5rem;
}

.form-control {
    display: block;
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control-lg {
    padding: 1rem;
    font-size: 1.25rem;
    border-radius: 0.3rem;
}

.form-label {
    position: absolute;
    top: -0.5rem;
    left: 1rem;
    font-size: 0.85rem;
    color: #6c757d;
    pointer-events: none;
    transition: all 0.2s ease-in-out;
}

.btn {
    display: inline-block;
    font-weight: 400;
    line-height: 1.5;
    text-align: center;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
    user-select: none;
    padding: 0.75rem 1.25rem;
    font-size: 1rem;
    border-radius: 0.375rem;
    transition: all 0.15s ease-in-out;
    color: #fff;
    border: none;
}

.text-body {
    color: #495057;
}

.text-muted {
    color: #6c757d;
}

.mt-5 {
    margin-top: 3rem;
}

.mb-0 {
    margin-bottom: 0;
}

.fw-bold {
    font-weight: 700;
}
</style>
