import pytest
from unittest.mock import MagicMock, AsyncMock
from telegram import Update, Bot
from telegram.ext import CallbackContext, ContextTypes
from app.handlers.commands import (start, register_user_handler, create_event_handler,
                                   uploading_button_callback)


@pytest.mark.asyncio
async def test_start_command():
    # Создаем mock-объекты для Update и ContextTypes
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    # Настройка mock-объектов
    mock_update.effective_chat.id = 123
    mock_update.effective_chat.id = 123
    mock_update.message = AsyncMock()
    mock_context.bot = AsyncMock(spec=Bot)
    mock_context.bot.send_message = AsyncMock()

    await start(mock_update, mock_context)

    # Проверяем, что сообщения было отправлено
    mock_context.bot.send_message.assert_awaited_with(
        chat_id=123,
        text="Привет! Я ваш бот-календарь. Вы можете использовать следующие команды:\n"
             "/create_event <название> <дата> <время> [детали] - создать событие\n"
             "/register <имя> <фамилия> [отчество] <почта> <пароль> - регистрация\n"
             "/read_event <номер_события> - прочитать событие\n"
             "/edit_event <номер_события> <поле> <новое_значение> - редактировать событие\n"
             "/delete_event <номер_события> - удалить событие\n"
             "/sorted_events - <1> Показать все события в порядке возрастания <2> Показать все события в порядке убывания"
    )

@pytest.mark.asyncio
async def test_register_user_handler():
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    # Настраиваем mock-объекты
    mock_update.message = AsyncMock()
    mock_update.message.chat_id = 123
    mock_update.message.from_user.id = 123
    mock_update.message.text = "/register"
    mock_context.bot = AsyncMock()
    mock_context.bot.send_message = AsyncMock()

    result = await register_user_handler(mock_update, mock_context)

    # Проверяем что сообщение было отправлено
    mock_context.bot.send_message.assert_awaited_with(
        chat_id=123,
        text="Пожалуйста, введите ваше имя:"
    )
    assert result == 0 # FIRST_NAME

@pytest.mark.asyncio
async def test_create_event_handler():
    # Создаем mock-объекты для Update и ContextTypes
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    # Настраиваем mock-объекты
    mock_update.message = AsyncMock()
    mock_update.message.chat_id = 123
    mock_update.message.from_user.id = 123
    mock_update.message.text = "/create_event TestEvent 2023-12-31 23:59 Details"
    mock_context.bot = AsyncMock()
    mock_context.bot.send_message = AsyncMock()
    mock_context.application.event_service.create_event = AsyncMock()

    # Вызываем функцию create_event_handler
    await create_event_handler(mock_update, mock_context)

    # Проверка что сообщение было отправлено
    mock_context.bot.send_message.assert_awaited_with(
        chat_id=123,
        text="Создано событие: TestEvent для пользователя: 123"
    )


