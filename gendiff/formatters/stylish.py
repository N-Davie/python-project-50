def to_str(value, depth=0):
    indent = ' ' * (depth * 4)
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for k, v in value.items():
            lines.append(f"{indent}    {k}: {to_str(v, depth + 1)}")
        return "{\n" + "\n".join(lines) + f"\n{indent}}}"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    return str(value)  # строки теперь без кавычек


def format_diff(diff, depth=0):
    lines = []
    indent = ' ' * (depth * 4)
    for item in diff:
        key = item["key"]
        status = item["status"]

        if status == "added":
            val = to_str(item["value"], depth + 1)
            lines.append(f"{indent}  + {key}: {val}")
        elif status == "removed":
            val = to_str(item["value"], depth + 1)
            lines.append(f"{indent}  - {key}: {val}")
        elif status == "changed":
            old_val = to_str(item["old_value"], depth + 1)
            new_val = to_str(item["new_value"], depth + 1)
            lines.append(f"{indent}  - {key}: {old_val}")
            lines.append(f"{indent}  + {key}: {new_val}")
        elif status == "unchanged":
            val = to_str(item["value"], depth + 1)
            lines.append(f"{indent}    {key}: {val}")
        elif status == "nested":
            children = format_diff(item["children"], depth + 1)
            lines.append(f"{indent}    {key}: {{")
            lines.append(children)
            lines.append(f"{indent}    }}")
    return "\n".join(lines)


def format_diff_output(diff):
    """Главная функция для stylish, возвращает строку всего diff."""
    return "{\n" + format_diff(diff, 0) + "\n}"
