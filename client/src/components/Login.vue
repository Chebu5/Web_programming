<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const router = useRouter()

async function login() {
  errorMessage.value = ''
  try {
    const response = await axios.post('/api/token/', {
      username: username.value,
      password: password.value
    })

    // Сохраняем токен в localStorage или в другом безопасном месте
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // Устанавливаем Authorization заголовок для axios
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access

    // Перенаправляем пользователя после успешного входа
    router.push('/')
    
  } catch (error) {
    errorMessage.value = 'Ошибка входа: неверный логин или пароль'
  }
}
</script>

<template>
  <div class="login-container">
    <h2>Авторизация</h2>
    <input v-model="username" placeholder="Логин" />
    <input type="password" v-model="password" placeholder="Пароль" />
    <button @click="login">Войти</button>
    <p v-if="errorMessage" style="color:red;">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
}
.login-container input {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
}
.login-container button {
  padding: 8px;
}
</style>
