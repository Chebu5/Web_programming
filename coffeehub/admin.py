from django.contrib import admin
from coffeehub.models import Product,Category,Order,Profile

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']
@admin.register(Order)
class OrederAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Order._meta.get_fields() if field.concrete and not field.many_to_many]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_admin=request.user)

    def has_view_permission(self, request, obj=None):
        # Разрешать менять только свои объекты, суперюзер может все
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.user_admin == request.user

    def has_delete_permission(self, request, obj=None):
        # Разрешать удалять только свои объекты
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.user_admin == request.user
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','last_name','name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)