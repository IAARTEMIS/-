#7766016748:AAGPG0MsU1iE9syW3j5s2qJpGSS5RhJmLhc
from telegram import InputMediaPhoto, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import sqlite3
import asyncio


# Стадії конверсії
DATE_START, DATE_END, GUESTS, ROOM_TYPE = range(4)

app = ApplicationBuilder().token('7766016748:AAGPG0MsU1iE9syW3j5s2qJpGSS5RhJmLhc').build()

# Налаштування бази даних
def setup_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Створення таблиці користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        chat_id INTEGER NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

def add_user(username, chat_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO users (username, chat_id)
        VALUES (?, ?)
        """, (username, chat_id))
        connection.commit()
        print(f"Користувач {username} успішно доданий.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні користувача: {e}")
    finally:
        connection.close()

def add_booking(chat_id, date_start, date_end, guests, room_type):
    connection = sqlite3.connect("datebase.db")
    cursor = connection.cursor()
    try:
        # Отримання user_id за chat_id
        cursor.execute("SELECT is FROM users WHERE chat-id = ?", (chat_id))
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            cursor.execute("""INSERT INTO booking (user_id, date_start, data_end, guests, room_type)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, date_start, date_end, guests, room_type))
            connection.commit()
            print("Користувача не зенайденно в базі.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні бронювання: {e}")
    finally:
        connection.close()

def get_all_users():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = cursor.fetchall()
    connection.close()
    return [user[0] for user in users]

async def broadcast_message(update, context):
    users = get_all_users()
    message = "Этот массовая рассылка для всех пользователей!"
    successful = 0
    failed = 0

    for chat_id in users:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            successful += 1
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {chat_id}: {e}")
            failed += 1
        await asyncio.sleep(0.1) #Додати затримку для уникнення ліміту Telegram

    await update.message.reply_text(f"Рассылка завершена. Успешно: {successful}, Неудачно: {failed}")

async def start_command(update, context):
    username = update.effective_user.username or "NoUsername"
    chat_id = update.effective_user.id

    #Додавання користувача в базу данних
    add_user(username, chat_id)

    inline_keyboard = [
        [InlineKeyboardButton("Заказать такси", callback_data="Order_a_taxi")],
        [InlineKeyboardButton("Услуги", callback_data="services")],
        [InlineKeyboardButton("Контакты", callback_data="contacts")],
        [InlineKeyboardButton("Наш сайт", url="https://uklon.com.ua/ru/")],
        [InlineKeyboardButton("Самое нерекамендованное время заказов", callback_data="schedule")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_text(
        "Добро пожаловать! Я навигатор такси. Если хочеш заказать такси, я к твоиим услугам!:",
        reply_markup=markup
    )


async def button_handler(update, context):
    q = update.callback_query
    await q.answer()

    if q.data == "Order_a_taxi":
        await q.message.reply_text(
            "Чтобы заказать такси, пожалуйста, отправьте следующую информацию:\n"
            "- Дата заезда\n"
            "- Место нахождение\n"
            "- Количество заказчиков\n"
            "- Класс такси (бизнес, люкс, эконом)\n"
        )
        return DATE_START
    elif q.data == "services":
        await  q.message.reply_text(
            "У нас доступны следующие услуги:\n"
            "- Выбор водителя который к вам приедет\n"
            "- Выбор марки и класса которая к вам подьедет\n"
            "- Выбор любимых ваших заказов и водителей\n"
            "- Время за которое вам нада добратся на место\n"
            "- Заказ личного водителя на определённое время, за определённую сумму\n"
        )
        return ConversationHandler.END
    elif q.data == "contacts":
        await  q.message.reply_text(
            "Наши контактные данные:\n"
            "- Телефон: +380686504379\n"
            "- Электронная почта: contact@dreamstay.com\n"
            "- Адрес: ул. Мира, 10, Киев\n"
        )
        return ConversationHandler.END
    elif q.data == "schedule":
        await  q.message.reply_text(
            "Время когда водители меньше всего ездят, а могут вообще не ездить:\n"
            "- Завтрак: 7:00 - 8:00\n"
            "- Обед: 12:00 - 13:00\n"
            "- Ужин: 18:00 - 19:00\n"
        )
        return ConversationHandler.END

# Сбор данных для бронирования
async def date_start(update, context):
    context.user_data['date_start'] = update.message.text
    await update.message.reply_text("Введите дату выезда (например, 2023-12-10):")
    return DATE_END

async def date_end(update, context):
    context.user_data['date_end'] = update.message.text
    await update.message.reply_text("Сколько гостей будет проживать?")
    return GUESTS

async def guests(update, context):
    context.user_data['guests'] = update.message.text
    reply_keyboard = [["Стандарт", "Люкс", "Семейный"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите тип номера:", reply_markup=markup)
    return ROOM_TYPE

async def room_type(update, context):
    context.user_data['room_type'] = update.message.text
    booking_details = (
        f"Ваши данные для бронирования:\n"
        f"- Дата заезда: {context.user_data['date_start']}\n"
        f"- Дата выезда: {context.user_data['date_end']}\n"
        f"- Количество гостей: {context.user_data['guests']}\n"
        f"- Тип номера: {context.user_data['room_type']}\n"
        "Если все верно, наш администратор свяжется с вами для подтверждения."
    )
    await update.message.reply_text(booking_details, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Бронирование отменено. Возвращайтесь, когда будете готовы!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


#InputMediaPhoto
async def send_photos(update,contrxt):
    #Шляхи до локальних файлів
    photo_paths = ["noname/9458a801c21d72e72c78f406d860fb3e95d2575772d6a30be7a6bb9a6e9d080a.jpg", "noname/death note.jpg", "noname/death note2.jpg", "noname/team.jpg", "noname/welcome.jpg"]
    #Перевірка на шснування файлів
    try:
        media_group = [InputMediaPhoto(open(photo, "rb")) for photo in photo_paths]
        await update.message.reply_media_group(media_group)
    except FileNotFoundError as e:
        await update.message.reply_text(f"Помилка: файл {e.filename} не знайдено.")
    except Exception as e:
        await update.message.reply_text(f"Виникла помилка: {str(e)}")

#Додавання обробника команди
app.add_handler(CommandHandler("sendphotos", send_photos))
booking_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern="^(Order_a_taxi|services|contacts|schedule)$")],
    states={
        DATE_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, date_start)],
        DATE_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, date_end)],
        GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, guests)],
        ROOM_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, room_type)],
    },
    fallbacks=[CommandHandler("cancel", cancel)], per_user= True
)
app.add_handler(booking_handler)
#Інцінізація бази данних
setup_database()

app.add_handler(CommandHandler("start", start_command))

#Запуск бота
if __name__ == "__main__":
    app.run_polling()
