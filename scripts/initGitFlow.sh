#!/bin/sh
MBRANCH="develop"


if git show-ref --verify --quiet refs/heads/$MBRANCH;  test $? = 0  ; then
    echo "local branch $MBRANCH exists .. please rename/delete and rerun"
    echo "> git branch -m $MBRANCH <NEWNAME>"
    echo "or"
    echo "> git branch -d $MBRANCH"
    
    exit 1
else
    echo "branch $MBRANCH does not exist .. create"
    if git branch -a | grep -q "/$MBRANCH" ; then
	git branch --set-upstream $MBRANCH origin/$MBRANCH
    else
	git checkout -b $MBRANCH 
    fi
    echo 
fi

echo "Set git flow settings:"
git config gitflow.branch.master "master"
git config gitflow.branch.develop  "$MBRANCH"
git config gitflow.prefix.feature 'feature/'
git config gitflow.prefix.release 'release/'
git config gitflow.prefix.hotfix 'hotfix/'
git config gitflow.prefix.support 'support/'
git config gitflow.prefix.versiontag 'v'
git config --list | grep "gitflow."
echo ".. finished"

echo
echo " production branch is master, developing branch is $MBRANCH"
echo 