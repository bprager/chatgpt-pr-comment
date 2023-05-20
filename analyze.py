import base64
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
    files_json_base64 = sys.argv[1]
    files_json = base64.b64decode(files_json_base64).decode("utf-8")
    files = json.loads(files_json)

    for file in files:
        analyze_file(file)
