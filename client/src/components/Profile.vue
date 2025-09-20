<template>
<form @submit.prevent="onProfileAdd">
    <div class="row align-items-end mb-4">
      <div class="col-auto">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="profileName"
            v-model="profileAdd.name"
            placeholder="Имя"
            required
          />
          <label for="profileName">Имя</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="profileLastName"
            v-model="profileAdd.last_name"
            placeholder="Фамилия"
            required
          />
          <label for="profileLastName">Фамилия</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <input
            type="tel"
            class="form-control"
            id="profilePhone"
            v-model.number="profileAdd.phone_number"
            placeholder="Телефон"
            required
          />
          <label for="profilePhone">Телефон</label>
        </div>
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary h-100">
          Добавить покупателя
        </button>
      </div>
    </div>
  </form>

  <!-- Список продуктов -->
  <div class="products-list">
    <div v-for="profile in profiles" :key="profile.id" class="product-item d-flex align-items-center justify-content-between p-3 mb-2 border rounded">
      <div class="product-info flex-grow-1">
        <div class="fw-bold">{{ profile.name }} {{ profile.last_name }}</div>
      </div>
      <div class="product-actions ms-3">
        <button
          class="btn btn-sm btn-outline-success me-2"
          @click="onProfileEditClick(profile)"
          data-bs-toggle="modal"
          data-bs-target="#editProfileModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button 
          class="btn btn-sm btn-outline-danger" 
          @click="onRemoveClick(profile)"
        >
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Модальное окно редактирования -->
  <div class="modal fade" id="editProfileModal" tabindex="-1">
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
                  id="editProfileName"
                  v-model="profileToEdit.name"
                  placeholder="Имя пользователя"
                />
                <label for="editProfiletName">Имя</label>
              </div>
            </div>
            <div class="col-12">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  id="editProfileLastName"
                  v-model="profileToEdit.last_name"
                  placeholder="Фамилия пользователя"
                />
                <label for="editProfileLastName">Фамилия</label>
              </div>
            </div>
            <div class="col-12">
              <div class="form-floating">
                <input
                  type="tel"
                  class="form-control"
                  id="editProfilePhoneNumber"
                  v-model.number="profileToEdit.phone_number"
                  placeholder="Телефон"
                  min="0"
                />
                <label for="editProfilePhoneNumber">Телефон</label>
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
            @click="onProfileUpdate"
            data-bs-dismiss="modal"
          >
            Сохранить
          </button>
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
const profileToEdit = ref({})
const profileAdd = ref({})
const fetchProfiles = async () => {
  const response = await axios.get('/api/profiles/')
  profiles.value = response.data
}
const onProfileAdd = async () =>{
  await axios.post('/api/profiles/',{
    ...profileAdd.value,
  })
}
const onProfileEditClick = (profile) => {
  profileToEdit.value = { ...profile }
  new bootstrap.Modal(document.getElementById('editProfileModal')).show()
}
const onRemoveClick = async (profile) =>{
  await axios.delete(`/api/profiles/${profile.id}/`)
  await fetchProfiles()
}
const onProfileUpdate = async () => {
  await axios.put(`/api/profiles/${profileToEdit.value.id}/`, {
    name:profileToEdit.value.name,
    last_name:profileToEdit.value.last_name,
    phone_number: profileToEdit.value.phone_number
  })
  await fetchProfiles()
}
onMounted(fetchProfiles)
</script>