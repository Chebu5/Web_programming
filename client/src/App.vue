<script setup>
import axios from "axios";
import { onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import {computed,ref} from "vue";

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})
const productToAdd = ref({});

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
async function onLoadClick() {
    await fetchProducts()
}
onBeforeMount(async()=>{
    await fetchProducts();
    await fetchCategories();
})
async function onProductAdd() {
  await axios.post("/api/products/", {
    ...productToAdd.value,
  });
  await fetchProducts();
}
async function onRemoveClick(products) {
  await axios.delete(`/api/products/${products.id}/`);
  await fetchProducts(); // переподтягиваю
}
</script>

<template>
  <form @submit.prevent.stop="onProductAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
        <input
          type="text"
          class="form-control"
          v-model="productToAdd.name"
          required
        />
        <label for="floatingInput">Название</label>
      </div>
    </div>
    <div class="col-auto">
        <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
      <div class="form-floating">
        <select class="form-select" v-model="productToAdd.category" required>
          <option :value="g.id" v-for="g in categories">{{ g.name }}</option>
        </select>
        <label for="floatingInput">Группа</label>
      </div>
    </div>
    <div class="col-auto">
        <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
      <div class="form-floating">
        <input
          type="number"
          class="form-control"
          v-model="productToAdd.price"
          required
        />
        <label for="floatingInput">Цена</label>
      </div>
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
    
  </div>
  <div v-for="item in products" class="student-item">
  <div>{{ item.name }}</div>
  <button class="btn btn-danger" @click="onRemoveClick(item)">
    <i class="bi bi-x"></i>
  </button>
</div>
</form>
   <div>
    <div v-for="item in products">
        {{ item.name }}
    </div>
    <button @click = "onLoadClick">Вывести</button>
  </div> 
</template>

<style scoped></style>
