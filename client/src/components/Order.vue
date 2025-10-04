<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const orders = ref([])
const users = ref([])
const products = ref([]) // для списка продуктов
const statusFilter = ref('')
const dateFilter = ref('')
const userFilter = ref('')
const selectedOrder = ref(null)

const newOrderItems = ref([{ product_id: null, quantity: 1 }])
const currentUser = ref(null)  // текущий пользователь

const getStatusDisplay = (status) => {
  const statuses = {
    pending: 'Ожидает',
    preparing: 'Готовится',
    ready: 'Готов',
    cancelled: 'Отменен'
  }
  return statuses[status] || status
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    preparing: 'info',
    ready: 'success',
    cancelled: 'danger'
  }
  return colors[status]
}

async function loadCurrentUser() {
  const res = await axios.get('/api/profiles/me/') // предполагается эндпоинт, возвращающий профиль текущего пользователя
  currentUser.value = res.data
}

async function loadProducts() {
  const res = await axios.get('/api/products/')
  products.value = res.data
}

async function loadOrders() {
  const res = await axios.get('/api/orders/')
  orders.value = res.data
}

onMounted(() => {
  loadProducts()
  loadOrders()
  loadCurrentUser()
})


async function createOrder() {
  if (!currentUser.value) {
    alert("Пользователь не определён")
    return
  }

  try {
    const orderData = {
      user: currentUser.value.id,  // текущий пользователь
      status: 'pending',
      items: newOrderItems.value.map(item => ({
        product: item.product_id,
        quantity: item.quantity,
        price_at_time_of_order: 0  // либо ценой с бекенда, если нужно
      }))
    }

    const res = await axios.post('/api/orders/', orderData)
    orders.value.push(res.data)
    // сброс формы
    newOrderItems.value = [{ product_id: null, quantity: 1 }]
  } catch(e) {
    alert('Ошибка при создании заказа')
  }
}
</script>

<template>
  <!-- Ваша текущая разметка заказов -->

  <!-- Форма создания заказа -->
  <div class="card mt-4 p-4">
    <h3>Создать новый заказ</h3>

    <div v-for="(item, index) in newOrderItems" :key="index" class="mb-3 row g-2 align-items-center">
      <div class="col">
        <select class="form-select" v-model="item.product_id" required>
          <option :value="null" disabled>Выберите продукт</option>
          <option v-for="product in products" :key="product.id" :value="product.id">
            {{ product.name }} - {{ product.price }} руб.
          </option>
        </select>
      </div>
      <div class="col-2">
        <input type="number" v-model.number="item.quantity" min="1" class="form-control" />
      </div>
      <div class="col-auto">
        <button class="btn btn-danger" @click="newOrderItems.splice(index, 1)" type="button">Удалить</button>
      </div>
    </div>

    <button class="btn btn-secondary mb-3" @click="newOrderItems.push({ product_id: null, quantity: 1 })" type="button">
      Добавить позицию
    </button>
    <br />
    <button class="btn btn-primary" @click="createOrder">Создать заказ</button>
  </div>
</template>
