import argparse
import os
import requests
import openai

task_prompt = """
Comment next on code quality of this pull request, \
any potential security risk if they exist. \
Make suggestions how the code could be improved if there are any. \
Otherwise compliment the author on his code. \
Limit to 300 words. 
"""

# gpt-3.5-turbo, (gtp-4 not available from GitHub as of 06-05-23)
def get_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def pr_comment(body: str) -> None:
    print(f'GITHUB_REPOSITORY={os.environ["GITHUB_REPOSITORY"]}')
    print(f'GITHUB_REF = {os.environ["GITHUB_REF"]}')

    # Access repository and owner
    repo = os.environ["GITHUB_REPOSITORY"]
    owner = repo.split("/")[0]
    # Access pull request number
    pull_request_number = os.environ["GITHUB_REF"].split("/")[2]

    api_url = (
        f"https://api.github.com/repos/{repo}/issues/{pull_request_number}/comments"
    )
    print(f"API URL: {api_url}")

    token = os.environ["GITHUB_TOKEN"]

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"body": body}
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 201:
        print("Comment submitted successfully!")
    else:
        print(f"Failed to submit comment. Status code: {response.status_code}.")
        print(response.text)


def analyze_added_file(file: str, language: str) -> None:
    print(f"analyze_added_file: {file}, language: {language}")
    with open(file, "r") as f:
        content = f.read()
    print(f"Content: {content}")
    prompt = (
        f"""
Your task as an experience ```{language}``` programmer is to \ 
review a pull request for adding this source code:
---
```{content}```
---
. 
"""
        + task_prompt
    )
    print(f"Prompt: {prompt}")
    completion = get_completion(prompt)
    pr_comment(f"ChatGPT commented:\n{completion}")


def analyze_modified_file(file: str, diff_file: str, language: str) -> None:
    with open(diff_file, "r") as f:
        diff_content = f.read()
    with open(file, "r") as f:
        content = f.read()
    prompt = (
        f"""
Your task as an experience ```{language}``` programmer is to \ 
review a pull request to add following change:
---
```{diff_content}```
---
to this code:
---
```{content}```
---
. Focus on the changes made by the diff file.
"""
        + task_prompt
    )
    completion = get_completion(prompt)
    pr_comment(f"ChatGPT commented:\n{completion}")


def analyze_files(
    temp_dir: str,
    added_files: list[str] = [],
    modified_files: list[str] = [],
    diff_files: list[str] = [],
):
    # languages we proceed with
    languages = {
        ".py": "Python",
        ".java": "Java",
        ".cpp": "C++",
        ".js": "JavaScript",
    }
    print("Added files:", added_files)
    for file in added_files:
        print("File:", file)
        file_path = os.path.join(temp_dir, file)
        base_name, extension = os.path.splitext(file_path)
        if (
            os.path.isfile(file_path)
            and os.access(file_path, os.R_OK)
            and not os.path.isdir(file_path)
            and extension in languages
        ):
            analyze_added_file(file_path, languages[extension])

    if not modified_files:
        modified_files = []
    # Process modified files
    print("Modified files:", modified_files)
    for file in modified_files:
        file_path = os.path.join(temp_dir, file)
        base_name, extension = os.path.splitext(file_path)
        diff_file_path = base_name + ".diff"
        if (
            os.path.isfile(file_path)
            and os.access(file_path, os.R_OK)
            and not os.path.isdir(file_path)
            and os.path.isfile(diff_file_path)
            and os.access(diff_file_path, os.R_OK)
            and not os.path.isdir(diff_file_path)
            and extension in languages
        ):
            analyze_modified_file(file_path, diff_file_path, languages[extension])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--temp-dir", help="Temp directory")
    parser.add_argument("--added", help="Added files")
    parser.add_argument("--modified", help="Modified files")
    parser.add_argument("--diffs", help="Diff files")
    args = parser.parse_args()
    temp_dir = args.temp_dir
    added_files = args.added.split(" ")
    modified_files = args.modified.split(" ")
    diff_files = args.diffs.split(" ")

    analyze_files(temp_dir, added_files, modified_files, diff_files)
