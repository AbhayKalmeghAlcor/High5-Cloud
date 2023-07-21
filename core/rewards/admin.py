from django.contrib import admin

from rewards import models


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Check if the created_by field is not set (new instance)
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(BaseAdmin):
    list_display = ('id', 'name', 'is_active', 'created_by', 'created_at', 'modified_by', 'modified_at')
    list_filter = ('is_active', 'created_by', 'modified_by', 'created_at', 'modified_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'modified_at', 'modified_by', 'created_by')


@admin.register(models.Product)
class ProductAdmin(BaseAdmin):
    list_display = ('id', 'name', 'brand_name', 'created_at', 'modified_at')
    list_filter = ('is_active', 'category__name')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'modified_at', 'modified_by', 'created_by')


@admin.register(models.ProductPointsAmountMap)
class ProductPointAmountMapAdmin(BaseAdmin):
    list_display = ('id', 'product', 'points', 'amount')
    list_filter = ('is_active', 'product__name')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'modified_at', 'modified_by', 'created_by')