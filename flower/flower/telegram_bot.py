# flower/telegram_bot.py
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from django.conf import settings
# from flower.models import Order
from .models import Order
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN
ADMIN_CHAT_ID = settings.ADMIN_CHAT_ID  # ID вашего чата с ботом для уведомлений

def start(update, context):
    update.message.reply_text("Привет! Я бот для уведомлений о заказах цветов.")

def send_order_notification(order):
    bot = Bot(token=TELEGRAM_TOKEN)
    message = (
        f"Новый заказ #{order.id}!\n"
        f"Пользователь: {order.user.username}\n"
        f"Телефон: {order.customer_phone}\n"
        f"Адрес доставки: {order.delivery_address}\n"
        f"Время доставки: {order.delivery_time}"
    )
    bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

def setup_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    logger.info("Бот запущен в режиме polling.")