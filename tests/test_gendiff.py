import pytest
import os
import json
import tempfile

from gendiff import load
from gendiff import diff_builder
from gendiff.formatters import stylish
from gendiff import gendiff

yaml = load.yaml
try:
    import yaml as pyyaml
except ImportError:
    pyyaml = None

# --- Тесты для load.py ---

@pytest.fixture
def json_file():
    data = {"key": "value"}
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as f:
        json.dump(data, f)
        f.flush()
        yield f.name
    os.remove(f.name)

@pytest.fixture
def yaml_file():
    if pyyaml is None:
        pytest.skip("PyYAML не установлен")
    data = {"key": "value"}
    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
        pyyaml.dump(data, f)
        f.flush()
        yield f.name
    os.remove(f.name)

def test_load_json(json_file):
    data = load.load_data(json_file)
    assert data == {"key": "value"}

def test_load_yaml(yaml_file):
    data = load.load_data(yaml_file)
    assert data == {"key": "value"}

def test_unsupported_extension():
    with tempfile.NamedTemporaryFile("w+", suffix=".unsupported", delete=False) as f:
        f.write("test")
        f.flush()
        path = f.name
    try:
        with pytest.raises(ValueError):
            load.load_data(path)
    finally:
        os.remove(path)

def test_yaml_importerror(monkeypatch):
    # Принудительно сбросить yaml в None
    monkeypatch.setattr(load, "yaml", None)
    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
        f.write("key: value")
        f.flush()
        path = f.name
    with pytest.raises(ImportError):
        load.load_data(path)
    os.remove(path)

# --- Тесты для diff_builder.py ---

def test_added_key():
    d1 = {}
    d2 = {"a": 1}
    diff = diff_builder.build_diff(d1, d2)
    assert diff == [{'key': 'a', 'status': 'added', 'value': 1}]

def test_removed_key():
    d1 = {"a": 1}
    d2 = {}
    diff = diff_builder.build_diff(d1, d2)
    assert diff == [{'key': 'a', 'status': 'removed', 'value': 1}]

def test_changed_value():
    d1 = {"a": 1}
    d2 = {"a": 2}
    diff = diff_builder.build_diff(d1, d2)
    assert diff == [{'key': 'a', 'status': 'changed', 'old_value': 1, 'new_value': 2}]

def test_unchanged_value():
    d1 = {"a": 1}
    d2 = {"a": 1}
    diff = diff_builder.build_diff(d1, d2)
    assert diff == [{'key': 'a', 'status': 'unchanged', 'value': 1}]

def test_nested_diff():
    d1 = {"a": {"b": 1}}
    d2 = {"a": {"b": 2}}
    diff = diff_builder.build_diff(d1, d2)
    assert diff == [
        {'key': 'a', 'status': 'nested', 'children': [
            {'key': 'b', 'status': 'changed', 'old_value': 1, 'new_value': 2}
        ]}
    ]

# --- Тесты для stylish.py ---

def test_to_str_primitives():
    assert stylish.to_str("hello") == '"hello"'
    assert stylish.to_str(True) == "true"
    assert stylish.to_str(False) == "false"
    assert stylish.to_str(None) == "null"
    assert stylish.to_str(123) == "123"

def test_to_str_dict_and_list():
    d = {"a": 1, "b": {"c": 2}}
    s = stylish.to_str(d)
    assert "a: 1" in s
    assert "c: 2" in s

    l = [1, 2, {"a": 3}]
    s = stylish.to_str(l)
    assert "1" in s
    assert "3" in s

def test_format_diff_output_simple():
    diff = [
        {'key': 'a', 'status': 'added', 'value': 1},
        {'key': 'b', 'status': 'removed', 'value': 2},
        {'key': 'c', 'status': 'changed', 'old_value': 3, 'new_value': 4},
        {'key': 'd', 'status': 'unchanged', 'value': 5},
        {'key': 'e', 'status': 'nested', 'children': [
            {'key': 'f', 'status': 'added', 'value': 6}
        ]}
    ]
    output = stylish.format_diff_output(diff)
    assert "+ a" in output
    assert "- b" in output
    assert "- c" in output and "+ c" in output
    assert "d:" in output
    assert "f" in output

# --- Тесты для gendiff.py ---

def test_generate_diff_integration(tmp_path):
    # Создадим два файла
    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"
    file1.write_text(json.dumps({"a": 1, "b": 2}))
    file2.write_text(json.dumps({"a": 1, "b": 3, "c": 4}))

    result = gendiff.generate_diff(str(file1), str(file2))
    # Результат должен содержать добавленные, изменённые и неизменённые ключи
    assert "+ c" in result
    assert "- b" in result
    assert "+ b" in result
    assert "a:" in result

def test_generate_diff_type_error(tmp_path):
    file1 = tmp_path / "file1.json"
    file1.write_text(json.dumps(["not", "a", "dict"]))
    file2 = tmp_path / "file2.json"
    file2.write_text(json.dumps({"a": 1}))

    with pytest.raises(TypeError):
        gendiff.generate_diff(str(file1), str(file2))
