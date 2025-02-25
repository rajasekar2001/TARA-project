from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Raw Material Model
class RawMaterial(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.FloatField()  # Available stock in KG or units
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.quantity} available)"

# Finished Product Model
class FinishedProduct(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='product name', null=True,blank=True)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField(default=0)  # Number of finished products
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product_name} ({self.quantity} in stock)"

# Production Process: Converts Raw Material to Finished Product
class Production(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    finished_product = models.ForeignKey(FinishedProduct, on_delete=models.CASCADE, related_name="productions")
    raw_material_used = models.FloatField()  # Quantity of raw material used
    quantity_produced = models.IntegerField()  # Number of finished products created
    start_time = models.DateTimeField(auto_now_add=True)  # Auto-fetch start time
    end_time = models.DateTimeField(null=True, blank=True)  # User will set this
    duration = models.DurationField(null=True, blank=True)  # Auto-calculate
    is_completed = models.BooleanField(default=False)  # Status of production

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:  # Ensure both are not None
            if self.end_time < self.start_time:
                raise ValidationError("End time cannot be earlier than start time.")
            self.duration = self.end_time - self.start_time  # Auto-calculate duration
        super().save(*args, **kwargs)


    def complete_production(self):
        """Ye function tab call hoga jab end_time reach ho jaye"""
        if not self.is_completed and self.end_time and now() >= self.end_time:
            if self.raw_material.quantity < self.raw_material_used:
                raise ValidationError("Not enough raw material to complete production.")
            
            # Reduce raw material stock
            self.raw_material.quantity -= self.raw_material_used
            self.raw_material.save()

            # Increase finished product stock
            self.finished_product.quantity += self.quantity_produced
            self.finished_product.save()

            # Mark production as completed
            self.is_completed = True
            self.save()
