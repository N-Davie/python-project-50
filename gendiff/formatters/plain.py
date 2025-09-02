def format_diff(diff):
    lines = []

    def build_path(path, key):
        return f"{path}.{key}" if path else key

    def to_str(value):
        if isinstance(value, dict) or isinstance(value, list):
            return "[complex value]"
        elif isinstance(value, str):
            return f"'{value}'"
        elif value is None:
            return "null"
        elif isinstance(value, bool):
            return str(value).lower()
        else:
            return str(value)

    def handle_added(item, current_path):
        value_str = to_str(item["value"])
        lines.append(
            (
                f"Property '{current_path}' was added with value: "
                f"{value_str}"
            )
        )

    def handle_removed(current_path):
        lines.append(f"Property '{current_path}' was removed")

    def handle_changed(item, current_path):
        old_value_str = to_str(item["old_value"])
        new_value_str = to_str(item["new_value"])
        lines.append(
            f"Property '{current_path}' was updated. From {old_value_str} to {new_value_str}"
        )

    def iter_diff(items, path=""):
        for item in items:
            key = item["key"]
            status = item["status"]
            current_path = build_path(path, key)

            if status == "added":
                handle_added(item, current_path)
            elif status == "removed":
                handle_removed(current_path)
            elif status == "changed":
                handle_changed(item, current_path)
            elif status == "nested":
                iter_diff(item["children"], current_path)

    iter_diff(diff)
    return "\n".join(lines)
