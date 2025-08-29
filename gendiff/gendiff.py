#!/usr/bin/env python3

import argparse
import json
from .load import load_data


def generate_diff(file_path1, file_path2):
    data1 = load_data(file_path1)
    data2 = load_data(file_path2)

    if not isinstance(data1, dict):
        raise TypeError(f"Данные из файла {file_path1} должны быть словарем.")
    if not isinstance(data2, dict):
        raise TypeError(f"Данные из файла {file_path2} должны быть словарем.")

    keys = sorted(data1.keys() | data2.keys())
    result_lines = []

    for key in keys:
        if key not in data1:
            result_lines.append(
                f"  + {key}: {json.dumps(data2[key], ensure_ascii=False)}"
            )
        elif key not in data2:
            result_lines.append(
                f"  - {key}: {json.dumps(data1[key], ensure_ascii=False)}"
            )
        else:
            if data1[key] == data2[key]:
                result_lines.append(
                    f"    {key}: {json.dumps(data1[key], ensure_ascii=False)}"
                )
            else:
                result_lines.append(
                    f"  - {key}: {json.dumps(data1[key], ensure_ascii=False)}"
                )
                result_lines.append(
                    f"  + {key}: {json.dumps(data2[key], ensure_ascii=False)}"
                )

    return "{\n" + "\n".join(result_lines) + "\n}"


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
