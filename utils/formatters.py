STATUS_ICONS: dict[str, str] = {
    "pending": "🔲",
    "completed": "✅",
    "bought": "🛒",
}


def format_todo_item(item: dict) -> str:
    icon = STATUS_ICONS.get(item["status"], "🔲")
    return f"{icon} {item['text']}"


def format_shop_item(item: dict) -> str:
    icon = STATUS_ICONS.get(item["status"], "🔲")
    return f"{icon} {item['text']}"
