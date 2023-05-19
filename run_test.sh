#!/usr/bin/env/bash

# Check for a single argument
if [ $# -lt 1 ]; then
  echo "Error: Missing commit message. Exiting ..."
  exit 1
fi

prlist=$(gh pr list)

if grep -q "no open pull requests" <<< "$output"; then
echo "There are no open pull requests"
else
echo "There are open pull requests. Merge first. Exiting ..."
exit 1
fi

# run the test
git pull
git rm examples/main.py
git add
git commit -m "$1"
git br -D example_branch
git co -b example_branch
cat example/main.py << EOF
# /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
import sys

def main():
    print("Hello World!")


if __name__ == "__main__":
    main()
EOF
git add .
git commit "test after $1"
git push --set-upstream origin example_branch
git co main
echo "Now start the pull request and observe the Github Action ..."
echo "Don't forget to merge and delete the branch after before making additional changes.)"

