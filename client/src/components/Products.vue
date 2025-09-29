<script setup>
import axios from "axios";
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import {computed,ref} from "vue";
import { useRouter } from 'vue-router'

const router = useRouter()
onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})
const productToAdd = ref({});
const productToEdit = ref({});
const productsPictureRef = ref();
const productAddImageUrl = ref();
async function fetchProducts() {
    //loading.value = true;
    const r = await axios.get("api/products");
    console.log(r.data)
    products.value = r.data;
    //loading.value = false;
}
async function fetchCategories() {
    const response = await axios.get("api/categories"); // Предполагаемый endpoint
    categories.value = response.data;
}
const products = ref([])
const categories = ref([]);

onBeforeMount(async()=>{
    await fetchProducts();
    await fetchCategories();
})
async function onProductAdd() {
  const formData = new FormData();
  formData.append('picture',productsPictureRef.value.files[0]);
  formData.set('name',productToAdd.value.name)
  formData.set('category',productToAdd.value.category)
  formData.set('price',productToAdd.value.price)
  await axios.post("/api/products/",formData, {
    headers:{
      'Content-Type':'multipart/form-data'
    }
  });
  await fetchProducts();
}
async function productAddPictureChange() {
  productAddImageUrl.value = URL.createObjectURL(productsPictureRef.value.files[0])
}
const newPictureFile = ref(null); // выбранный файл для замены картинки

function onEditPictureChange(event) {
  const file = event.target.files[0];
  newPictureFile.value = file;
}
async function onProductEditClick(products) {
  productToEdit.value = { ...products };
}
async function onRemoveClick(products) {
  await axios.delete(`/api/products/${products.id}/`);
  await fetchProducts(); // переподтягиваю
}
async function onUpdateProduct() {
  const formData = new FormData();
  formData.set('name', productToEdit.value.name);
  formData.set('category', productToEdit.value.category);
  formData.set('price', productToEdit.value.price);

  if (newPictureFile.value) {
    formData.append('picture', newPictureFile.value);
  }

  await axios.put(`/api/products/${productToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  newPictureFile.value = null; // очистить выбранный файл после обновления
  await fetchProducts();
}

</script>

<template>
  <form @submit.prevent="onProductAdd">
    <div class="row align-items-end mb-4">
      <div class="col">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="productName"
            v-model="productToAdd.name"
            placeholder="Название продукта"
            required
          />
          <label for="productName">Название</label>
        </div>
      </div>
      <div class="col-auto">
        <input class="form-control" type="file" ref="productsPictureRef" @change="productAddPictureChange"></input>
      </div>
      <div class="col-auto">
        <img :src="productAddImageUrl" style="max-height: 60px;" alt=""></img>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <select 
            class="form-select" 
            id="productCategory"
            v-model="productToAdd.category" 
            required
          >
            <option value="" disabled>Выберите категорию</option>
            <option :value="category.id" v-for="category in categories" :key="category.id">
              {{ category.name }}
            </option>
          </select>
          <label for="productCategory">Категория</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <input
            type="number"
            class="form-control"
            id="productPrice"
            v-model.number="productToAdd.price"
            placeholder="Цена"
            min="0"
            required
          />
          <label for="productPrice">Цена</label>
        </div>
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary h-100">
          Добавить продукт
        </button>
      </div>
    </div>
  </form>

  <!-- Список продуктов -->
  <div class="products-list">
    <div v-for="product in products" :key="product.id" class="product-item d-flex align-items-center justify-content-between p-3 mb-2 border rounded">
      <div class="product-info flex-grow-1">
        <div class="fw-bold">{{ product.name }}</div>
        <div class="fw-bold">{{ product.price }} - руб</div>
        <div v-show="product.picture"><img :src="product.picture" style="max-height: 60px;"></div>
      </div>
      <div class="product-actions ms-3">
        <button
          class="btn btn-sm btn-outline-success me-2"
          @click="onProductEditClick(product)"
          data-bs-toggle="modal"
          data-bs-target="#editProductModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button 
          class="btn btn-sm btn-outline-danger" 
          @click="onRemoveClick(product)"
        >
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Модальное окно редактирования -->
  <div class="modal fade" id="editProductModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать продукт</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  id="editProductName"
                  v-model="productToEdit.name"
                  placeholder="Название продукта"
                />
                <label for="editProductName">Название</label>
              </div>
            </div>
            <div class="col-12">
              <div class="form-floating">
                <input
                  type="file"
                  class="form-control"
                  id="editProductImage"
                  ref="productsPictureEditRef"
                  @change="onEditPictureChange"
                />
                <label for="editProductImage">Картинка</label>

              </div>
            </div>
            <div class="col-12">
              <div class="form-floating">
                <select class="form-select" id="editProductCategory" v-model="productToEdit.category">
                  <option :value="category.id" v-for="category in categories" :key="category.id">
                    {{ category.name }}
                  </option>
                </select>
                <label for="editProductCategory">Категория</label>
              </div>
            </div>
            <div class="col-12">
              <div class="form-floating">
                <input
                  type="number"
                  class="form-control"
                  id="editProductPrice"
                  v-model.number="productToEdit.price"
                  placeholder="Цена"
                  min="0"
                />
                <label for="editProductPrice">Цена</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Отмена
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="onUpdateProduct"
            data-bs-dismiss="modal"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
