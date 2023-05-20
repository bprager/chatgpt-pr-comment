import os
import sys


def analyze_file(file):
    print("Analyzing file:", file)


def analyze_diff(diff):
    print("Diff:")
    print(diff)


def analyze_files(temp_dir, added_files, modified_files=[], diff_files=[]):
    # Process added files
    print("Added files:", added_files)
    for file in added_files:
        if not file:
            continue
        file_path = os.path.join(temp_dir, file)
        analyze_file(file_path)

    # Process modified files
    print("Modified files:", modified_files)
    for file in modified_files:
        if not file:
            continue
        file_path = os.path.join(temp_dir, file)
        analyze_file(file_path)

    # Process diff files
    print("Diff files:", diff_files)
    for diff_file in diff_files:
        if not file:
            continue
        with open(os.path.join(temp_dir, diff_file), "r") as file:
            diff_content = file.read()
            analyze_diff(diff_content)


if __name__ == "__main__":
    temp_dir = sys.argv[1]
    added_files = sys.argv[2].split(",")
    modified_files = []
    diff_files = []
    if len(sys.argv) > 2:
        modified_files = sys.argv[2].split(",")
    if len(sys.argv) > 3:
        diff_files = sys.argv[3].split(",")

    analyze_files(temp_dir, added_files, modified_files, diff_files)
