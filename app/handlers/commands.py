import re
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from settings.config import AppSettings
from app.infra.postgres.db import Database


settings = AppSettings()

database = Database(settings.POSTGRES_DSN)

FIRST_NAME, LAST_NAME, PATRONYMIC, EMAIL, PASSWORD = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.effective_user and update.message:
        welcome_message = (
            "Привет! Я ваш бот-календарь. Вы можете использовать следующие команды:\n"
            "/create_event <название> <дата> <время> [детали] - создать событие\n"
            "/register <имя> <фамилия> [отчество] <почта> <пароль> - регистрация\n"
            "/read_event <номер_события> - прочитать событие\n"
            "/edit_event <номер_события> <поле> <новое_значение> - редактировать событие\n"
            "/delete_event <номер_события> - удалить событие\n"
            "/sorted_events - <1> Показать все события в порядке возрастания <2> Показать все события в порядке убывания"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)


async def register_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            await context.bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, введите ваше имя:")
            return FIRST_NAME
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")
    return ConversationHandler.END

async def first_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            first_name = update.message.text
            context.user_data["first_name"] = first_name
            await context.bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, введите вашу фамилию:")
            return LAST_NAME
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")
    return ConversationHandler.END


async def last_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            last_name = update.message.text
            context.user_data["last_name"] = last_name
            await context.bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, введите ваше отчество:")
            return PATRONYMIC
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")
    return ConversationHandler.END

async def patronymic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            patronymic = update.message.text
            context.user_data["patronymic"] = patronymic
            await context.bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, введите ваш email:")
            return EMAIL
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")
    return ConversationHandler.END


async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            email = update.message.text
            context.user_data["email"] = email
            await context.bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, введите ваш пароль:")
            return PASSWORD
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")
    return ConversationHandler.END


async def password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            password = update.message.text
            context.user_data["password"] = password
            user_id = update.message.from_user.id
            first_name = context.user_data["first_name"]
            last_name = context.user_data["last_name"]
            patronymic = context.user_data["patronymic"]
            email = context.user_data["email"]
            password = context.user_data["password"]

            await context.application.user_service.create_user(user_id, last_name, first_name, email, password, patronymic)

            await context.bot.send_message(chat_id=update.message.chat_id, text="Регистрация завершена!")
            return ConversationHandler.END
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler.END:
    await context.bot.send_message(chat_id=update.message.chat_id, text="Регистрация отменена.")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register_user_handler)],
    states={
        FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_name_handler)],
        LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_name_handler)],
        PATRONYMIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, patronymic_handler)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_handler)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_handler)],
    },
    fallbacks=[CommandHandler("cancel", cancel_handler)]
)


async def create_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            user_id = update.message.from_user.id
            message_text = update.message.text

            pattern = r'/create_event\s+(.*?)\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*(.*)'
            match = re.match(pattern, message_text)

            if match:
                event_name = match.group(1)
                event_date = datetime.strptime(match.group(2), "%Y-%m-%d").date()
                event_time = datetime.strptime(match.group(3), "%H:%M").time()
                event_details = match.group(4)

                await context.application.event_service.create_event(user_id, event_name, event_date, event_time, event_details)

                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Создано событие: {event_name}  для пользователя: {user_id}")
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Некорректный формат сообщения. Пожалуйста, используйте формат: /create_event <название> <дата> <время> [детали]")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")


async def read_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            user_id = update.message.from_user.id

            pattern = r'/read_event\s+(\d+)'
            match = re.match(pattern, update.message.text)

            if match:
                event_id = int(match.group(1))

                event = await context.application.event_service.read_event(event_id, user_id)
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Вот событие: {event}")
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Некорректный формат сообщения. Пожалуйста, используйте формат: /read_event <номер события>")

        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")


async def edit_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            message_text = update.message.text
            user_id = update.message.from_user.id
            patterns = r'/edit_event\s+(\d+)\s+(name|date|time|details)\s+(.*)'
            match = re.match(patterns, message_text)
            if match:
                event_id = int(match.group(1))
                field = match.group(2)
                new_value = match.group(3).strip()


                if field == "name":
                    await context.application.event_service.edit_event(event_id, user_id, name=new_value)
                elif field == "date":
                    await context.application.event_service.edit_event(event_id, user_id, date=new_value)
                elif field == "time":
                    await context.application.event_service.edit_event(event_id, user_id, time=new_value)
                elif field == "details":
                    await context.application.event_service.edit_event(event_id, user_id, details=new_value)

                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Событие: {event_id} изменено")
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Некорректный формат сообщения. Пожалуйста, используйте формат: /edit_event <номер события> <поле> <новое значение>")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")


async def delete_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            user_id = update.message.from_user.id
            message_text = update.message.text
            pattern = r'/delete_event\s+(\d+)'

            match = re.match(pattern, message_text)

            if match:
                event_id = int(match.group(1))

                del_event = await context.application.event_service.delete_event(event_id, user_id)
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Событие: {del_event} удалено")
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Некорректный формат ввода. Введите номер события!")

        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")


async def display_event_sorted_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user and update.message.from_user.id:
        try:
            message_text = update.message.text
            user_id = update.message.from_user.id
            pattern = r'/sorted_events\s*(\d*)'
            match = re.match(pattern, message_text)

            if match:
                choice_sorted = match.group(1)

                if choice_sorted in ["1", "2"]:
                    reverse = (choice_sorted == "2")
                    all_events = await context.application.event_service.display_event_sorted(user_id, reverse=reverse)
                    if all_events:
                        if choice_sorted == "1":
                            events_text = "\n".join([f"Event number: {event['id']}, Date: {event['date']}, Time: {event['time']}, Details: {event['details'] if event['details'] else None}"
                                                    for event in all_events])
                            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события в порядке возрастания:\n{events_text}")

                        elif choice_sorted == "2":
                            events_text = "\n".join([f"Event number: {event['id']}, Date: {event['date']}, Time: {event['time']}, Details: {event['details'] if event['details'] else None}"
                                                    for event in all_events])
                            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события в порядке убывания:\n{events_text}")
                    else:
                        await context.bot.send_message(chat_id=update.message.chat_id, text="У вас нет событий.")
                else:
                    await context.bot.send_message(chat_id=update.message.chat_id, text="Некорректный параметр сортировки. Используйте /sorted_events [1|2]")
            else:
                # Если параметр не указан, по умолчанию отображаем события в порядке возрастания
                all_events = await context.application.event_service.display_event_sorted(user_id, reverse=False)
                if all_events:
                    events_text = "\n".join([f"Event number: {event['id']}, Date: {event['date']}, Time: {event['time']}, Details: {event['details'] if event['details'] else None}"
                                            for event in all_events])
                    await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события в порядке возрастания:\n{events_text}")
                else:
                    await context.bot.send_message(chat_id=update.message.chat_id, text="У вас нет событий.")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")
