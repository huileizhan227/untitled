#!/usr/bin/env bash
echo "发现重复的topic名字"
echo arg1: file, arg2: oper id

cat $1 | sort | uniq | sort | awk -F "," -v oper=$2 '$1==oper{print $4}' | sort | uniq -c | sort
