from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['is_available']

class IngredientSerializer(serializers.ModelSerializer):
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ingredient
        fields = '__all__'

class ProductCompositionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    
    class Meta:
        model = ProductComposition
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    # При создании принимаем product в виде ID (PrimaryKeyRelatedField)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_time_of_order', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.price_at_time_of_order

class OrderSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(many=True)  # writable nested serializer

    class Meta:
        model = Order
        fields = ['id', 'user_admin', 'user', 'user_username', 'status', 'status_display', 'total_amount', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        print("Create Order called")
        items_data = validated_data.pop('items', [])
        request = self.context.get('request')
        user = request.user
        profile = user.profile

        validated_data.pop('user', None)
        validated_data.pop('user_admin', None)

        order = Order.objects.create(user_admin=user, user=profile, **validated_data)
        print(f"Order created with id={order.id}")

        total_amount = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_time_of_order=price
        )
            total_amount += price * quantity
            print(f"OrderItem added: product id {product.id}, quantity {quantity}")
        order.total_amount = total_amount
        order.save()
        print(f"Order total_amount updated: {total_amount}")
        return order

    def update(self, instance, validated_data):
        # Решение для обновления заказа и позиций — optional
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)

        if items_data is not None:
            # Удаляем старые позиции и добавляем новые в упрощённом варианте
            instance.items.all().delete()
            total_amount = 0
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                price = product.price
                OrderItem.objects.create(
                    order=instance,
                    product=product,
                    quantity=quantity,
                    price_at_time_of_order=price
                )
                total_amount += price * quantity
            instance.total_amount = total_amount
            instance.save()

        return instance