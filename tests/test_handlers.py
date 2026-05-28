import pytest
from app.validators import ShoppingItem, TodoItem


def test_todo_item_valid():
    item = TodoItem(id="abc", text="Buy milk", user_id=1, created_at="2026-01-01T00:00:00+00:00")
    assert item.text == "Buy milk"
    assert item.status == "pending"


def test_todo_item_text_too_long():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        TodoItem(id="abc", text="x" * 1001, user_id=1, created_at="2026-01-01T00:00:00+00:00")


def test_todo_item_empty_text():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        TodoItem(id="abc", text="", user_id=1, created_at="2026-01-01T00:00:00+00:00")


def test_shopping_item_valid():
    item = ShoppingItem(id="xyz", text="Хлеб", user_id=2, created_at="2026-01-01T00:00:00+00:00")
    assert item.text == "Хлеб"
    assert item.status == "pending"


def test_shopping_item_model_dump_keys():
    item = ShoppingItem(id="xyz", text="Молоко", user_id=2, created_at="2026-01-01T00:00:00+00:00")
    d = item.model_dump()
    assert set(d.keys()) == {"id", "text", "status", "user_id", "created_at", "deadline", "cost"}


def test_todo_item_model_dump_keys():
    item = TodoItem(id="abc", text="Task", user_id=1, created_at="2026-01-01T00:00:00+00:00")
    d = item.model_dump()
    assert set(d.keys()) == {"id", "text", "status", "user_id", "created_at", "deadline", "cost"}
