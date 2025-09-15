<template>
  <div>
    <h2>Управление заказами</h2>
    
    <div class="mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <select class="form-select" v-model="statusFilter">
            <option value="">Все статусы</option>
            <option value="pending">Ожидает</option>
            <option value="preparing">Готовится</option>
            <option value="ready">Готов</option>
            <option value="cancelled">Отменен</option>
          </select>
        </div>
        <div class="col-md-3">
          <input type="date" class="form-control" v-model="dateFilter" />
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="userFilter">
            <option value="">Все пользователи</option>
            <option :value="user.id" v-for="user in users" :key="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="list-group">
      <div v-for="order in filteredOrders" :key="order.id" 
           :class="['list-group-item', `list-group-item-${getStatusColor(order.status)}`]">
        <div class="d-flex justify-content-between align-items-start">
          <div>
            <strong>Заказ #{{ order.id }}</strong> - 
            {{ getStatusDisplay(order.status) }}
            <br>
            <small class="text-muted">
              Пользователь: {{ getUserName(order.user) }} | 
              Сумма: {{ order.total_amount }} руб. |
              {{ formatDate(order.created_at) }}
            </small>
            <div v-if="order.items && order.items.length > 0" class="mt-2">
              <small>
                <strong>Состав:</strong>
                <span v-for="(item, index) in order.items" :key="item.id">
                  {{ item.product.name }} ×{{ item.quantity }}{{ index < order.items.length - 1 ? ', ' : '' }}
                </span>
              </small>
            </div>
          </div>
          <div class="btn-group">
            <select class="form-select form-select-sm" v-model="order.status" 
                    @change="onOrderStatusChange(order)">
              <option value="pending">Ожидает</option>
              <option value="preparing">Готовится</option>
              <option value="ready">Готов</option>
              <option value="cancelled">Отменен</option>
            </select>
            <button class="btn btn-sm btn-outline-info" @click="onViewOrderDetails(order)">
              👁️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно деталей заказа -->
    <div class="modal fade" id="orderDetailsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Детали заказа #{{ selectedOrder?.id }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedOrder">
              <p><strong>Статус:</strong> {{ getStatusDisplay(selectedOrder.status) }}</p>
              <p><strong>Пользователь:</strong> {{ getUserName(selectedOrder.user) }}</p>
              <p><strong>Общая сумма:</strong> {{ selectedOrder.total_amount }} руб.</p>
              <p><strong>Дата создания:</strong> {{ formatDate(selectedOrder.created_at) }}</p>
              
              <h6>Позиции заказа:</h6>
              <ul class="list-group">
                <li v-for="item in selectedOrder.items" :key="item.id" class="list-group-item">
                  {{ item.product.name }} - {{ item.quantity }} × {{ item.price_at_time_of_order }} руб. = 
                  {{ item.quantity * item.price_at_time_of_order }} руб.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const orders = ref([])
const users = ref([])
const statusFilter = ref('')
const dateFilter = ref('')
const userFilter = ref('')
const selectedOrder = ref(null)

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
</script>