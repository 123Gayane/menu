import { createStore } from 'vuex';
import axios from 'axios';
import router from '@/router';

export default createStore({
  state: {
    user: null,
    url: "http://127.0.0.1:8000/",
    products: [],
    ingredients:[],
    isLoggedIn: !!localStorage.getItem('user'),
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      console.log(user);
      
    },
    change_user_error(state, obj) {
      state.user_error = obj;
    },
    setProducts(state,products){
      state.products = products;
    },
    setIngredients(state,Ingredient){
      state.ingredients = Ingredient

    },
    addProduct(state, product) {
      state.products.push(product);
    },
    addingredient(state,obj){
      state.ingredients.push(obj)

    },
    SET_LOGOUT(state) {
      state.isLoggedIn = false
      state.user = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },


    MARK_PRODUCT_UNAVAILABLE(state, productId) {
      const product = state.products.find(product => product.id === productId);
      if (product) {
        product.is_available = false;
      }
    }

  },

  actions: {
    async sign_up({ state, commit }, obj) {
        let {data} = await axios.post(state.url + "signup/", obj);
        console.log(data);
        router.push({ name: "signin" });
 {
        console.log(data);
        commit("change_user_error", data);
      }
    },
    async sign_in({ state, commit ,dispatch}, obj) {
      try {
        let { data } = await axios.post(state.url + "signin/", obj);
        console.log(data);
        localStorage.token = data.token;
    
        router.push({ name: "products" });
        dispatch("get_user")

      } catch (err) {
        console.log(err.response.data.message);
        commit("change_user_error", err.response.data);
      }
    },
 
    async get_products({state,commit}){
      let config = {
        headers: { 
          'Authorization': `Token ${localStorage.token}` },
      };
      let {data} = await axios.get(state.url + "products/", config);
        console.log(data);
        commit("setProducts",data)

    },

        async add_ingredient({state, commit},ingredientData){
          let config = {
            headers: { 
              'Authorization': `Token ${localStorage.token}` },
          };
          let {data} =  await axios.post(state.url+"ingredients/add/", ingredientData,config);
          console.log(data);
          commit('addingredient', data)

        },

        async get_ingredients({state,commit}){
          let config = {
            headers: { 
              'Authorization': `Token ${localStorage.token}` },
          };
          let {data} = await axios.get(state.url + "ingredients/", config);
          console.log(data);
          commit("setIngredients",data)

  },
  async add_product({ state, commit }, product) {
    try {
   
      let config = {
        headers: { 
          'Authorization': `Token ${localStorage.token}` },
      };
      const response = await axios.post(state.url + 'products/add/', product, config);
      console.log('Product added:', response.data);
      commit('addProduct', response.data);
      return response.data;

    } catch (error) {
      console.error('Error adding product:', error);
      throw error;
    }
  },

  async fetchIngredients({state, commit }) {
    const response=  await axios.get(state.url+'ingredients/')
     
        commit('setIngredients', response.data);
        console.log(response);
        
 
  },

    async deleteIngredient({ state }, id) {
      try {
        let config = {
          headers: {
            'Authorization': 'Token ' + localStorage.token
          }
        }
        await axios.delete(state.url +`ingredients/${id}/delete/`, config);
        state.ingredients = state.ingredients.filter(elm => elm.id !== id);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.message };
      }
    },

    async mark_product_unavailable({state, commit }, productId) {
      try {
        let config = {
          headers: {
            'Authorization': 'Token ' + localStorage.token
          }
        }
        await axios.patch(`${state.url}products/${productId}/unavailable/`, config);
        commit('MARK_PRODUCT_UNAVAILABLE', productId);
      } catch (error) {
        console.error('Error marking product unavailable:', error);
      }
    },

    async logout({state, commit }) {
      const config = {
        headers: {
          "Authorization": `Token ${localStorage.token}`,
        },
      }
      try {
        const { data } = await axios.post(`${state.url}log_out/`, {}, config)
        console.log(data)
        localStorage.removeItem("token")
        commit("SET_LOGOUT")
        router.push({ name: "signin" })  
      } catch (err) {
        console.log(err.response.data)
      }
    },


    async get_user({ state, commit}) {
      const config = {
        headers: {
          "Authorization": `Token ${localStorage.token}`,
        },
      }
      try {
        const { data } = await axios.get(`${state.url}get_user/`, config)
        console.log(data)
        console.log("hello", data.user);
        commit("setUser", data.user)
        if(data.user.user_type == 'admin'){
          router.push("/products")
        }else if (data.user.user_type === 'manager') {
          // const managerId = data.user.id
          router.push("/manager");
        }else if (data.user.user_type === 'chef'){
          // const customerId = data.user.id
          router.push("/addProduct");
        }
      
        return data
      } catch (err) {
        console.log(err.response.data)
        
      }
     
    },

 
  },
  getters: {
    isAuthenticated: state => !!state.user,
    getUserError: state => state.user_error,
    getProducts: state => state.products,
    allIngredients: (state) => state.ingredients,
    products: (state) => state.products,
    ingredients: (state) => state.ingredients,

    totalCost: (state) => (selectedIngredients) => {
      return selectedIngredients.reduce((total, ingredientId) => {
        const ingredient = state.ingredients.find(i => i.id === ingredientId);
        return ingredient ? total + parseFloat(ingredient.cost) : total;
      }, 0).toFixed(2);
    },
    // Calculate the selling price based on the total cost
    calculatedSellingPrice: (state, getters) => (selectedIngredients) => {
      const totalCost = parseFloat(getters.totalCost(selectedIngredients));
      return (totalCost * 1.15).toFixed(2);
    },
  
 
  }
});







 

