import pytest
from unittest.mock import AsyncMock
from telegram import Update
from telegram.ext import ContextTypes
from app.handlers.commands import uploading_button_callback

@pytest.mark.asyncio
async def test_button_callback_export_json():
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    # Настраиваем mock-объекты
    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.data = 'export_json'
    mock_context.bot = AsyncMock()
    mock_context.bot.send_document = AsyncMock()

    # Вызываем функцию button_callback
    await uploading_button_callback(mock_update, mock_context)

    # Проверяем, что документ был отправлен
    mock_context.bot.send_document.assert_awaited_once()