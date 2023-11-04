from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from storeapi.main import app
from storeapi.routers.post import post_table, comment_table


@pytest.fixture(scope="session")
def anyio_backend():
    """
    This fixture ensures that runs once for the the entire test session"""
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    """
    This is a test client. This is what we are going
    to interact with instead of the main server"""
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def clear_db_tables() -> AsyncGenerator:
    """
    This ensures that our test database table is empty
    NOTE: The autouse=True ensures that this fixture runs on every test
    """
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
