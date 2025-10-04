"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from django.conf.urls.static import static
from coffeehub.api import *
from coffeehub import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('products', ProductsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('compositions', ProductCompositionsViewSet)
router.register('profiles', ProfilesViewSet)
router.register('orders', OrdersViewSet)
router.register('order-items', OrderItemsViewSet)
urlpatterns = [
    path('api/profiles/me/', CurrentUserProfileView.as_view(), name='current_user_profile'),
    path('',views.ShowProductView.as_view()),
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
