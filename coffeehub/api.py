from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins,viewsets
from coffeehub.models import Product
from coffeehub.serializers import ProductSerializer
class ProductsViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer