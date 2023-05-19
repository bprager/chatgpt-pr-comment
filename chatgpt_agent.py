import argparse
import os

import openai
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

# model="gpt-4"
# model="gpt-3.5-turbo"
# model="da-vinci-codex"


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    response = response.choices[0].message["content"]


def ask_chatgpt(mode, old_content, new_content, programming_language):
    print("askchatgpt")
    prompt_modified = f"""
Your task as an experience ```{programming_language}``` programmer is to \ 
review a pull request to replace following code:
---
```{old_content}```
---
which following new code:
---
```{new_content}```
---
. Focus on the changes made by the diff file.
"""

    prompt_added = f"""
Your task as an experience ```{programming_language}``` programmer is to \ 
review a pull request for adding this source code:
---
```{new_content}```
---
.
"""

    prompt = prompt_modified if mode == "MODIFIED" else prompt_added
    prompt += """
Comment next on code quality of this pull request, \
any potential security risk if they exist. \
Make suggestions how the code could be improved if there are any. \
Otherwise compliment the author on his code. \
Limit to 300 words. 
"""

    return get_completion(prompt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="File name")
    parser.add_argument("--old-file", help="Old file content")
    parser.add_argument("--diff-file", help="Old file content")
    args = parser.parse_args()

    filename = args.file
    with open(filename, "r") as f:
        content = f.read()
    if args.diff_file:
        with open(args.diff_file, "r") as f:
            diff = f.read()
    if args.old_file:
        with open(args.old_file, "r") as f:
            old_content = f.read()

    languages = {".py": "Python", ".java": "Java", ".cpp": "C++", ".js": "JavaScript"}
    _, extension = os.path.splitext(filename)

    if extension in languages:
        if content is None:
            print(ask_chatgpt("MODIFIED", old_content, content, languages[extension]))
        else:
            print(ask_chatgpt("ADDED", "", content, languages[extension]))


if __name__ == "__main__":
    main()
