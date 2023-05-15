import sys
import openai
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def ask_chatgpt(base_content, diff, programming_language):
    prompt = f"""
Your task as an experience ```{programming_language}``` programmer is to \ 
review a pull request for this file with previous content as followed:
---
```{base_content}```
---
to which following diff file is supposed to be applied: 
---
```{diff}```
---
.
Comment on code quality of this pull request, \
any potential security risk \
and make suggestions how the code could be improved if such suggestions exit. \
Otherwise compliment the author on his code. \
Limit to 300 words. 
"""

    return get_completion(prompt)


if __name__ == "__main__":
    base_content = sys.argv[1]
    head_content = sys.argv[2]
    diff = sys.argv[3]
    programming_language = sys.argv[4]

    print(ask_chatgpt(base_content, diff, programming_language))