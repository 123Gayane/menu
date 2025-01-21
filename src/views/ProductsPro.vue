<template>
  <div class="products-container">
    <h1>MENU</h1>

    <div v-if="products.length" class="products-list">
      <ul>
        <li v-for="product in products" :key="product.id" class="product-item">
          <div class="product-header">
            <h2>{{ product.name }}</h2>
            <img src="https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?cs=srgb&dl=pexels-ash-122861-376464.jpg&fm=jpg" class="product-image" />
          </div>
          <div class="product-actions">
            <label>
              <input type="checkbox" name="q3" class="tm-radio-group-2 with-gap" value="q3_a2" />
              Select
            </label>
            <input type="number" id="typeNumber" class="quantity-input" placeholder="How many?" />
            <div v-if="user && user.user_type === 'manager'">
            <button v-if="product.available" @click="markProductUnavailable(product.id)" class="unavailable-button">Mark Unavailable</button>
           </div>
            <p v-if="!product.available" class="unavailable-text">No product available</p>
          </div>
          <p class="price">Selling Price: ${{ product.selling_price }}</p>
          <p class="ingredients-title">Ingredients:</p>
    
          <ul class="ingredients-list">
            <li v-for="ingredient in product.ingredients" :key="ingredient.id" class="ingredient-item">
              {{ ingredient.name   }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div v-else>
      <p class="no-products">No products available.</p>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions ,mapState} from 'vuex';

export default {
  name: 'ProductsPage',
  computed: {
    ...mapGetters(['getProducts']),
    products() {
      return this.getProducts;
    }
  },
  methods: {
    ...mapState(['user','ingredients']),
    ...mapActions(['get_products', 'mark_product_unavailable']),
    fetchProducts() {
      this.get_products();
    },
    markProductUnavailable(productId) {
      this.mark_product_unavailable(productId);
    }
  },
  created() {
    this.fetchProducts();
  }
};
</script>

<style scoped>
.products-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
  background: #f4f4f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.products-list {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.product-item {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
}

.product-header {
  position: relative;
  margin-bottom: 15px;
}

.product-item h2 {
  margin: 0;
  color: #333;
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
}

.product-image {
  width: 100%;
  height: 150px;
  border-radius: 8px;
  margin-top: 10px;
  object-fit: cover;
}

.product-actions {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.quantity-input {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-top: 10px;
}

.unavailable-button {
  background-color: #ff6b6b;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.unavailable-button:hover {
  background-color: #e05656;
}

.unavailable-text {
  color: #ff6b6b;
  font-weight: bold;
}

.price {
  color: #333;
  font-size: 1.2rem;
  margin: 15px 0;
  font-weight: bold;
}

.ingredients-title {
  color: #333;
  font-size: 1.1rem;
  margin-top: 15px;
  font-weight: bold;
}

.ingredients-list {
  padding-left: 20px;
  margin-top: 10px;
  list-style-type: none;
}

.ingredient-item {
  background: #fafafa;
  border-radius: 5px;
  padding: 8px;
  margin-bottom: 5px;
  color: #555;
}

.no-products {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-top: 20px;
}
</style>
