# flower/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Модель товара (цветка)."""
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Order(models.Model):
    """Модель заказа."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivery_address = models.TextField(verbose_name="Адрес доставки", blank=True, null=True)
    delivery_time = models.DateTimeField(verbose_name="Время доставки", blank=True, null=True)
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

class OrderItem(models.Model):
    """Модель позиции заказа (один товар в заказе)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в заказе #{self.order.id}"