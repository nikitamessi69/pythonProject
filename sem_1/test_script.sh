#! /bin/bash
RESULT=$(cat /etc/os-release)
if [[ $RESULT == *"22.04.2"* && $RESULT == *"jammy"* && $? == 0 ]];
then echo "SUCCESS"
else echo "FAIL"
fi
