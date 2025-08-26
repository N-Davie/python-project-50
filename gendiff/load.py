import os
import json

try:
    import yaml
except ImportError:
    yaml = None


def load_data(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    with open(file_path, 'r', encoding='utf-8') as f:
        if ext in ['.yaml', '.yml']:
            if yaml is None:
                raise ImportError("PyYAML не установлен.")
            return yaml.safe_load(f)
        elif ext == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Неподдерживаемый формат файла.")
