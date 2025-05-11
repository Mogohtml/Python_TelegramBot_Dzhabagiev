import re

from telegram import Update
from telegram.ext import ContextTypes
from settings.config import AppSettings
from app.infra.postgres.db import Database


settings = AppSettings()

database = Database(settings.POSTGRES_DSN)


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
        await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)


async def register_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.user.id:
        pass

async def create_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user.id:
        try:
            user_id = update.message.from_user.id
            message_text = update.message.text

            pattern = r'/create_event\s+(.*?)\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*(.*)'
            match = re.match(pattern, message_text)

            if match:
                event_name = match.group(1)
                event_date = match.group(2)
                event_time = match.group(3)
                event_details = match.group(4)

                await context.application.event_service.create_event(user_id, event_name, event_date, event_time, event_details)

                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Создано событие: {event_name}  для пользователя: {user_id}")
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Некорректный формат сообщения. Пожалуйста, используйте формат: /create_event <название> <дата> <время> [детали]")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка! {str(e)}")


async def read_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user.id:
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
    if update.message and update.message.text and update.message.from_user.id:
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
    if update.message and update.message.text and update.message.from_user.id:
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

async def display_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text and update.message.from_user.id:
        try:
            user_id = update.message.from_user.id
            all_events = await context.application.event_service.display_event(user_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события: {all_events}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")

async def display_event_sorted_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text:
        try:
            user_id = update.message.from_user.id
            all_events = await context.application.event_service.display_event_sorted(user_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Все события в порядке убывания: {all_events}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка. {str(e)}")