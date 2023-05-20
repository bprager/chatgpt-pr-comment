import argparse
import os
import sys


def analyze_file(file):
    print("Analyzing file:", file)


def analyze_diff(diff):
    print("Diff:")
    print(diff)


def analyze_files(temp_dir, added_files, modified_files=[], diff_files=[]):
    # Process added files
    if not added_files:
        added_files = []
    print("Added files:", added_files)
    for file in added_files:
        print("File:", file)
        file_path = os.path.join(temp_dir, file)
        print(f"isfile: {os.path.isfile(file_path)}")
        print(f"is readable: {os.access(file_path, os.R_OK)}")
        print(f"is dir: {os.path.isdir(file_path)}")
        if (
            os.path.isfile(file_path)
            and os.access(file_path, os.R_OK)
            and not os.path.isdir(file_path)
        ):
            analyze_file(file_path)

    if not modified_files:
        modified_files = []
    # Process modified files
    print("Modified files:", modified_files)
    for file in modified_files:
        file_path = os.path.join(temp_dir, file)
        if (
            os.path.isfile(file_path)
            and os.access(file_path, os.R_OK)
            and not os.path.isdir(file_path)
        ):
            analyze_file(file_path)

    # Process diff files
    if not diff_files:
        diff_files = []
    print("Diff files:", diff_files)
    for diff_file in diff_files:
        diff_file_path = os.path.join(temp_dir, diff_file)
        if (
            os.path.isfile(diff_file_path)
            and os.access(diff_file_path, os.R_OK)
            and not os.path.isdir(diff_file_path)
        ):
            with open(diff_file_path, "r") as file:
                diff_content = file.read()
                analyze_diff(diff_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--temp-dir", help="Temp directory")
    parser.add_argument("--added", help="Added files")
    parser.add_argument("--modified", help="Modified files")
    parser.add_argument("--diffs", help="Diff files")
    args = parser.parse_args()
    temp_dir = args.temp_dir
    added_files = args.added
    modified_files = args.modified
    diff_files = args.diffs

    analyze_files(temp_dir, added_files, modified_files, diff_files)
