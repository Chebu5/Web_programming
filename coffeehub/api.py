from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins,viewsets
from coffeehub.models import *
from coffeehub.serializers import *
class ProductsViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer