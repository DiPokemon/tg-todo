import json
import pytest
import pytest_asyncio
from pathlib import Path
from unittest.mock import AsyncMock, mock_open, patch

from database.storage import ensure_chat, load_data, save_data


@pytest.mark.asyncio
async def test_load_data_missing_file():
    with patch("database.storage.DATA_FILE") as mock_path:
        mock_path.exists.return_value = False
        result = await load_data()
    assert result == {"chats": {}}


@pytest.mark.asyncio
async def test_load_data_valid_json(tmp_path):
    data = {"chats": {"123": {"todo": [], "shopping": []}}}
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps(data), encoding="utf-8")

    with patch("database.storage.DATA_FILE", data_file):
        result = await load_data()

    assert result == data


@pytest.mark.asyncio
async def test_load_data_corrupted_json(tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("NOT VALID JSON", encoding="utf-8")

    with patch("database.storage.DATA_FILE", data_file):
        result = await load_data()

    assert result == {"chats": {}}


@pytest.mark.asyncio
async def test_save_data_creates_file(tmp_path):
    data_dir = tmp_path / "data"
    data_file = data_dir / "data.json"
    data = {"chats": {"42": {"todo": [{"id": "1", "text": "test"}], "shopping": []}}}

    with patch("database.storage.DATA_FILE", data_file):
        with patch("database.storage._lock", None):
            await save_data(data)

    assert data_file.exists()
    saved = json.loads(data_file.read_text(encoding="utf-8"))
    assert saved == data


def test_ensure_chat_creates_entry():
    data: dict = {"chats": {}}
    ensure_chat(data, "99")
    assert "99" in data["chats"]
    assert data["chats"]["99"] == {"todo": [], "shopping": []}


def test_ensure_chat_does_not_overwrite():
    data: dict = {"chats": {"99": {"todo": [{"id": "x"}], "shopping": []}}}
    ensure_chat(data, "99")
    assert data["chats"]["99"]["todo"] == [{"id": "x"}]
