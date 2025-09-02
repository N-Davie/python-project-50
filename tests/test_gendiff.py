import pytest
import os
import json
import tempfile
import sys

from gendiff import load
from gendiff import diff_builder
from gendiff.formatters import stylish
from gendiff import gendiff

yaml = load.yaml
try:
    import yaml as pyyaml
except ImportError:
    pyyaml = None


# --- Фикстуры ---

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


# --- Тесты для load.py ---

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

def test_load_invalid_json(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{ invalid json }")
    with pytest.raises(json.JSONDecodeError):
        load.load_data(str(file))

def test_load_invalid_yaml(tmp_path):
    if pyyaml is None:
        pytest.skip("PyYAML не установлен")
    file = tmp_path / "bad.yaml"
    file.write_text("key: [unclosed")
    with pytest.raises(pyyaml.YAMLError):
        load.load_data(str(file))


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
    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"
    file1.write_text(json.dumps({"a": 1, "b": 2}))
    file2.write_text(json.dumps({"a": 1, "b": 3, "c": 4}))

    result = gendiff.generate_diff(str(file1), str(file2))
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

def test_generate_diff_plain_format(tmp_path):
    file1 = tmp_path / "f1.json"
    file2 = tmp_path / "f2.json"
    file1.write_text(json.dumps({"x": 1}))
    file2.write_text(json.dumps({"x": 2, "y": 3}))
    result = gendiff.generate_diff(str(file1), str(file2), format_name="plain")
    assert "Property 'x' was updated" in result
    assert "Property 'y' was added" in result

def test_generate_diff_unknown_format(tmp_path):
    file1 = tmp_path / "f1.json"
    file2 = tmp_path / "f2.json"
    file1.write_text(json.dumps({"a": 1}))
    file2.write_text(json.dumps({"a": 2}))
    with pytest.raises(ValueError):
        gendiff.generate_diff(str(file1), str(file2), format_name="unknown")

def test_main_stylish_and_plain(monkeypatch, tmp_path, capsys):
    file1 = tmp_path / "f1.json"
    file2 = tmp_path / "f2.json"
    file1.write_text(json.dumps({"a": 1}))
    file2.write_text(json.dumps({"a": 2, "b": 3}))

    # stylish
    monkeypatch.setattr(sys, "argv", ["gendiff", str(file1), str(file2), "--format", "stylish"])
    gendiff.main()
    out, _ = capsys.readouterr()
    assert "{", "}" in out
    assert "+ b" in out

    # plain
    monkeypatch.setattr(sys, "argv", ["gendiff", str(file1), str(file2), "--format", "plain"])
    gendiff.main()
    out, _ = capsys.readouterr()
    assert "Property 'b' was added" in out

def test_main_handles_exception(monkeypatch, capsys, tmp_path):
    f1 = tmp_path / "bad1.json"
    f2 = tmp_path / "bad2.json"
    f1.write_text(json.dumps([1, 2, 3]))
    f2.write_text(json.dumps([4, 5]))

    monkeypatch.setattr(sys, "argv", ["gendiff", str(f1), str(f2)])
    gendiff.main()
    out, _ = capsys.readouterr()
    assert "Error:" in out


# --- Тесты для json-форматтера ---

def test_generate_diff_json_format(tmp_path):
    file1 = tmp_path / "f1.json"
    file2 = tmp_path / "f2.json"
    file1.write_text(json.dumps({"x": 1}))
    file2.write_text(json.dumps({"x": 2, "y": 3}))

    result = gendiff.generate_diff(str(file1), str(file2), format_name="json")

    parsed = json.loads(result)
    assert isinstance(parsed, list)
    keys = {item["key"] for item in parsed}
    assert "x" in keys
    assert "y" in keys

def test_generate_diff_json_nested(tmp_path):
    file1 = tmp_path / "f1.json"
    file2 = tmp_path / "f2.json"
    file1.write_text(json.dumps({"a": {"b": 1}}))
    file2.write_text(json.dumps({"a": {"b": 2}}))

    result = gendiff.generate_diff(str(file1), str(file2), format_name="json")
    parsed = json.loads(result)

    assert parsed[0]["key"] == "a"
    assert parsed[0]["status"] == "nested"
    assert isinstance(parsed[0]["children"], list)
    assert parsed[0]["children"][0]["status"] == "changed"

def test_main_with_json(monkeypatch, tmp_path, capsys):
    file1 = tmp_path / "f1.json"
    file2 = tmp_path / "f2.json"
    file1.write_text(json.dumps({"a": 1}))
    file2.write_text(json.dumps({"a": 2}))

    monkeypatch.setattr(sys, "argv", ["gendiff", str(file1), str(file2), "--format", "json"])
    gendiff.main()
    out, _ = capsys.readouterr()

    parsed = json.loads(out)
    assert isinstance(parsed, list)
    assert parsed[0]["key"] == "a"
    assert parsed[0]["status"] == "changed"


