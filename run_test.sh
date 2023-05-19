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

# add any changes and push
git add .
git commit -m "\"$1\""
git push

# delete test branch, recreate it and switch to i
git br -D example_branch
git co -b example_branch

# create test file
mkdir -p examples
touch examples/main.py
cat examples/main.py << EOF
print("Hello world!")
EOF

# commit and push
git add .
git commit -m "\"test after $1\""
git push --set-upstream origin example_branch

# switch back to main
git co main
echo "Now start the pull request and observe the Github Action ..."
echo "Don't forget to merge and delete the branch after before making additional changes.)"

