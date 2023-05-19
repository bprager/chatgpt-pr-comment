#!/usr/bin/env/bash
# set -x
# Check for a single argument
if [ $# -lt 1 ]; then
  echo "Error: Missing commit message. Exiting ..."
  exit 1
fi

# (note: requires sudo apt install expect)
if unbuffer gh pr list | grep -q 'no open pull requests'; then
echo "There are no open pull requests"
else
echo "There are open pull requests. Merge first. Exiting ..."
exit 1
fi

# run the test
git pull
 
# remove the file if it exists
if test -f "examples/main.py"; then
  git rm examples/main.py
fi

# add any changes
git add .
git commit -m "\"$1\""

# delete test branch, recreate it and switch to i
git br -D example_branch
git co -b example_branch

# create test file
touch example/main.py
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

# commit and push
git add .
git commit -m "\"test after $1\""
git push --set-upstream origin example_branch

# switch back to main
git co main
echo "Now start the pull request and observe the Github Action ..."
echo "Don't forget to merge and delete the branch after before making additional changes.)"

