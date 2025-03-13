import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import django
from django.db import DatabaseError

# Инициализация Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower.settings')
django.setup()

from flower.models import Product, Order, OrderItem
from django.contrib.auth.models import User
from dotenv import load_dotenv

load_dotenv()
# Конфигурация бота
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Примеры работы с ORM --------------------------------------------------------
def sync_orm_operations():
    """Синхронные операции с ORM"""
    # Получение товара
    product = Product.objects.get(id=1)

    # Создание заказа
    user = User.objects.get(username='admin')
    order = Order.objects.create(
        user=user,
        delivery_address="ул. Примерная, 1",
        customer_phone="+79991234567"
    )
    OrderItem.objects.create(order=order, product=product, quantity=2)


async def async_orm_operations():
    """Асинхронные операции с ORM (для aiogram 3.x+)"""
    from django.db import close_old_connections

    try:
        # Используем sync_to_async для синхронных ORM-операций
        from asgiref.sync import sync_to_async

        # Получение товара
        product = await sync_to_async(Product.objects.get)(id=1)

        # Создание пользователя
        user, created = await sync_to_async(User.objects.get_or_create)(
            username='tg_user',
            defaults={'email': 'tg@example.com'}
        )

        # Создание заказа
        order = await sync_to_async(Order.objects.create)(
            user=user,
            delivery_address="ул. Телеграмная, 5",
            customer_phone="+79997654321"
        )

        # Создание позиции заказа
        await sync_to_async(OrderItem.objects.create)(
            order=order,
            product=product,
            quantity=1
        )

    except DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        await sync_to_async(close_old_connections)()


# -----------------------------------------------------------------------------

async def send_order_notification(order: Order):
    """Отправка уведомления о новом заказе"""
    message = (
        f"🛎 Новый заказ #{order.id}!\n"
        f"👤 Пользователь: {order.user.username}\n"
        f"📞 Телефон: {order.customer_phone}\n"
        f"📍 Адрес: {order.delivery_address}\n"
        f"🕒 Время доставки: {order.delivery_time}"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        "🌸 Бот для заказа цветов\n"
        "Команды:\n"
        "/products - список товаров\n"
        "/order <адрес>;<телефон>;<ID товаров через запятую> - создать заказ"
    )


@dp.message(Command('products'))
async def list_products(message: types.Message):
    """Получение списка товаров"""
    from asgiref.sync import sync_to_async

    async def get_products():
        return await sync_to_async(list)(Product.objects.all())

    products = await get_products()
    response = "Список товаров:\n" + "\n".join(
        [f"{p.id}. {p.name} - {p.price}₽" for p in products]
    )
    await message.answer(response)


@dp.message(Command('order'))
async def create_order(message: types.Message):
    """Создание заказа через Telegram"""
    from asgiref.sync import sync_to_async

    try:
        _, data = message.text.split(maxsplit=1)
        address, phone, product_ids = data.split(';')
        product_ids = [int(pid.strip()) for pid in product_ids.split(',')]

        # Создание пользователя
        user, created = await sync_to_async(User.objects.get_or_create)(
            username=f'tg_{message.from_user.id}',
            defaults={'email': f'tg_{message.from_user.id}@example.com'}
        )

        # Создание заказа
        order = await sync_to_async(Order.objects.create)(
            user=user,
            delivery_address=address.strip(),
            customer_phone=phone.strip()
        )

        # Добавление товаров
        for pid in product_ids:
            product = await sync_to_async(Product.objects.get)(id=pid)
            await sync_to_async(OrderItem.objects.create)(
                order=order,
                product=product,
                quantity=1
            )

        await message.answer(f"✅ Заказ #{order.id} создан!")
        await send_order_notification(order)

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())