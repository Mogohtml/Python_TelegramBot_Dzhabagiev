import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from app.handlers.commands import uploading_button_callback


@pytest.mark.asyncio
async def test_export_json_callback():
    # Создаем mock-объекты для Update и ContextTypes
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.data = 'export_json'
    mock_context.bot = AsyncMock()
    mock_context.bot.send_document = AsyncMock()

    await uploading_button_callback(mock_update, mock_context)

    mock_context.bot.send_document.assert_awaited_once()


@pytest.mark.asyncio
async def test_export_csv_callback():
    # Создаем mock-объекты для Update и ContextTypes
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    # Настраиваем mock-объекты
    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.data = 'export_csv'
    mock_context.bot = AsyncMock()
    mock_context.bot.send_document = AsyncMock()

    # Вызываем функцию button_callback
    await uploading_button_callback(mock_update, mock_context)

    # Проверяем, что документ был отправлен
    mock_context.bot.send_document.assert_awaited_once()

