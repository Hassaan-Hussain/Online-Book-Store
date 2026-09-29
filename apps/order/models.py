from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from ..catalog.models import Book

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders',
    )
    address = models.ForeignKey(
            'accounts.Address',
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            related_name='orders'
    )

    user_snapshot = models.CharField(max_length=255, blank=True, null=True)
    address_snapshot = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('shipped', 'Shipped'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"

    def save(self, *args, **kwargs):
        if self.user and not self.user_snapshot:
            self.user_snapshot = f"{self.user.get_full_name()} ({self.user.email})"

        if self.address and not self.address_snapshot:
            self.address_snapshot = f"{self.address.address}, {self.address.city}, {self.address.state}, {self.address.postal_code}"

        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
    )
    book = models.ForeignKey(
        'catalog.Book',
        on_delete=models.PROTECT,
        related_name='order_items',
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'book'],
                name='unique_book_per_order',
            ),
        ]
        

    def save(self, *args, **kwargs):
        self.subtotal = self.price_at_time * self.quantity
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.quantity > self.book.stock_quantity:
            raise ValidationError('Ordering quantity is more than stock quantity')

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"