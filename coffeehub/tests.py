from django.test import TestCase
from rest_framework.test import APIClient
from coffeehub.models import Category, Product, Ingredient, ProductComposition, Profile, Order, OrderItem
from decimal import Decimal
from model_bakery import baker

class CategoryViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        category = Category.objects.create(name="Кофе")
        r = self.client.get('/api/categories/')
        data = r.json()
        assert category.name == data[0]['name']
        assert category.id == data[0]['id']
        assert len(data) == 1
    def test_create_category(self):
        r = self.client.post("/api/categories/", {
            "name": "Чай"
        }, format='json')
        new_category_id = r.json()['id']
        categories = Category.objects.all()
        assert len(categories) == 1
        new_category = Category.objects.filter(id=new_category_id).first()
        assert new_category.name == 'Чай'
    def test_delete_category(self):
        categories = baker.make("Category", 5)
        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 5
        category_id_to_delete = categories[2].id
        self.client.delete(f'/api/categories/{category_id_to_delete}/')
        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 4
        assert category_id_to_delete not in [i['id'] for i in data]
    def test_update_category(self):
        category = baker.make("Category")
        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == category.name
        r = self.client.put(f'/api/categories/{category.id}/', {
            "name": "Десерты"
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == "Десерты"
        category.refresh_from_db()
        assert category.name == "Десерты"

class ProductViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        category = Category.objects.create(name="Кофе")
        product = Product.objects.create(name="Американо", price=200, is_available=1, category=category)
        r = self.client.get('/api/products/')
        data = r.json()
        assert product.name == data[0]['name']
        assert product.id == data[0]['id']
        assert product.price == data[0]['price']
        assert product.is_available == data[0]['is_available']
        assert product.category.id == data[0]['category']
        assert len(data) == 1
    def test_create_product(self):
        category = baker.make("coffeehub.Category")
        r = self.client.post("/api/products/", {
            "name": "Латте",
            "price": 200,
            "category": category.id,
            "is_available": 1
        }, format='json')
        new_product_id = r.json()['id']
        products = Product.objects.all()
        assert len(products) == 1
        new_product = Product.objects.filter(id=new_product_id).first()
        assert new_product.name == 'Латте'
        assert new_product.category == category
        assert new_product.is_available == 1
        assert new_product.price == 200
    def test_delete_product(self):
        products = baker.make("Product", 10)
        r = self.client.get('/api/products/')
        data = r.json()
        assert len(data) == 10
        product_id_to_delete = products[3].id
        self.client.delete(f'/api/products/{product_id_to_delete}/')
        r = self.client.get('/api/products/')
        data = r.json()
        assert len(data) == 9
        assert product_id_to_delete not in [i['id'] for i in data]
    def test_update_product(self):
        products = baker.make("Product", 10)
        product = products[2]
        r = self.client.get(f'/api/products/{product.id}/')
        data = r.json()
        assert data['name'] == product.name
        r = self.client.put(f'/api/products/{product.id}/', {
            "name": "Капучино",
            "price": product.price,
            "category": product.category.id if product.category else None,
            "is_available": product.is_available,
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/products/{product.id}/')
        data = r.json()
        assert data['name'] == "Капучино"
        product.refresh_from_db()
        assert data['name'] == product.name

class IngredientViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        ingredient = Ingredient.objects.create(
            name="Молоко",
            unit="l",
            current_stock=Decimal('10.000'),
            min_stock_threshold=Decimal('2.000')
        )
        r = self.client.get('/api/ingredients/')
        data = r.json()
        assert ingredient.name == data[0]['name']
        assert ingredient.unit == data[0]['unit']
        assert ingredient.current_stock == Decimal(data[0]['current_stock'])
        assert ingredient.min_stock_threshold == Decimal(data[0]['min_stock_threshold'])
        assert len(data) == 1
    def test_create_ingredient(self):
        r = self.client.post("/api/ingredients/", {
            "name": "Кофейные зерна",
            "unit": "kg",
            "current_stock": "5.000",
            "min_stock_threshold": "2.000"
        }, format='json')
        new_ingredient_id = r.json()['id']
        ingredients = Ingredient.objects.all()
        assert len(ingredients) == 1
        new_ingredient = Ingredient.objects.filter(id=new_ingredient_id).first()
        assert new_ingredient.name == 'Кофейные зерна'
        assert new_ingredient.unit == 'kg'
        assert new_ingredient.current_stock == Decimal('5.000')
        assert new_ingredient.min_stock_threshold == Decimal('2.000')
    def test_delete_ingredient(self):
        ingredients = baker.make("Ingredient", 5)
        r = self.client.get('/api/ingredients/')
        data = r.json()
        assert len(data) == 5
        ingredient_id_to_delete = ingredients[2].id
        self.client.delete(f'/api/ingredients/{ingredient_id_to_delete}/')
        r = self.client.get('/api/ingredients/')
        data = r.json()
        assert len(data) == 4
        assert ingredient_id_to_delete not in [i['id'] for i in data]
    def test_update_ingredient(self):
        ingredient = baker.make("Ingredient")
        r = self.client.get(f'/api/ingredients/{ingredient.id}/')
        data = r.json()
        assert data['name'] == ingredient.name
        r = self.client.put(f'/api/ingredients/{ingredient.id}/', {
            "name": "Сахар",
            "unit": "kg",
            "current_stock": "10.000",
            "min_stock_threshold": "3.000"
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/ingredients/{ingredient.id}/')
        data = r.json()
        assert data['name'] == "Сахар"
        ingredient.refresh_from_db()
        assert ingredient.name == "Сахар"

class ProductCompositionViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        category = Category.objects.create(name="Кофе")
        product = Product.objects.create(
            name="Американо",
            price=200,
            is_available=1,
            category=category
        )
        ingredient = Ingredient.objects.create(
            name="Молоко",
            unit="l",
            current_stock=Decimal('10.000'),
            min_stock_threshold=Decimal('2.000')
        )
        composition = ProductComposition.objects.create(
            product=product,
            ingredient=ingredient,
            ingredient_amount=Decimal('0.200')
        )
        r = self.client.get('/api/compositions/')
        data = r.json()
        assert composition.product.id == data[0]['product']
        assert composition.ingredient.id == data[0]['ingredient']
        assert composition.ingredient_amount == Decimal(data[0]['ingredient_amount'])
        assert len(data) == 1
    def test_create_composition(self):
        product = baker.make("Product")
        ingredient = baker.make("Ingredient")
        r = self.client.post("/api/compositions/", {
            "product": product.id,
            "ingredient": ingredient.id,
            "ingredient_amount": "0.300"
        }, format='json')
        new_composition_id = r.json()['id']
        compositions = ProductComposition.objects.all()
        assert len(compositions) == 1
        new_composition = ProductComposition.objects.filter(id=new_composition_id).first()
        assert new_composition.product == product
        assert new_composition.ingredient == ingredient
        assert new_composition.ingredient_amount == Decimal('0.300')
    def test_delete_composition(self):
        compositions = baker.make("ProductComposition", 5)
        r = self.client.get('/api/compositions/')
        data = r.json()
        assert len(data) == 5
        composition_id_to_delete = compositions[2].id
        self.client.delete(f'/api/compositions/{composition_id_to_delete}/')
        r = self.client.get('/api/compositions/')
        data = r.json()
        assert len(data) == 4
        assert composition_id_to_delete not in [i['id'] for i in data]
    def test_update_composition(self):
        composition = baker.make("ProductComposition")
        r = self.client.get(f'/api/compositions/{composition.id}/')
        data = r.json()
        assert data['ingredient_amount'] == str(composition.ingredient_amount)
        r = self.client.put(f'/api/compositions/{composition.id}/', {
            "product": composition.product.id,
            "ingredient": composition.ingredient.id,
            "ingredient_amount": "0.500"
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/compositions/{composition.id}/')
        data = r.json()
        assert data['ingredient_amount'] == "0.500"
        composition.refresh_from_db()
        assert composition.ingredient_amount == Decimal('0.500')

class ProfileViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        profile = Profile.objects.create(
            name="Иван",
            last_name="Иванов",
            phone_number="+71234567890"
        )
        r = self.client.get('/api/profiles/')
        data = r.json()
        assert profile.name == data[0]['name']
        assert profile.last_name == data[0]['last_name']
        assert profile.phone_number == data[0]['phone_number']
        assert len(data) == 1
    def test_create_profile(self):
        r = self.client.post("/api/profiles/", {
            "name": "Петр",
            "last_name": "Петров",
            "phone_number": "+79876543210"
        }, format='json')
        new_profile_id = r.json()['id']
        profiles = Profile.objects.all()
        assert len(profiles) == 1
        new_profile = Profile.objects.filter(id=new_profile_id).first()
        assert new_profile.name == 'Петр'
        assert new_profile.last_name == 'Петров'
        assert new_profile.phone_number == '+79876543210'
    def test_delete_profile(self):
        profiles = baker.make("Profile", 5)
        r = self.client.get('/api/profiles/')
        data = r.json()
        assert len(data) == 5
        profile_id_to_delete = profiles[2].id
        self.client.delete(f'/api/profiles/{profile_id_to_delete}/')
        r = self.client.get('/api/profiles/')
        data = r.json()
        assert len(data) == 4
        assert profile_id_to_delete not in [i['id'] for i in data]
    def test_update_profile(self):
        profile = baker.make("Profile")
        r = self.client.get(f'/api/profiles/{profile.id}/')
        data = r.json()
        assert data['name'] == profile.name
        r = self.client.put(f'/api/profiles/{profile.id}/', {
            "name": "Сергей",
            "last_name": "Сергеев",
            "phone_number": "+79123456789"
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/profiles/{profile.id}/')
        data = r.json()
        assert data['name'] == "Сергей"
        profile.refresh_from_db()
        assert profile.name == "Сергей"

class OrderViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        profile = Profile.objects.create(
            name="Иван",
            last_name="Иванов",
            phone_number="+71234567890"
        )
        order = Order.objects.create(user=profile, status='pending', total_amount=200)
        r = self.client.get('/api/orders/')
        data = r.json()
        assert order.id == data[0]['id']
        assert order.status == data[0]['status']
        assert order.total_amount == data[0]['total_amount']
        assert order.user.id == data[0]['user']
        assert len(data) == 1
    def test_create_order(self):
        profile = Profile.objects.create(
            name="Петр",
            last_name="Петров",
            phone_number="+79876543210"
        )
        r = self.client.post("/api/orders/", {
            "user": profile.id,
            "status": "pending",
            "total_amount": 300
        }, format='json')
        new_order_id = r.json()['id']
        orders = Order.objects.all()
        assert len(orders) == 1
        new_order = Order.objects.filter(id=new_order_id).first()
        assert new_order.user == profile
        assert new_order.status == "pending"
        assert new_order.total_amount == 300
    def test_delete_order(self):
        orders = baker.make("Order", 5)
        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 5
        order_id_to_delete = orders[2].id
        self.client.delete(f'/api/orders/{order_id_to_delete}/')
        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 4
        assert order_id_to_delete not in [i['id'] for i in data]
    def test_update_order(self):
        order = baker.make("Order")
        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['status'] == order.status
        r = self.client.put(f'/api/orders/{order.id}/', {
            "user": order.user.id,
            "status": "ready",
            "total_amount": order.total_amount
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['status'] == "ready"
        order.refresh_from_db()
        assert order.status == "ready"

class OrderItemViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        category = Category.objects.create(name="Кофе")
        profile = Profile.objects.create(
            name="Иван",
            last_name="Иванов",
            phone_number="+71234567890"
        )
        product = Product.objects.create(name="Американо", price=200, is_available=1, category=category)
        order = Order.objects.create(user=profile, status='pending', total_amount=200)
        item = OrderItem.objects.create(order=order, product=product, quantity=1, price_at_time_of_order=200)
        r = self.client.get('/api/order-items/')
        data = r.json()
        assert item.id == data[0]['id']
        assert item.order.id == data[0]['order']
        assert item.product.id == data[0]['product']
        assert item.quantity == data[0]['quantity']
        assert item.price_at_time_of_order == data[0]['price_at_time_of_order']
        assert len(data) == 1
    def test_create_order_item(self):
        order = baker.make("Order")
        product = baker.make("Product")
        r = self.client.post("/api/order-items/", {
            "order": order.id,
            "product": product.id,
            "quantity": 2,
            "price_at_time_of_order": 150
        }, format='json')
        new_item_id = r.json()['id']
        items = OrderItem.objects.all()
        assert len(items) == 1
        new_item = OrderItem.objects.filter(id=new_item_id).first()
        assert new_item.order == order
        assert new_item.product == product
        assert new_item.quantity == 2
        assert new_item.price_at_time_of_order == 150
    def test_delete_order_item(self):
        items = baker.make("OrderItem", 5)
        r = self.client.get('/api/order-items/')
        data = r.json()
        assert len(data) == 5
        item_id_to_delete = items[2].id
        self.client.delete(f'/api/order-items/{item_id_to_delete}/')
        r = self.client.get('/api/order-items/')
        data = r.json()
        assert len(data) == 4
        assert item_id_to_delete not in [i['id'] for i in data]
    def test_update_order_item(self):
        item = baker.make("OrderItem")
        r = self.client.get(f'/api/order-items/{item.id}/')
        data = r.json()
        assert data['quantity'] == item.quantity
        r = self.client.put(f'/api/order-items/{item.id}/', {
            "order": item.order.id,
            "product": item.product.id,
            "quantity": 3,
            "price_at_time_of_order": 250
        }, format='json')
        assert r.status_code == 200
        r = self.client.get(f'/api/order-items/{item.id}/')
        data = r.json()
        assert data['quantity'] == 3
        item.refresh_from_db()
        assert item.quantity == 3
