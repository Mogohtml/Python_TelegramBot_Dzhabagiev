import pytest
from unittest.mock import AsyncMock, patch
from app.core.repositories.events import EventRepository
from app.infra.postgres.db import Database


@pytest.mark.asyncio
async def test_create_event_if_not_exists():
    # Создаем mock для Database
    mock_db = AsyncMock(spec=Database)
    mock_conn = AsyncMock()
    mock_db.connection.return_value.__aenter__.return_value = mock_conn

    # Создаем экземпляр EventRepository с mock-объектом
    event_repo = EventRepository(database=mock_db)

    # Вызываем метод create_event_if_not_exists
    await event_repo.create_event_if_not_exists(user_id=1, name="Test Event", date="2023-12-31", time="23:59",
                                                details="Test Details")

    # Проверяем, что метод execute был вызван с правильными аргументами
    mock_conn.execute.assert_awaited_once_with(
        "INSERT INTO events (name, date, time, details, user_id) VALUES ($1, $2, $3, $4, $5)",
        "Test Event", "2023-12-31", "23:59", "Test Details", 1
    )

@pytest.mark.asyncio
async def test_read_event():
    # Создаем mock для Database
    mock_db = AsyncMock(spec=Database)
    mock_conn = AsyncMock()
    mock_db.connection.return_value.__aenter__.return_value == mock_conn

    event_repo = EventRepository(database=mock_db)

    mock_conn.fetchrow.return_value = {
        "id": 1,
        "name": "Test Event",
        "date": "2023-12-31",
        "time": "23:59",
        "details": "Test Details",
        "user_id": 1
    }

    event = await event_repo.read_event(event_id=1, user_id=1)

    mock_conn.fetchrow.assert_awaited_once_with("SELECT * FROM events WHERE id = $1 AND user_id = $2", 1, 1)

    assert event == {
        "id": 1,
        "name": "Test Event",
        "date": "2023-12-31",
        "time": "23:59",
        "details": "Test Details",
        "user_id": 1
    }

@pytest.mark.asyncio
async def test_edit_event():
    # Создаем mock для Database
    mock_db = AsyncMock(spec=Database)
    mock_conn = AsyncMock()
    mock_db.connection.return_value.__aenter__.return_value = mock_conn

    # Создаем экземпляр EventRepository с mock-объектом
    event_repo = EventRepository(database=mock_db)

    # Вызываем метод edit_event
    await event_repo.edit_event(event_id=1, user_id=1, name="New Name", date="2023-12-30", time="23:58", details="New Details")

    # Проверяем, что метод execute был вызван с правильными аргументами
    mock_conn.execute.assert_awaited_once_with(
        "UPDATE events SET name = COALESCE($3, name), date = COALESCE($4, date), time = COALESCE($5, time), details = COALESCE($6, details) WHERE id = $1 AND user_id = $2",
        1, 1, "New Name", "2023-12-30", "23:58", "New Details"
    )

@pytest.mark.asyncio
async def test_delete_event():
    # Создаем mock для Database
    mock_db = AsyncMock(spec=Database)
    mock_conn = AsyncMock()
    mock_db.connection.return_value.__aenter__.return_value = mock_conn

    # Создаем экземпляр EventRepository с mock-объектом
    event_repo = EventRepository(database=mock_db)

    # Настраиваем mock для возврата тестовых данных
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "name": "Test Event",
        "date": "2023-12-31",
        "time": "23:59",
        "details": "Test Details"
    }

    # Вызываем метод delete_event
    event = await event_repo.delete_event(event_id=1, user_id=1)

    # Проверяем, что метод fetchrow был вызван с правильными аргументами
    mock_conn.fetchrow.assert_awaited_once_with("DELETE FROM events WHERE id = $1 AND user_id = $2 RETURNING *;", 1, 1)

    # Проверяем, что возвращенные данные корректны
    assert event == {
        "id": 1,
        "name": "Test Event",
        "date": "2023-12-31",
        "time": "23:59",
        "details": "Test Details"
    }

@pytest.mark.asyncio
async def test_display_event():
    # Создаем mock для Database
    mock_db = AsyncMock(spec=Database)
    mock_conn = AsyncMock()
    mock_db.connection.return_value.__aenter__.return_value = mock_conn

    # Создаем экземпляр EventRepository с mock-объектом
    event_repo = EventRepository(database=mock_db)

    # Настраиваем mock для возврата тестовых данных
    mock_conn.fetch.return_value = [
        {
            "id": 1,
            "name": "Test Event 1",
            "date": "2023-12-31",
            "time": "23:59",
            "details": "Test Details 1"
        },
        {
            "id": 2,
            "name": "Test Event 2",
            "date": "2023-12-30",
            "time": "23:58",
            "details": "Test Details 2"
        }
    ]

    # Вызываем метод display_event
    events = await event_repo.display_event(user_id=1, reverse=False)

    # Проверяем, что метод fetch был вызван с правильными аргументами
    mock_conn.fetch.assert_awaited_once_with("SELECT * FROM events WHERE user_id = $1 ORDER BY date ASC", 1)

    # Проверяем, что возвращенные данные корректны
    assert events == [
        {
            "id": 1,
            "name": "Test Event 1",
            "date": "2023-12-31",
            "time": "23:59",
            "details": "Test Details 1"
        },
        {
            "id": 2,
            "name": "Test Event 2",
            "date": "2023-12-30",
            "time": "23:58",
            "details": "Test Details 2"
        }
    ]

