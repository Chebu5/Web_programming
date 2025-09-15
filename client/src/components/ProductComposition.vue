<template>
  <div>
    <h2>Управление составом продуктов</h2>
    
    <form @submit.prevent="onCompositionAdd" class="mb-4">
      <div class="row g-3 align-items-end">
        <div class="col-md-4">
          <div class="form-floating">
            <select class="form-select" v-model="compositionToAdd.product" required>
              <option value="" disabled>Выберите продукт</option>
              <option :value="product.id" v-for="product in products" :key="product.id">
                {{ product.name }}
              </option>
            </select>
            <label>Продукт</label>
          </div>
        </div>
        <div class="col-md-4">
          <div class="form-floating">
            <select class="form-select" v-model="compositionToAdd.ingredient" required>
              <option value="" disabled>Выберите ингредиент</option>
              <option :value="ingredient.id" v-for="ingredient in ingredients" :key="ingredient.id">
                {{ ingredient.name }}
              </option>
            </select>
            <label>Ингредиент</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input type="number" class="form-control" v-model.number="compositionToAdd.ingredient_amount" 
                   step="0.001" min="0" required />
            <label>Количество</label>
          </div>
        </div>
        <div class="col-md-2">
          <button type="submit" class="btn btn-primary h-100">Добавить</button>
        </div>
      </div>
    </form>

    <div class="list-group">
      <div v-for="composition in compositions" :key="composition.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ getProductName(composition.product) }}</strong> - 
            {{ getIngredientName(composition.ingredient) }}: 
            {{ composition.ingredient_amount }} {{ getIngredientUnit(composition.ingredient) }}
          </div>
          <div>
            <button class="btn btn-sm btn-outline-warning me-2" @click="onCompositionEditClick(composition)">
              ✏️
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="onCompositionDelete(composition)">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div class="modal fade" id="editCompositionModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать состав</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="compositionToEdit.product" disabled>
                    <option :value="compositionToEdit.product">
                      {{ getProductName(compositionToEdit.product) }}
                    </option>
                  </select>
                  <label>Продукт</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="compositionToEdit.ingredient" disabled>
                    <option :value="compositionToEdit.ingredient">
                      {{ getIngredientName(compositionToEdit.ingredient) }}
                    </option>
                  </select>
                  <label>Ингредиент</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model.number="compositionToEdit.ingredient_amount" 
                         step="0.001" min="0" required />
                  <label>Количество</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" @click="onCompositionUpdate" data-bs-dismiss="modal">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const compositions = ref([])
const products = ref([])
const ingredients = ref([])
const compositionToAdd = ref({ product: '', ingredient: '', ingredient_amount: 0 })
const compositionToEdit = ref({ id: null, product: '', ingredient: '', ingredient_amount: 0 })

const productsById = computed(() => products.value.reduce((acc, product) => {
  acc[product.id] = product
  return acc
}, {}))

const ingredientsById = computed(() => ingredients.value.reduce((acc, ingredient) => {
  acc[ingredient.id] = ingredient
  return acc
}, {}))

const getProductName = (productId) => productsById.value[productId]?.name || 'Неизвестно'
const getIngredientName = (ingredientId) => ingredientsById.value[ingredientId]?.name || 'Неизвестно'
const getIngredientUnit = (ingredientId) => {
  const unit = ingredientsById.value[ingredientId]?.unit
  const units = { kg: 'кг', g: 'г', l: 'л', ml: 'мл', pcs: 'шт' }
  return units[unit] || unit
}

const fetchCompositions = async () => {
  const response = await axios.get('/api/product-compositions/')
  compositions.value = response.data
}

const fetchProducts = async () => {
  const response = await axios.get('/api/products/')
  products.value = response.data
}

const fetchIngredients = async () => {
  const response = await axios.get('/api/ingredients/')
  ingredients.value = response.data
}

const onCompositionAdd = async () => {
  await axios.post('/api/product-compositions/', compositionToAdd.value)
  compositionToAdd.value = { product: '', ingredient: '', ingredient_amount: 0 }
  await fetchCompositions()
}

const onCompositionEditClick = (composition) => {
  compositionToEdit.value = { ...composition }
  new bootstrap.Modal(document.getElementById('editCompositionModal')).show()
}

const onCompositionUpdate = async () => {
  await axios.put(`/api/product-compositions/${compositionToEdit.value.id}/`, compositionToEdit.value)
  await fetchCompositions()
}

const onCompositionDelete = async (composition) => {
  if (confirm('Удалить этот состав?')) {
    await axios.delete(`/api/product-compositions/${composition.id}/`)
    await fetchCompositions()
  }
}

onMounted(async () => {
  await Promise.all([fetchCompositions(), fetchProducts(), fetchIngredients()])
})
</script>