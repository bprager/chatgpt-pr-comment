import argparse
import logging
import os
import sys

import openai
from dotenv import find_dotenv, load_dotenv

# setup logger
logger = logging.getLogger(__name__)
stoh = logging.StreamHandler(sys.stdout)
fmth = logging.Formatter(
    "%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
)
stoh.setFormatter(fmth)
logger.addHandler(stoh)
logger.setLevel(logging.DEBUG)

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
    return response.choices[0].message["content"]


def ask_chatgpt(mode, old_content, new_content, programming_language):
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
    logging.debug("Starting chatgpt_agent.py")
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="File name")
    parser.add_argument("--content", help="File content")
    parser.add_argument("--old-content", help="Old file content")
    parser.add_argument("--new-content", help="New file content")
    args = parser.parse_args()

    filename = args.file
    content = args.content
    old_content = args.old_content
    new_content = args.new_content
    languages = {"py": "Python", "java": "Java", "cpp": "C++", "js": "JavaScript"}
    _, extension = os.path.splitext(filename)

    if extension in languages:
        if content is None:
            mode = "MODIFIED"
            print(ask_chatgpt(mode, old_content, new_content, languages[extension]))
        else:
            print(ask_chatgpt(mode, "", content, languages[extension]))


if __name__ == "__main__":
    main()
