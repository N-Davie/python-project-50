import pytest
from gendiff.gendiff import generate_diff

json_full = 'tests/fixtures/file1.json'
json_some_equall = 'tests/fixtures/file2.json'
json_full_anotherkeys = 'tests/fixtures/file3.json'
json_empty = 'tests/fixtures/file4.json'


def generate_diff(json_full, json_some_equall):
   assert "{\n" + "\n".join(result_lines) + "\n}"
