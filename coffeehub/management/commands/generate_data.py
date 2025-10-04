from django.core.management.base import BaseCommand
from faker import Faker
from coffeehub.models import *
from django.contrib.auth.models import User
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate 1000 records for all models'

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        # 1. Получение существующих пользователей и профилей
        self.stdout.write("Getting existing users and profiles...")
        users = list(User.objects.all())
        profiles = list(Profile.objects.all())
        
        # Если пользователей нет, создаем несколько
        if not users:
            self.stdout.write("No existing users found. Creating sample users...")
            for i in range(50):
                user = User.objects.create_user(
                    username=fake.user_name() + str(i),
                    email=fake.email(),
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                users.append(user)
            
            # Обновляем список профилей после создания пользователей
            profiles = list(Profile.objects.all())

        # 2. Создание категорий (с обработкой дубликатов)
        self.stdout.write("Creating categories...")
        categories = []
        category_names = ['Кофе', 'Чай', 'Десерты', 'Сэндвичи', 'Салаты', 
                         'Напитки', 'Выпечка', 'Завтраки', 'Снеки']
        
        # Сначала очищаем существующие категории или используем существующие
        Category.objects.all().delete()  # Раскомментируйте если хотите очистить старые категории
        
        for name in category_names:
            try:
                # Пытаемся найти существующую категорию
                category = Category.objects.filter(name=name).first()
                if not category:
                    category = Category.objects.create(name=name)
                categories.append(category)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error with category '{name}': {e}"))
                # Создаем категорию с уникальным именем
                unique_name = f"{name}_{random.randint(1000, 9999)}"
                category = Category.objects.create(name=unique_name)
                categories.append(category)

        # 3. Создание ингредиентов
        self.stdout.write("Creating ingredients...")
        ingredients = []
        ingredient_names = [
            'Кофе молотый', 'Молоко', 'Сахар', 'Сливки', 'Шоколад', 'Ваниль',
            'Мука', 'Яйца', 'Сливочное масло', 'Сыр', 'Ветчина', 'Помидоры',
            'Салат', 'Хлеб', 'Чай черный', 'Чай зеленый', 'Мед', 'Корица',
            'Лимон', 'Мята', 'Клубника', 'Банан', 'Орехи', 'Какао'
        ]
        
        units = ['kg', 'g', 'l', 'ml', 'pcs']
        
        # Очищаем существующие ингредиенты
        Ingredient.objects.all().delete()
        
        for name in ingredient_names:
            ingredient = Ingredient.objects.create(
                name=name,
                unit=random.choice(units),
                current_stock=Decimal(random.uniform(1, 100)).quantize(Decimal('0.001')),
                min_stock_threshold=Decimal(random.uniform(0.1, 10)).quantize(Decimal('0.001'))
            )
            ingredients.append(ingredient)

        # 4. Создание продуктов
        self.stdout.write("Creating products...")
        products = []
        product_names = [
            'Эспрессо', 'Капучино', 'Латте', 'Американо', 'Раф кофе',
            'Черный чай', 'Зеленый чай', 'Чай с мятой', 'Чай с лимоном',
            'Тирамису', 'Чизкейк', 'Маффин', 'Круассан', 'Печенье',
            'Клубничный смузи', 'Шоколадный коктейль', 'Сэндвич с ветчиной',
            'Сэндвич с сыром', 'Салат Цезарь', 'Греческий салат'
        ]
        
        # Очищаем существующие продукты
        Product.objects.all().delete()
        
        for name in product_names:
            product = Product.objects.create(
                name=name,
                price=random.randint(100, 500),
                is_available=random.choice([True, False]),
                category=random.choice(categories)
            )
            products.append(product)

        # 5. Создание состава продуктов
        self.stdout.write("Creating product compositions...")
        ProductComposition.objects.all().delete()
        
        for product in products:
            # Для каждого продукта добавляем от 2 до 5 ингредиентов
            num_ingredients = random.randint(2, 5)
            selected_ingredients = random.sample(ingredients, num_ingredients)
            
            for ingredient in selected_ingredients:
                ProductComposition.objects.create(
                    product=product,
                    ingredient=ingredient,
                    ingredient_amount=Decimal(random.uniform(0.01, 0.5)).quantize(Decimal('0.001'))
                )

        # 6. Создание заказов из существующих пользователей
        self.stdout.write("Creating orders from existing users...")
        orders = []
        status_choices = ['pending', 'preparing', 'ready', 'cancelled']
        
        # Очищаем существующие заказы
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        
        # Проверяем, что есть пользователи для создания заказов
        if not users or not profiles:
            self.stdout.write(self.style.ERROR("No users or profiles available to create orders!"))
            return
        
        # Создаем заказы для существующих пользователей
        num_orders = min(200, len(profiles) * 3)  # Ограничиваем количество заказов
        for i in range(num_orders):
            try:
                profile = random.choice(profiles)
                user_admin = random.choice(users)
                
                order = Order.objects.create(
                    user_admin=user_admin,
                    user=profile,
                    status=random.choice(status_choices),
                    total_amount=0
                )
                orders.append(order)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error creating order {i}: {e}"))

        # 7. Создание позиций заказов
        self.stdout.write("Creating order items...")
        for order in orders:
            try:
                # В каждом заказе от 1 до 5 позиций
                num_items = random.randint(1, min(5, len(products)))
                selected_products = random.sample(products, num_items)
                
                total_amount = 0
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    price = product.price
                    
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price_at_time_of_order=price
                    )
                    
                    total_amount += order_item.get_total_price()
                
                # Обновляем общую сумму заказа
                order.total_amount = total_amount
                order.save()
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error creating order items for order {order.id}: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated:\n'
                f'- Users: {len(users)}\n'
                f'- Profiles: {len(profiles)}\n'
                f'- Categories: {len(categories)}\n'
                f'- Ingredients: {len(ingredients)}\n'
                f'- Products: {len(products)}\n'
                f'- Product compositions: {ProductComposition.objects.count()}\n'
                f'- Orders: {len(orders)}\n'
                f'- Order items: {OrderItem.objects.count()}'
            )
        )