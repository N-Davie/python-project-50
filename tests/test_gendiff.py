import pytest
from gendiff.gendiff import generate_diff

json_full = 'tests/fixtures/file1_test.json'
json_some_equall = 'tests/fixtures/file2_test.json'
json_full_anotherkeys = 'tests/fixtures/file3_test.json'
json_empty = 'tests/fixtures/file4_test.json'
yaml_full = 'tests/fixtures/file1_test.yaml'
yaml_some_equall = 'tests/fixtures/file2_test.yaml'
yaml_full_anotherkeys = 'tests/fixtures/file3_test.yaml'
yaml_empty = 'tests/fixtures/file4_test.yaml'

def test_generate_diff_with_pare():
    result = generate_diff(json_full, json_some_equall)
    expected = """{
    age: 17
  - best_friend: "Ron"
  + best_friend: "books"
    faculty: "Griffindor"
  + hobby: "help house elfs"
  - name: "harry"
  + name: "hermione"
    school: "hogwards"
}"""
    assert result == expected


def test_generate_diff_without_pare():
    result = generate_diff(json_full, json_full_anotherkeys)
    expected = """{
  - age: 17
  - best_friend: "Ron"
  + best_friend: "books"
  + character: "cunning"
  + dinasty: 1000
  - faculty: "Griffindor"
  + family: "Malfoy"
  - name: "harry"
  + passion: "dark magic"
  - school: "hogwards"
}"""
    assert result == expected


def test_generate_diff_with_empty():
    result = generate_diff(json_full, json_empty)
    expected = """{
  - age: 17
  - best_friend: "Ron"
  - faculty: "Griffindor"
  - name: "harry"
  - school: "hogwards"
}"""
    assert result == expected

def test_generate_diff_with_pare():
    result = generate_diff(yaml_full, yaml_some_equall)
    expected = """{
    age: 17
  - best_friend: "Ron"
  + best_friend: "books"
    faculty: "Griffindor"
  + hobby: "help house elfs"
  - name: "harry"
  + name: "hermione"
    school: "hogwards"
}"""
    assert result == expected


def test_generate_diff_without_pare():
    result = generate_diff(yaml_full, yaml_full_anotherkeys)
    expected = """{
  - age: 17
  - best_friend: "Ron"
  + best_friend: "books"
  + character: "cunning"
  + dinasty: 1000
  - faculty: "Griffindor"
  + family: "Malfoy"
  - name: "harry"
  + passion: "dark magic"
  - school: "hogwards"
}"""
    assert result == expected


def test_generate_diff_with_empty():
    result = generate_diff(yaml_full, yaml_empty)
    expected = """{
  - age: 17
  - best_friend: "Ron"
  - faculty: "Griffindor"
  - name: "harry"
  - school: "hogwards"
}"""
    assert result == expected