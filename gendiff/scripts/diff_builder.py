def build_diff(d1, d2):
    diff = []
    keys = sorted(set(d1.keys()) | set(d2.keys()))
    for key in keys:
        if key not in d1:
            diff.append({"key": key, "status": "added", "value": d2[key]})
        elif key not in d2:
            diff.append({"key": key, "status": "removed", "value": d1[key]})
        else:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                children = build_diff(d1[key], d2[key])
                diff.append(
                    {"key": key, "status": "nested", "children": children}
                )
            elif d1[key] != d2[key]:
                diff.append(
                    {
                        "key": key,
                        "status": "changed",
                        "old_value": d1[key],
                        "new_value": d2[key],
                    }
                )
            else:
                diff.append(
                    {"key": key, "status": "unchanged", "value": d1[key]}
                )
    return diff
