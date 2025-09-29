from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Категории товаров
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

# Продукты
class Product(models.Model):
    name = models.TextField("Название")
    price = models.IntegerField("Цена")
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Категория'
    )
    picture = models.ImageField("Изображение", null=True, upload_to="products")
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."

# Ингредиенты
class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('kg', 'кг'),
        ('g', 'г'),
        ('l', 'л'),
        ('ml', 'мл'),
        ('pcs', 'шт'),
    )
    
    name = models.CharField(max_length=100, verbose_name='Название')
    unit = models.CharField(
        max_length=3, 
        choices=UNIT_CHOICES, 
        verbose_name='Единица измерения'
    )
    current_stock = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        default=0,
        verbose_name='Текущий запас'
    )
    min_stock_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        default=0,
        verbose_name='Минимальный запас'
    )
    picture = models.ImageField("Изображение", null=True, upload_to="ingredients")
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.get_unit_display()})"
    
    def is_low_stock(self):
        return self.current_stock <= self.min_stock_threshold

# Состав продуктов
class ProductComposition(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='compositions'
    )
    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    ingredient_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        verbose_name='Количество ингредиента'
    )
    
    class Meta:
        verbose_name = 'Состав продукта'
        verbose_name_plural = 'Состав продуктов'
        unique_together = ['product', 'ingredient']
    
    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name}"

# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null= True)
    name = models.TextField("Имя", null=True)
    last_name = models.TextField("Фамилия",null=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        verbose_name='Номер телефона'
    )
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

# Заказы
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('preparing', 'Готовится'),
        ('ready', 'Готов'),
        ('cancelled', 'Отменен'),
    )
    user_admin = models.ForeignKey("auth.User",on_delete=models.CASCADE,
        verbose_name='Пользователь',null = True)
    user = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='orders'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Статус'
    )
    total_amount = models.IntegerField(
        default=0,
        verbose_name='Общая сумма'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    # def __str__(self):
    #     return f"Заказ #{self.id} - {self.user.username}"

# Позиции в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    price_at_time_of_order = models.IntegerField(
        verbose_name='Цена на момент заказа'
    )
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def get_total_price(self):
        return self.price_at_time_of_order * self.quantity


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()