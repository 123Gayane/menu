<template>
  <div>
    <!-- Ingredients Section -->
    <h1>All Ingredients</h1>
    <ul>
      <li v-for="ingredient in ingredients" :key="ingredient.id" class="ingredient-item">
        {{ ingredient.name }} - ${{ ingredient.cost }}
        <button @click="delete_Ingredient(ingredient.id)" class="delete-button">Delete</button>
      </li>
    </ul>

    <h1>Add Ingredient</h1>
    <form @submit.prevent="addIngredient" class="add-ingredient-form">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" v-model="newIngredient.name" id="name" required>
      </div>

      <div class="form-group">
        <label for="cost">Cost:</label>
        <input type="number" v-model.number="newIngredient.cost" id="cost" required>
      </div>

      <button type="submit" class="submit-button">Add</button>
    </form>

    <!-- Products Section -->
    <h1>All Products</h1>
    <ul>
      <li v-for="product in products" :key="product.id" class="product-item">
        {{ product.name }} - ${{ product.selling_price }}
        <button @click="toggleProductAvailability(product.id, product.available)" class="availability-button">
          {{ product.available ? 'Mark Unavailable' : 'Mark Available' }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  computed: {
    ...mapState({
      ingredients: state => state.ingredients,
      products: state => state.products // Assuming products are stored in Vuex state
    })
  },
  data() {
    return {
      newIngredient: {
        name: '',
        cost: null
      }
    };
  },
  methods: {
    ...mapActions(['get_ingredients', 'add_ingredient', 'deleteIngredient', 'get_products', 'mark_product_unavailable']),
    async addIngredient() {
      try {
        await this.add_ingredient(this.newIngredient); 
        this.newIngredient.name = '';
        this.newIngredient.cost = null;
      } catch (error) {
        console.error('Error adding ingredient:', error);
      }
    },
    delete_Ingredient(id) {
      this.deleteIngredient(id);
    },

    async toggleProductAvailability(productId) {
      try {
        await this.mark_product_unavailable( productId);
        this.$router.push('/products')
      } catch (error) {
        console.error('Error updating product availability:', error);
      }
    }
  },
  mounted() {
    this.get_ingredients(); 
    this.get_products(); // Fetch products when the component is mounted
  }
};
</script>

<style scoped>
h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

.ingredient-item,
.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.delete-button {
  background-color: #e74c3c;
  color: #fff;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 3px;
}

.delete-button:hover {
  background-color: #c0392b;
}

.add-ingredient-form {
  margin-top: 20px;
  max-width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  background-color: #3498db;
  color: #fff;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 3px;
}

.submit-button:hover {
  background-color: #2980b9;
}

.availability-button {
  background-color: #2ecc71;
  color: #fff;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 3px;
}

.availability-button:hover {
  background-color: #27ae60;
}

.availability-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
</style>
