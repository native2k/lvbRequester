#!/bin/bash
CBRANCH=`git rev-parse --abbrev-ref HEAD`


if echo $CBRANCH | grep -q 'release/' || echo $CBRANCH | grep -q "hotfix/" ; then 
    version=`echo $CBRANCH | cut -d "/" -f2`
#if true; then
#    version='0.0.0'

    echo "bump to version $version"
    NVERSION="\'$version\'"
    TODAY=`date +%Y-%m-%d`
     read -p 'What changed: ' changes
    sed -i "s/\(__version__\s*=\s*\)[\'0-9\.]\+/\1$NVERSION/" supervisorserialrestart/__init__.py
    sed -i "s/\(version\s*=\s*\)[\'0-9\.]\+/\1$NVERSION/" setup.py
    sed -i "/^-------/a * $version ($TODAY)\n    * $changes\n" HISTORY.rst
    
    echo "Files modified, if necessary plz check changes and commit"
    echo "\$>git diff"    
    echo "\$> git commit supervisorserialrestart/__init__.py setup.py HISTORY.rst -m \'bump to version $version\'"

else
    echo "!!! you are not on an release or hotfix branch .. can not bump version"
    exit 1
fi    