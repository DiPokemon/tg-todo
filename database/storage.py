import asyncio
import json
from pathlib import Path

import aiofiles

DATA_FILE = Path(__file__).parent.parent / "data" / "data.json"

_lock: asyncio.Lock | None = None


def _get_lock() -> asyncio.Lock:
    global _lock
    if _lock is None:
        _lock = asyncio.Lock()
    return _lock


async def load_data() -> dict:
    if not DATA_FILE.exists():
        return {"chats": {}}
    async with aiofiles.open(DATA_FILE, mode="r", encoding="utf-8") as f:
        content = await f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"chats": {}}


async def save_data(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = DATA_FILE.with_suffix(".tmp")
    async with _get_lock():
        async with aiofiles.open(tmp_file, mode="w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))
        tmp_file.replace(DATA_FILE)


def ensure_chat(data: dict, chat_id: str) -> None:
    if chat_id not in data["chats"]:
        data["chats"][chat_id] = {"todo": [], "shopping": []}
