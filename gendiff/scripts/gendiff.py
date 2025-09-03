#!/usr/bin/env python3

import argparse

from .load import load_data
from .diff_builder import build_diff

from gendiff.formatters.stylish import format_diff_output as format_stylish
from gendiff.formatters.plain import format_diff as format_plain
from gendiff.formatters.json import format_diff as format_json


def generate_diff(file_path1, file_path2, format_name="stylish"):
    data1 = load_data(file_path1)
    data2 = load_data(file_path2)

    if not isinstance(data1, dict):
        raise TypeError(f"Данные из файла {file_path1} должны быть словарем.")
    if not isinstance(data2, dict):
        raise TypeError(f"Данные из файла {file_path2} должны быть словарем.")

    diff_tree = build_diff(data1, data2)

    if format_name == "stylish":
        return format_stylish(diff_tree)
    elif format_name == "plain":
        return format_plain(diff_tree)
    elif format_name == "json":
        return format_json(diff_tree)
    else:
        raise ValueError(f"Неизвестный формат: {format_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare two configuration files and show a diff."
    )
    parser.add_argument("filepath1", help="Path to the first file")
    parser.add_argument("filepath2", help="Path to the second file")
    parser.add_argument(
        "--format", help="Формат вывода (stylish, plain)", default="stylish"
    )
    args = parser.parse_args()
    try:
        diff_result = generate_diff(args.filepath1, args.filepath2, args.format)
        print(diff_result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
