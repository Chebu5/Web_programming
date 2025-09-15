<template>
  <div>
    <h2>Управление категориями</h2>
    
    <!-- Форма добавления -->
    <form @submit.prevent="onCategoryAdd" class="mb-4">
      <div class="row align-items-end">
        <div class="col">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="categoryToAdd.name"
              placeholder="Название категории"
              required
            />
            <label>Название категории</label>
          </div>
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <!-- Список категорий -->
    <div class="list-group">
      <div v-for="category in categories" :key="category.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ category.name }}</span>
        <div>
          <button class="btn btn-sm btn-outline-warning me-2" @click="onCategoryEditClick(category)">
            ✏️
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="onCategoryDelete(category)">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div class="modal fade" id="editCategoryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать категорию</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="categoryToEdit.name"
                placeholder="Название категории"
              />
              <label>Название категории</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" @click="onCategoryUpdate" data-bs-dismiss="modal">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const categories = ref([])
const categoryToAdd = ref({ name: '' })
const categoryToEdit = ref({ id: null, name: '' })

const fetchCategories = async () => {
  const response = await axios.get('/api/categories/')
  categories.value = response.data
}

const onCategoryAdd = async () => {
  await axios.post('/api/categories/', categoryToAdd.value)
  categoryToAdd.value = { name: '' }
  await fetchCategories()
}

const onCategoryEditClick = (category) => {
  categoryToEdit.value = { ...category }
  new bootstrap.Modal(document.getElementById('editCategoryModal')).show()
}

const onCategoryUpdate = async () => {
  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, categoryToEdit.value)
  await fetchCategories()
}

const onCategoryDelete = async (category) => {
  if (confirm(`Удалить категорию "${category.name}"?`)) {
    await axios.delete(`/api/categories/${category.id}/`)
    await fetchCategories()
  }
}

onMounted(fetchCategories)
</script>