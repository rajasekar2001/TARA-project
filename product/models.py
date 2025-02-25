from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ('In stock', 'In stock'),
        ('Out of stock', 'Out of stock'),
    ]

    CATEGORY_CHOICES = [
        ('Rings', 'Rings'),
        ('Chains', 'Chains'),
        ('Pendants', 'Pendants'),
        ('Bangles', 'Bangles'),
        ('Anklets', 'Anklets'),
        ('Necklaces', 'Necklaces'),
        ('Bracelets', 'Bracelets'),
        ('Earrings', 'Earrings'),
    ]

    product_id = models.CharField(max_length=10, primary_key=True, unique=True, editable=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In stock')

    @property
    def total_price(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if not self.product_id:
            last_product = Product.objects.order_by('-product_id').first()
            if last_product and last_product.product_id.startswith("PR-"):
                last_number = int(last_product.product_id.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.product_id = f"PR-{new_number:03d}"

        self.status = 'In stock' if self.quantity > 0 else 'Out of stock'

        super().save(*args, **kwargs)

    def reduce_stock(self, quantity):
        if quantity > self.quantity:
            raise ValueError("Insufficient stock!")
        self.quantity -= quantity
        self.save()

    def __str__(self):
        return f"{self.product_id} - {self.category} (x{self.quantity})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # One-to-Many Relationship
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.product_id}"
