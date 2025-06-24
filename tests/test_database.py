import pytest
from unittest.mock import AsyncMock, patch
from app.infra.postgres.db import Database
from pydantic import PostgresDsn

@pytest.mark.asyncio
async def test_database_connections():
    # Создаем mock для PostgresDsn
    mock_dsn = PostgresDsn("postgresql://postgres:12345@localhost:5432/calendar")

    db = Database(mock_dsn)

    # Используем patch для имитации успешное подключения
    with patch('asyncpg.create_pool', new_callable=AsyncMock) as mock_create_pool:
        await db.initialize()
        mock_create_pool.assert_awaited_once_with(str(mock_dsn.get_secret_value()))


@pytest.mark.asyncio
async def test_database_connection_error():
    # Создаем mock для PostgresDsn
    mock_dsn = PostgresDsn("postgresql://user:password@localhost:5432/dbname")

    # Создаем экземпляр Database с mock-объектом
    db = Database(mock_dsn)

    # Используем patch для имитации ошибки подключения
    with patch('asyncpg.create_pool', side_effect=Exception("Connection failed")) as mock_create_pool:
        with pytest.raises(Exception) as extinfo:
            await db.initialize()
        assert "Connection failed" in str(extinfo.value)
