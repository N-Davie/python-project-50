#!/usr/bin/env python3

import argparse
import json


def generate_diff(file_path1, file_path2):
    with open(file_path1) as f:
        data1 = json.load(f)
    with open(file_path2) as f:
        data2 = json.load(f)

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

    return "{\n" + "\n".join(result_lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('filepath1')
    parser.add_argument('filepath2')
    args = parser.parse_args()

    diff_result = generate_diff(args.filepath1, args.filepath2)
    print(diff_result)


if __name__ == "__main__":
    main()
