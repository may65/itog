# tests/test_telegram_bot.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from flower.telegram_bot import send_order_notification, create_order
from flower.models import Order, User, Product


@pytest.mark.asyncio
async def test_send_order_notification(mocker):
    mock_bot = AsyncMock()
    mocker.patch('flower.telegram_bot.bot', mock_bot)

    user = User(username='testuser')
    order = Order(
        id=1,
        user=user,
        delivery_address="ул. Тестовая",
        customer_phone="+79991234567"
    )

    await send_order_notification(order)
    mock_bot.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_create_order_command():
    mock_message = AsyncMock()
    mock_message.text = "/order ул. Тестовая;+79991234567;1"
    mock_message.from_user = MagicMock(id=123)

    mock_user = MagicMock()
    mock_product = MagicMock()

    with pytest.MonkeyPatch.context() as m:
        m.setattr('flower.telegram_bot.sync_to_async', lambda x: x)
        m.setattr('flower.telegram_bot.User.objects.get_or_create', lambda *args, **kwargs: (mock_user, True))
        m.setattr('flower.telegram_bot.Product.objects.get', lambda *args, **kwargs: mock_product)

        await create_order(mock_message)
        mock_message.answer.assert_called_with("✅ Заказ #1 создан!")