#!/usr/bin/env python3

import argparse
from .load import load_data
from .diff_builder import build_diff
from .formatters.stylish import format_diff_output

def generate_diff(file_path1, file_path2):
    data1 = load_data(file_path1)
    data2 = load_data(file_path2)

    if not isinstance(data1, dict):
        raise TypeError(f"Данные из файла {file_path1} должны быть словарем.")
    if not isinstance(data2, dict):
        raise TypeError(f"Данные из файла {file_path2} должны быть словарем.")

    diff_tree = build_diff(data1, data2)
    return format_diff_output(diff_tree)

def main():
    parser = argparse.ArgumentParser(
        description='Compare two configuration files and show a diff.'
    )
    parser.add_argument('filepath1', help='Path to the first file')
    parser.add_argument('filepath2', help='Path to the second file')
    args = parser.parse_args()

    try:
        diff_result = generate_diff(args.filepath1, args.filepath2)
        print(diff_result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
