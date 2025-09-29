<script setup>
import axios from "axios";
import { onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const ingredients = ref([]);
const ingredientToAdd = ref({ name: '', unit: 'g', current_stock: 0, min_stock_threshold: 0 });
const ingredientToEdit = ref({ id: null, name: '', unit: 'g', current_stock: 0, min_stock_threshold: 0 });

const ingredientsPictureRef = ref(null);          // Для добавления картинки
const ingredientsPictureEditRef = ref(null);      // Для редактирования картинки
const newPictureFile = ref(null);                   // Для новой картинки при редактировании
const ingredientAddImageUrl = ref(null);            // Превью картинки при добавлении

async function fetchIngredients() {
  const response = await axios.get("/api/ingredients/");
  ingredients.value = response.data.map(i => ({
    ...i,
    is_low_stock: i.current_stock <= i.min_stock_threshold
  }));
}

onBeforeMount(async () => {
  await fetchIngredients();
});

function ingredientAddPictureChange() {
  if (ingredientsPictureRef.value && ingredientsPictureRef.value.files.length > 0) {
    ingredientAddImageUrl.value = URL.createObjectURL(ingredientsPictureRef.value.files[0]);
  }
}

function onEditPictureChange(event) {
  const file = event.target.files[0];
  newPictureFile.value = file;
}

async function onIngredientAdd() {
  const formData = new FormData();
  if (ingredientsPictureRef.value && ingredientsPictureRef.value.files.length > 0) {
    formData.append('picture', ingredientsPictureRef.value.files[0]);
  }
  formData.set('name', ingredientToAdd.value.name);
  formData.set('unit', ingredientToAdd.value.unit);
  formData.set('current_stock', ingredientToAdd.value.current_stock);
  formData.set('min_stock_threshold', ingredientToAdd.value.min_stock_threshold);

  await axios.post("/api/ingredients/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  await fetchIngredients();
  ingredientToAdd.value = { name: '', unit: 'g', current_stock: 0, min_stock_threshold: 0 };
  ingredientAddImageUrl.value = null;
  if (ingredientsPictureRef.value) ingredientsPictureRef.value.value = null;
}

function onIngredientEditClick(ingredient) {
  ingredientToEdit.value = { ...ingredient };
  newPictureFile.value = null;
  if (ingredientsPictureEditRef.value) {
    ingredientsPictureEditRef.value.value = null;
  }
}

async function onRemoveClick(ingredient) {
  await axios.delete(`/api/ingredients/${ingredient.id}/`);
  await fetchIngredients();
}

async function onUpdateIngredient() {
  const formData = new FormData();
  formData.set('name', ingredientToEdit.value.name);
  formData.set('unit', ingredientToEdit.value.unit);
  formData.set('current_stock', ingredientToEdit.value.current_stock);
  formData.set('min_stock_threshold', ingredientToEdit.value.min_stock_threshold);

  if (newPictureFile.value) {
    formData.append('picture', newPictureFile.value);
  }

  await axios.put(`/api/ingredients/${ingredientToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  newPictureFile.value = null;
  await fetchIngredients();
}
</script>

<template>
  <div>
    <h2>Управление ингредиентами</h2>

    <form @submit.prevent="onIngredientAdd" class="mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="ingredientToAdd.name" placeholder="Название" required />
            <label>Название</label>
          </div>
        </div>
        <div class="col-auto">
          <input class="form-control" type="file" ref="ingredientsPictureRef" @change="ingredientAddPictureChange" />
        </div>
        <div class="col-auto">
          <img :src="ingredientAddImageUrl" style="max-height: 60px;" alt="" />
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
            <input type="number" step="0.001" class="form-control" v-model.number="ingredientToAdd.current_stock" placeholder="Запас" />
            <label>Запас</label>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-floating">
            <input type="number" step="0.001" class="form-control" v-model.number="ingredientToAdd.min_stock_threshold" placeholder="Мин. запас" />
            <label>Мин. запас</label>
          </div>
        </div>
        <div class="col-md-3">
          <button type="submit" class="btn btn-primary h-100">Добавить</button>
        </div>
      </div>
    </form>

    <div class="list-group">
      <div v-for="ingredient in ingredients" :key="ingredient.id" :class="['list-group-item', { 'list-group-item-warning': ingredient.is_low_stock }]">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ ingredient.name }}</strong> - {{ ingredient.current_stock }} {{ ingredient.unit }}
            <span v-if="ingredient.is_low_stock" class="badge bg-danger">Мало!</span>
            <div v-if="ingredient.picture"><img :src="ingredient.picture" style="max-height: 60px;" /></div>
          </div>
          <div>
            <button class="btn btn-sm btn-outline-warning me-2" data-bs-toggle="modal" data-bs-target="#editIngredientModal" @click="onIngredientEditClick(ingredient)">
              ✏️
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="onRemoveClick(ingredient)">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Модальное окно редактирования -->
  <div class="modal fade" id="editIngredientModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать ингредиент</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12 mb-3">
              <input type="text" class="form-control" v-model="ingredientToEdit.name" placeholder="Название ингредиента" />
            </div>
            <div class="col-12 mb-3">
              <input type="file" class="form-control" ref="ingredientsPictureEditRef" @change="onEditPictureChange" />
            </div>
            <div class="col-12 mb-3">
              <select class="form-select" v-model="ingredientToEdit.unit">
                <option value="kg">кг</option>
                <option value="g">г</option>
                <option value="l">л</option>
                <option value="ml">мл</option>
                <option value="pcs">шт</option>
              </select>
            </div>
            <div class="col-12 mb-3">
              <input type="number" class="form-control" v-model.number="ingredientToEdit.current_stock" placeholder="Текущий запас" />
            </div>
            <div class="col-12 mb-3">
              <input type="number" class="form-control" v-model.number="ingredientToEdit.min_stock_threshold" placeholder="Минимальный порог запаса" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
          <button type="button" class="btn btn-primary" @click="onUpdateIngredient" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
