<script setup>
import { onMounted } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onMounted(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    
    <div class="container">
      <div>
      <ul class="navbar-nav">
        <li calss="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Пользователь
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="/admin">Админ</a></li>
          </ul>
        </li>
      </ul>
    </div>
      <router-link to="/" class="navbar-brand">Кофейня</router-link>
      <div class="navbar-nav">
        <router-link to="/categories" class="nav-link">Категории</router-link>
        <router-link to="/products" class="nav-link">Продукты</router-link>
        <router-link to="/ingredients" class="nav-link">Ингредиенты</router-link>
        <router-link to="/profiles" class="nav-link">Профили</router-link>
        <router-link to="/orders" class="nav-link">Заказы</router-link>
      </div>
    </div>
  </nav>

    <div class="container mt-4">
      <router-view></router-view>
    </div>
  
</template>

<style scoped></style>
