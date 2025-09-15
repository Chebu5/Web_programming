from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from coffeehub.models import *
from coffeehub.serializers import *

# Категории
class CategoriesViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Продукты
class ProductsViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """Переключение доступности продукта"""
        product = self.get_object()
        product.is_available = not product.is_available
        product.save()
        return Response({'status': 'availability toggled', 'is_available': product.is_available})

# Ингредиенты
class IngredientsViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Список ингредиентов с низким запасом"""
        low_stock_ingredients = Ingredient.objects.filter(current_stock__lte=models.F('min_stock_threshold'))
        serializer = self.get_serializer(low_stock_ingredients, many=True)
        return Response(serializer.data)

# Состав продуктов
class ProductCompositionsViewSet(mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    queryset = ProductComposition.objects.all()
    serializer_class = ProductCompositionSerializer
    
    def get_queryset(self):
        """Фильтрация по продукту если передан product_id"""
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

# Профили пользователей
class ProfilesViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """Фильтрация профилей по роли"""
        role = request.query_params.get('role')
        if role:
            profiles = Profile.objects.filter(role=role)
        else:
            profiles = Profile.objects.all()
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)

# Заказы
class OrdersViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Обновление статуса заказа"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({'status': 'order status updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Фильтрация заказов по статусу"""
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = Order.objects.filter(status=status_filter)
        else:
            orders = Order.objects.all()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

# Позиции заказов
class OrderItemsViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        """Фильтрация по заказу если передан order_id"""
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset