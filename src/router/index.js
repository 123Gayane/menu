import { createRouter, createWebHistory } from 'vue-router'
import SignupSign from '../views/SignupSign.vue'
import SigninSign from '../views/SigninSign.vue'
import ProductsPro from '../views/ProductsPro.vue'

import AddProduct from '@/views/AddProduct.vue'
import ManagerMan from '@/views/ManagerMan.vue'

import store from '@/store'



const metadata =  store
console.log(metadata);

const routes = [

  {
    path:"/products",
    component:ProductsPro,
    name:"products",
    // meta: { requiresAuth: true },
  },
  {
    path:"/signup",
    component:SignupSign,
    name:"signup",
    meta: {check_auth :true}
  },

  {
    path:"/",
    component:SigninSign,
    name:"signin",
    meta: {check_auth :true}
  },



  {
    path:"/addProduct",
    component:AddProduct,
    name:"addProduct",
    // meta: { requiresAuth: true },
  },
  {
    path:"/manager",
    component:ManagerMan,
    name:"manager",
    // meta: { requiresAuth: true },
  }



]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;



  if (to.meta.requiresAuth && !isAuthenticated) {
    // If the route requires authentication and the user is not authenticated, redirect to signin
    next({ name: 'signin' });
  } else if (to.meta.check_auth && isAuthenticated) {
    // If the route is a public route (signup/signin) and the user is already authenticated, redirect to products
    next({ name: 'products' });
  } else {
    // Allow navigation
    next();
  }
});




  


export default router
