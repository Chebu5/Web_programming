import { createRouter, createWebHistory } from 'vue-router'
import CategoryManager from '@/components/Category.vue'
import ProductManager from '@/components/Products.vue'
import IngredientManager from '@/components/Ingredient.vue'
import ProductCompositionManager from '@/components/ProductComposition.vue'
import ProfileManager from '@/components/Profile.vue'
import OrderManager from '@/components/Order.vue'
import OrderItemManager from '@/components/OrderItem.vue'
import LoginManager from '@/components/Login.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', component: LoginManager, name: 'login' },
    {
    path: '/categories',
    name: 'Categories',
    component: CategoryManager
  },
  {
    path: '/products',
    name: 'Products',
    component: ProductManager
  },
  {
    path: '/ingredients',
    name: 'Ingredients',
    component: IngredientManager
  },
  {
    path: '/compositions',
    name: 'Compositions',
    component: ProductCompositionManager
  },
  {
    path: '/profiles',
    name: 'Profiles',
    component: ProfileManager
  },
  {
    path: '/orders',
    name: 'Orders',
    component: OrderManager
  },
  {
    path: '/order-items',
    name: 'OrderItems',
    component: OrderItemManager
  }],
})

export default router
