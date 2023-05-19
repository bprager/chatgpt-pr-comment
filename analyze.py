import json
import sys


def analyze_file(file):
    print("Analyzing file:", file["file"])

    if "content" in file:
        print("Content:")
        print(file["content"])
    if "diff" in file:
        print("Diff:")
        print(file["diff"])

    # Perform your analysis on the file here


if __name__ == "__main__":
    files_json = sys.argv[1]
    if files_json:
        files = json.loads(files_json.replace("'", '"'))

    for file in files:
        analyze_file(file)
