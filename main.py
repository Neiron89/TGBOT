from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters
from amocrm.v2 import tokens
from amocrm.v2 import Lead
from amocrm.v2 import Lead as _Lead, custom_field
import logging

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен Telegram-бота
TELEGRAM_TOKEN = '7636326131:AAHWD1hPtVgPl1JYPqIrttMO6ymcXZc9uus'

# Кастомные поля
class Lead(_Lead):
    trek_number = custom_field.TextCustomField("Трек - номер")
    local = custom_field.TextCustomField("Текущее местоположение груза")
    stage = custom_field.TextCustomField("Статус доставки")
    date_update = custom_field.DateCustomField("Дата последнего обновления")
    date_delivery = custom_field.DateCustomField("Ожидаемая дата доставки")

# Инициализация токена AmoCRM
tokens.default_token_manager(
    client_id="34f5a810-c579-4723-ae9d-a843ccc7914b",
    client_secret="03H1cUAGorPYSjzVnmSi67HFRtmrSTCWVvnqDciFUIoM7TxvfPhnaITD74yrelt8",
    subdomain="newhtf",
    redirect_url="https://newhtf.amocrm.ru/",
    storage=tokens.FileTokensStorage(),
)
# tokens.default_token_manager.init(
#     code="def50200baac657e6883cb14bd6271a6b02cffc8fdc9456b4424b278b10ac2fc39e94106009b433c613bdd22bd64fda32cccf0cdbd09f377ea20ad964e29a2931d2d96788cb4f899c2e7262fcde590ea6c5e0b7f28b46474c6cca73bbf58da0d2952e3542bc613b5928a80f62be0834eb468b06ae4be06cd4fc6327f2f4a3806269a27fb73a7c83bbff8170cfcce86013540f778b05a8ca960a735434e8147070d5185943cd225dad7b640d0f7fd5a9bc788560f5c7e03ad84bd65d87edaa488e3351001f234a96beea568bb271614a15a9653b3e6056adfd2e70faf3b40b8718809628b34a8e2280318e9cfea99d72800e9c0d07b47c2b4668b0f8a9118abfc3f02dddcafaf2eeb097bab699115eaed629c5b44bc7cc3dbee1edae9a623bc2d3c0143ffc0d9edd212b6f435d63a04d0061cc8aeb8bd197df3815a15cb00ec671b22a32e69ddc6c91dd5700960f88e126302657eaa18b007a0a64340946ca216f42c3417e64c308b6af3e3cd54f300cc88f94b01b4e121ec0f1a107f2f027c42a681d5520a94a8c4024a206a11befc837f85c073d2e111c5e2d5ac16d35521dff9f2b0b0e12a611d29f5fd24460696ce353ef52d2f32034b25c94b0bba1617f6b6c93fe44a2d580d212f21ea4b6ed4c38c7addbefb4373712117f45870cee63815dd4c22e37c5b5feef1",
#     skip_error=False
# )

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите ID сделки, чтобы получить информацию о грузе.')

# Обработка сообщения от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lead_id = update.message.text.strip()

    if not lead_id.isdigit():
        await update.message.reply_text("Пожалуйста, введите корректный числовой ID сделки.")
        return

    try:
        lead = Lead.objects.get(object_id=int(lead_id))
        trek_number = lead.trek_number
        local = lead.local
        stage = lead.stage
        date_update = lead.date_update
        date_delivery = lead.date_delivery

        message = (
            f"✅ Информация по грузу #{trek_number}\n\n"
            f"📍 Текущее местоположение: {local}\n"
            f"🚚 Статус: {stage}\n\n"
            f"📅 Последнее обновление: {date_update}\n"
            f"⏱️ Ожидаемая дата доставки: {date_delivery}\n\n"
            "KitTech следит за вашим грузом 24/7!"
        )
        await update.message.reply_text(message)

    except Exception as e:
        logger.error(f"Ошибка при получении информации о сделке: {e}")
        await update.message.reply_text("Не удалось найти информацию по сделке. Проверьте ID и попробуйте снова.")

# Запуск бота
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()