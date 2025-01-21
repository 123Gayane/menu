<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-3xl font-semibold text-gray-800 mb-6">Add Product</h2>

    <form @submit.prevent="submitProduct" class="space-y-6">
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-medium mb-2" for="name">
          Product Name
        </label>
        <input
          v-model="product.name"
          type="text"
          id="name"
          class="block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter product name"
        />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-medium mb-2" for="description">
          Description
        </label>
        <textarea
          v-model="product.description"
          id="description"
          class="block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter product description"
        ></textarea>
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-medium mb-2" for="category">
          Category
        </label>
        <select
          v-model="product.category"
          id="category"
          class="block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="" disabled>Select a category</option>
          <option value="APP">Appetizer</option>
          <option value="ENT">Entree</option>
          <option value="DES">Dessert</option>
          <!-- Add more categories as needed -->
        </select>
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-medium mb-2" for="ingredients">
          Ingredients
        </label>
        <select
          v-model="selectedIngredients"
          multiple
          id="ingredients"
          class="block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option
            v-for="ingredient in allIngredients"
            :key="ingredient.id"
            :value="ingredient.id"
          >
            {{ ingredient.name }} ({{ ingredient.cost }})
          </option>
        </select>
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-medium mb-2">
          Total Cost
        </label>
        <p class="text-xl font-semibold text-gray-900">{{ totalCost }}</p>
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-medium mb-2">
          Selling Price
        </label>
        <p class="text-xl font-semibold text-gray-900">{{ sellingPrice }}</p>
      </div>

      <div class="flex justify-end">
        <button
          type="submit"
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-500 transition duration-300"
        >
          Add Product
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'AddProduct',
  setup() {
    const store = useStore();
    const product = ref({
      name: '',
      description: '',
      category: '',
    });
    const selectedIngredients = ref([]);

    const allIngredients = computed(() => store.getters.allIngredients);
    const totalCost = computed(() => store.getters.totalCost(selectedIngredients.value));
    const sellingPrice = computed(() => store.getters.calculatedSellingPrice(selectedIngredients.value));

    const submitProduct = async () => {
      try {
        const productData = {
          ...product.value,
          ingredient_ids: selectedIngredients.value,
          cost: totalCost.value,
          selling_price: sellingPrice.value,
        };
        await store.dispatch('add_product', productData);
        // Clear the form after successful submission
        product.value.name = '';
        product.value.description = '';
        product.value.category = '';
        selectedIngredients.value = [];
      } catch (error) {
        console.error('Error adding product:', error);
      }
    };

    return {
      product,
      selectedIngredients,
      allIngredients,
      totalCost,
      sellingPrice,
      submitProduct,
    };
  },

  mounted() {
    this.$store.dispatch('fetchIngredients');
  },
};
</script>

<style scoped>
/* Add any scoped styles here */
</style>
