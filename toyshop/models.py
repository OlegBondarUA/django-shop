from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(
        'toyshop.Product', on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='slide_image', blank=True, null=True)
    base_url = models.URLField()

    def __str__(self):
        return self.image.url


class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='brand_image', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    base_url = models.URLField(max_length=512)
    title = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    rating = models.FloatField(max_length=3, blank=True, null=True)
    image = models.ImageField(upload_to='image')
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    category = models.ManyToManyField(Category, related_name='products')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='products',
        blank=True, null=True
    )

    def __str__(self):
        return self.title


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product
