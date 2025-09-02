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

    def iter_diff(items, path=""):
        for item in items:
            key = item["key"]
            status = item["status"]
            current_path = build_path(path, key)

            if status == "added":
                value_str = to_str(item["value"])
                lines.append(
                    f"Property '{current_path}' was added with value: {value_str}"
                )
            elif status == "removed":
                lines.append(f"Property '{current_path}' was removed")
            elif status == "changed":
                old_value_str = to_str(item["old_value"])
                new_value_str = to_str(item["new_value"])

                # Разбиваем длинную строку на части
                line_part1 = (
                    f"Property '{current_path}' was updated. From "
                    f"{old_value_str} to {new_value_str}"
                )
                lines.append(line_part1)
            elif status == "nested":
                iter_diff(item["children"], current_path)

    iter_diff(diff)
    return "\n".join(lines)
