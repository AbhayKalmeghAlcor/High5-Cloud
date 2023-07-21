import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='created_product_categories'
    )
    modified_by = models.ForeignKey(
        User, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='modified_product_categories'
    )

    class Meta:
        verbose_name_plural = 'Product Categories'
    
    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/products_images', null=True, blank=True)
    image_url = models.URLField(max_length=1000)
    logo = models.ImageField(upload_to='photos/products_logos', null=True, blank=True)
    logo_url = models.URLField(max_length=1000)
    redemption_information = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    country = models.CharField(max_length=100)
    terms_and_conditions = models.TextField()
    value_max_restriction = models.CharField(max_length=40)
    value_min_restriction = models.CharField(max_length=40)
    expiration_description = models.TextField()
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='created_products'
    )
    modified_by = models.ForeignKey(
        User, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='modified_products'
    )

    def __str__(self):
        return f"{self.name} of brand {self.brand_name}"


class ProductPointsAmountMap(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='points')
    currency = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='created_product_point_amount_maps'
    )
    modified_by = models.ForeignKey(
        User, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='modified_product_point_amount_maps'
    )

    def __str__(self):
        return f"Point Amount Map for {self.product.name}"