from rest_framework.viewsets import GenericViewSet
from coffeehub.models import Product

class ProductViewSet(GenericViewSet):
    queryset = Product.objects.all()