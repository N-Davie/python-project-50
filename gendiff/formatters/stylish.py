def to_str(value, indent=0):
    indent_str = " " * indent
    indent_inner = " " * (indent + 4)

    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        for k, v in value.items():
            lines.append(f"{indent_inner}{k}: {to_str(v, indent + 4)}")
        lines.append(f"{indent_str}}}")
        return "\n".join(lines)
    elif isinstance(value, list):
        if not value:
            return "[]"
        lines = ["["]
        for item in value:
            lines.append(f"{indent_inner}{to_str(item, indent + 4)}")
        lines.append(f"{indent_str}]")
        return "\n".join(lines)
    elif isinstance(value, str):
        return f'"{value}"'
    elif value is None:
        return "null"
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def format_diff(diff, indent=0):
    lines = []
    indent_str = " " * indent

    for item in diff:
        key = item["key"]
        status = item["status"]

        if status == "added":
            val_str = to_str(item["value"], indent + 4)
            lines.append(f"{indent_str}  + {key}: {val_str} # Добавлена")
        elif status == "removed":
            val_str = to_str(item["value"], indent + 4)
            lines.append(f"{indent_str}  - {key}: {val_str} # Удалена")
        elif status == "changed":
            old_val_str = to_str(item["old_value"], indent + 4)
            new_val_str = to_str(item["new_value"], indent + 4)
            lines.append(
                f"{indent_str}  - {key}: {old_val_str} # Старое значение"
            )
            lines.append(
                f"{indent_str}  + {key}: {new_val_str} # Новое значение"
            )
        elif status == "unchanged":
            val_str = to_str(item["value"], indent + 4)
            lines.append(f"{indent_str}    {key}: {val_str}")
        elif status == "nested":
            lines.append(f"{indent_str}    {key}: {{")
            lines.extend(format_diff(item["children"], indent + 4))
            lines.append(f"{indent_str}    }}")

    return lines


def format_diff_output(diff):
    lines = ["{"]
    lines.extend(format_diff(diff, indent=4))
    lines.append("}")
    return "\n".join(lines)
