<template>
  <div>
    <h2>Управление профилями пользователей</h2>
    
    <div class="mb-4">
      <div class="row g-3">
        <div class="col-md-4">
          <input type="text" class="form-control" v-model="searchQuery" placeholder="Поиск пользователей..." />
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="roleFilter">
            <option value="">Все роли</option>
            <option value="customer">Клиент</option>
            <option value="barista">Бариста</option>
            <option value="admin">Администратор</option>
          </select>
        </div>
      </div>
    </div>

    <div class="list-group">
      <div v-for="profile in filteredProfiles" :key="profile.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ profile.user.username }}</strong> - 
            {{ getRoleDisplay(profile.role) }}
            <br>
            <small class="text-muted">{{ profile.user.email }} | {{ profile.phone_number || 'Нет телефона' }}</small>
          </div>
          <div>
            <button class="btn btn-sm btn-outline-warning me-2" @click="onProfileEditClick(profile)">
              ✏️
            </button>
            <button class="btn btn-sm btn-outline-info" @click="onViewUserOrders(profile.user.id)">
              📋 Заказы
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div class="modal fade" id="editProfileModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать профиль</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" :value="profileToEdit.user?.username" disabled />
                  <label>Имя пользователя</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="email" class="form-control" :value="profileToEdit.user?.email" disabled />
                  <label>Email</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="profileToEdit.role">
                    <option value="customer">Клиент</option>
                    <option value="barista">Бариста</option>
                    <option value="admin">Администратор</option>
                  </select>
                  <label>Роль</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="tel" class="form-control" v-model="profileToEdit.phone_number" 
                         placeholder="Номер телефона" />
                  <label>Номер телефона</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" @click="onProfileUpdate" data-bs-dismiss="modal">
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
import { useRouter } from 'vue-router'

const router = useRouter()
const profiles = ref([])
const searchQuery = ref('')
const roleFilter = ref('')
const profileToEdit = ref({ id: null, user: {}, role: '', phone_number: '' })

const getRoleDisplay = (role) => {
  const roles = { customer: 'Клиент', barista: 'Бариста', admin: 'Администратор' }
  return roles[role] || role
}

const filteredProfiles = computed(() => {
  return profiles.value.filter(profile => {
    const matchesSearch = profile.user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         profile.user.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         (profile.phone_number && profile.phone_number.includes(searchQuery.value))
    const matchesRole = !roleFilter.value || profile.role === roleFilter.value
    return matchesSearch && matchesRole
  })
})

const fetchProfiles = async () => {
  const response = await axios.get('/api/profiles/')
  profiles.value = response.data
}

const onProfileEditClick = (profile) => {
  profileToEdit.value = { ...profile }
  new bootstrap.Modal(document.getElementById('editProfileModal')).show()
}

const onProfileUpdate = async () => {
  await axios.put(`/api/profiles/${profileToEdit.value.id}/`, {
    role: profileToEdit.value.role,
    phone_number: profileToEdit.value.phone_number
  })
  await fetchProfiles()
}

const onViewUserOrders = (userId) => {
  router.push({ path: '/orders', query: { user_id: userId } })
}

onMounted(fetchProfiles)
</script>