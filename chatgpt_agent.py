import sys


def process_diff(base_content, head_content, diff, programming_language):
    # This is where you would add your own logic.
    # For now, we will just return the number of lines and the detected language.
    base_lines = len(base_content.split("\n")) if base_content else 0
    head_lines = len(head_content.split("\n")) if head_content else 0
    diff_lines = len(diff.split("\n")) if diff else 0

    return f"Base content has {base_lines} lines, head content has {head_lines} lines, diff has {diff_lines} lines. Detected language: {programming_language}."


if __name__ == "__main__":
    base_content = sys.argv[1]
    head_content = sys.argv[2]
    diff = sys.argv[3]
    programming_language = sys.argv[4]

    print(process_diff(base_content, head_content, diff, programming_language))

