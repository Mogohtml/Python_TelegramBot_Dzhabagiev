from telegram import Update
from telegram.ext import ContextTypes
from app.event_manager import Calendar
from settings.config import AppSettings

from app.infra.postgres.db import Database


settings = AppSettings()

database = Database(settings.POSTGRES_DSN)
calendar = Calendar(database)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.effective_user and update.message:
        welcome_message = (
            "Привет! Я ваш бот-календарь. Вы можете использовать следующие команды:\n"
            "/create_event <название> <дата> <время> [детали] - создать событие\n"
            "/read_event <номер_события> - прочитать событие\n"
            "/edit_event <номер_события> <поле> <новое_значение> - редактировать событие\n"
            "/delete_event <номер_события> - удалить событие\n"
            "/display_event - показать все события\n"
            "/sorted_events - показать все события в порядке убывания"
        )
        await context.application.user_service.register_visitor(update.effective_user.id) # type: ignore[attr-defined]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

async def create_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            event_name = update.message.text[14:]
            event_date = "2023-03-14"
            event_time = "14:00"
            event_details = "Описание события"

            event_id = calendar.create_event(event_name, event_date, event_time, event_details)

            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Создано событие: {event_name} с номером: {event_id}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")

async def read_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            event_id = int(update.message.text.split()[1])
            event = await context.application.calendar.read_event(event_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Вот событие: {event}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")

async def edit_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            parts = update.message.text.split()[1:]
            event_id = int(parts[0])
            field = parts[1]
            new_value = ' '.join(parts[2:])

            if field == "name":
                await context.application.calendar.edit_event(event_id, name=new_value)
            elif field == "date":
                await context.application.calendar.edit_event(event_id, date=new_value)
            elif field == "time":
                await context.application.calendar.edit_event(event_id, time=new_value)
            elif field == "details":
                await context.application.calendar.edit_event(event_id, details=new_value)

            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Событие: {event_id} изменено")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")

async def delete_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            event_id = int(update.message.text.split()[1])
            del_event = await context.application.calendar.delete_event(event_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Событие: {del_event} удалено")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")

async def display_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            all_events = await context.application.calendar.display_event()
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события: {all_events}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")

async def display_event_sorted_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            all_events = await context.application.calendar.display_event_sorted()
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события в порядке убывания: {all_events}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")