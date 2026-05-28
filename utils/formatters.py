STATUS_ICONS: dict[str, str] = {
    "pending": "🔲",
    "completed": "✅",
    "bought": "🛒",
}


def format_todo_item(item: dict) -> str:
    icon = STATUS_ICONS.get(item["status"], "🔲")
    parts = [f"{icon} {item['text']}"]
    if item.get("deadline"):
        parts.append(f"📅 Дедлайн: {item['deadline']}")
    if item.get("cost") is not None:
        try:
            parts.append(f"💲 Цена: {float(item['cost']):.2f}")
        except Exception:
            parts.append(f"💲 Цена: {item['cost']}")
    return "\n".join(parts)


def format_shop_item(item: dict) -> str:
    icon = STATUS_ICONS.get(item["status"], "🔲")
    parts = [f"{icon} {item['text']}"]
    if item.get("deadline"):
        parts.append(f"📅 Дедлайн: {item['deadline']}")
    if item.get("cost") is not None:
        try:
            parts.append(f"💲 Цена: {float(item['cost']):.2f}")
        except Exception:
            parts.append(f"💲 Цена: {item['cost']}")
    return "\n".join(parts)
