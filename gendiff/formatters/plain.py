def build_path(path, key):
    return f"{path}.{key}" if path else key


def to_str(value):
    if isinstance(value, (dict, list)):
        return "[complex value]"
    if isinstance(value, str):
        return f"'{value}'"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def handle_added(item, current_path, lines):
    value_str = to_str(item["value"])
    lines.append(f"Property '{current_path}' was added with value: {value_str}")


def handle_removed(current_path, lines):
    lines.append(f"Property '{current_path}' was removed")


def handle_changed(item, current_path, lines):
    old_value_str = to_str(item["old_value"])
    new_value_str = to_str(item["new_value"])
    lines.append(
        f"Property '{current_path}' was updated. "
        f"From {old_value_str} to {new_value_str}"
    )


def iter_diff(items, lines, path=""):
    for item in items:
        key = item["key"]
        status = item["status"]
        current_path = build_path(path, key)

        if status == "added":
            handle_added(item, current_path, lines)
        elif status == "removed":
            handle_removed(current_path, lines)
        elif status == "changed":
            handle_changed(item, current_path, lines)
        elif status == "nested":
            iter_diff(item["children"], lines, current_path)


def format_diff(diff):
    lines = []
    iter_diff(diff, lines)
    return "\n".join(lines)
