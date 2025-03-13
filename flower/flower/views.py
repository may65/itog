# flower/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .del_telegram_bot import send_order_notification


def product_list(request):
    """Отображает список товаров."""
    products = Product.objects.all()
    return render(request, 'flower/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    """Добавляет товар в корзину."""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {}) # Получаем корзину из сессии

    product_id_str = str(product_id) # Ключи в сессии должны быть строками

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart # Сохраняем корзину в сессию
    # return redirect('flower:view_cart')
    return redirect('view_cart')

def view_cart(request):
    """Отображает содержимое корзины."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str) # Преобразуем обратно в int для поиска
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
        total_price += item_total

    return render(request, 'flower/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def create_order(request):
    """Создает заказ на основе данных из корзины."""
    cart = request.session.get('cart', {})
    if not cart:
        # return redirect('flower:product_list')
        return redirect('product_list')# Если корзина пуста, возвращаем к списку товаров

    order = Order(
        # user=request.user
        user=request.user,
        delivery_address=request.POST.get('delivery_address'),
        delivery_time=request.POST.get('delivery_time'),
        customer_phone=request.POST.get('customer_phone')
    )
    order.save()

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = get_object_or_404(Product, id=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    request.session['cart'] = {}  # Очищаем корзину после создания заказа
    # Отправка уведомления в Telegram
    if settings.TELEGRAM_BOT_TOKEN:
        send_order_notification(order)
    return render(request, 'flower/order_confirmation.html',
                  {'order': order})  # Перенаправляем на страницу подтверждения