<template>
  <div>
    <h2>Управление ингредиентами</h2>
    
    <form @submit.prevent="onIngredientAdd" class="mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="ingredientToAdd.name" required />
            <label>Название</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <select class="form-select" v-model="ingredientToAdd.unit" required>
              <option value="kg">кг</option>
              <option value="g">г</option>
              <option value="l">л</option>
              <option value="ml">мл</option>
              <option value="pcs">шт</option>
            </select>
            <label>Единица</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input type="number" class="form-control" v-model.number="ingredientToAdd.current_stock" step="0.001" />
            <label>Запас</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input type="number" class="form-control" v-model.number="ingredientToAdd.min_stock_threshold" step="0.001" />
            <label>Мин. запас</label>
          </div>
        </div>
        <div class="col-md-3">
          <button type="submit" class="btn btn-primary h-100">Добавить</button>
        </div>
      </div>
    </form>

    <div class="list-group">
      <div v-for="ingredient in ingredients" :key="ingredient.id" 
           :class="['list-group-item', { 'list-group-item-warning': ingredient.is_low_stock }]">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ ingredient.name }}</strong> - 
            {{ ingredient.current_stock }} {{ getUnitDisplay(ingredient.unit) }}
            <span v-if="ingredient.is_low_stock" class="badge bg-danger">Мало!</span>
          </div>
          <div>
            <button class="btn btn-sm btn-outline-warning me-2" @click="onIngredientEditClick(ingredient)">
              ✏️
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="onIngredientDelete(ingredient)">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <!-- Аналогично другим компонентам -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const ingredients = ref([])
const ingredientToAdd = ref({ name: '', unit: 'g', current_stock: 0, min_stock_threshold: 0 })
const ingredientToEdit = ref({ id: null, name: '', unit: 'g', current_stock: 0, min_stock_threshold: 0 })

const getUnitDisplay = (unit) => {
  const units = { kg: 'кг', g: 'г', l: 'л', ml: 'мл', pcs: 'шт' }
  return units[unit] || unit
}

const fetchIngredients = async () => {
  const response = await axios.get('/api/ingredients/')
  ingredients.value = response.data.map(ingredient => ({
    ...ingredient,
    is_low_stock: ingredient.current_stock <= ingredient.min_stock_threshold
  }))
}

// Остальные методы аналогично CategoryManager
// onIngredientAdd, onIngredientEditClick, onIngredientUpdate, onIngredientDelete

onMounted(fetchIngredients)
</script>