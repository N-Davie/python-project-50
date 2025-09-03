# gendiff/formatters/stylish.py

def to_str(value, depth):
    indent = ' ' * (depth * 4)
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"{indent}{k}: {to_str(v, depth + 1)}")
        closing_indent = ' ' * ((depth - 1) * 4)
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    return str(value)


def format_diff(diff, depth=1):
    lines = []
    indent_size = depth * 4
    current_indent = ' ' * (indent_size - 2)
    for item in diff:
        key = item["key"]
        status = item["status"]

        if status == "added":
            val = to_str(item["value"], depth + 1)
            lines.append(f"{current_indent}+ {key}: {val}")
        elif status == "removed":
            val = to_str(item["value"], depth + 1)
            lines.append(f"{current_indent}- {key}: {val}")
        elif status == "changed":
            old_val = to_str(item["old_value"], depth + 1)
            new_val = to_str(item["new_value"], depth + 1)
            lines.append(f"{current_indent}- {key}: {old_val}")
            lines.append(f"{current_indent}+ {key}: {new_val}")
        elif status == "unchanged":
            val = to_str(item["value"], depth + 1)
            lines.append(f"{current_indent}  {key}: {val}")
        elif status == "nested":
            children = format_diff(item["children"], depth + 1)
            lines.append(f"{current_indent}  {key}: " + "{")
            lines.append(children)
            lines.append(' ' * indent_size + "}")
    return "\n".join(lines)


def format_diff_output(diff):
    return "{\n" + format_diff(diff, 1) + "\n}"
