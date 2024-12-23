#7766016748:AAGPG0MsU1iE9syW3j5s2qJpGSS5RhJmLhc
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = ApplicationBuilder().token('7766016748:AAGPG0MsU1iE9syW3j5s2qJpGSS5RhJmLhc'
                                 '').build()

async def start_command(update, context):
    welcome_text = (
        "Добро пожаловать, я гениус\n"
        "Я помогу тебе проверить свой IQ с помощью теста\n"
        "Попробуйте следующие команды:\n"
        "/start test - начать тест\n"
        "/services - узнать об услугах\n"
        "/contacts - наши контактные данные\n"
        "/schedule - расписание услуг"
    )

    await update.message.reply_text(welcome_text)

async def book_command(update, context):
    booking_text = (
        "Чтобы забронировать номер, пожалуйста, отправьте следующую информацию:\n"
        "- Дата заезда\n"
        "- Дата выезда\n"
        "- Количество гостей\n"
        "- Тип номера (стандарт, люкс, семейный)\n\n"
        "Наш администратор свяжется с вами для подтверждения бронирования."
    )
    await update.message.reply_text(booking_text)

async def services_command(update, context):
    services_text = (
        "У нас доступны следующие услуги:\n"
        "- Завтраки\n"
        "- Бассейн и SPA\n"
        "- Wi-Fi в номерах\n"
        "- Трансфер из/в аэропорт\n"
        "- Прачечная\n\n"
        "Подробнее об услугах можно узнать у нашего администратора."
    )
    await update.message.reply_text(services_text)

async def contacts_command(update, context):
    contacts_text = (
        "Наши контактные данные:\n"
        "- Телефон: +123456789\n"
        "- Электронная почта: contact@dreamstay.com\n"
        "- Адрес: ул. Мира, 10, Киев\n\n"
        "Будем рады помочь вам!"
    )
    await update.message.reply_text(contacts_text)

async def schedule_command(update, context):
    schedule_text = (
        "Расписание:\n"
        "- Завтрак: 7:00 - 10:00\n"
        "- Обед: 12:00 - 15:00\n"
        "- Ужин: 18:00 - 21:00\n"
        "- Уборка номеров: 10:00 - 14:00\n\n"
        "Пожалуйста, сообщите нам, если вам нужно другое время для уборки."
    )
    await update.message.reply_text(schedule_text)

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("book", book_command))
app.add_handler(CommandHandler("services", services_command))
app.add_handler(CommandHandler("contacts", contacts_command))
app.add_handler(CommandHandler("schedule", schedule_command))

if __name__ == "__main__":
    app.run_polling()