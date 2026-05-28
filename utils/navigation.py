from collections import defaultdict

_nav_stacks = defaultdict(list)


def reset(chat_id: str, root: str = "main") -> None:
    """Reset navigation stack for chat to root."""
    _nav_stacks[chat_id] = [root]


def push(chat_id: str, page: str) -> None:
    """Push a new page onto the chat stack."""
    _nav_stacks[chat_id].append(page)


def pop(chat_id: str):
    """Pop current page and return new current page or None."""
    stack = _nav_stacks.get(chat_id, [])
    if not stack:
        return None
    # remove current
    stack.pop()
    if not stack:
        return None
    return stack[-1]


def current(chat_id: str):
    stack = _nav_stacks.get(chat_id, [])
    return stack[-1] if stack else None
