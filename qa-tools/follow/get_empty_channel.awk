#!/usr/bin/awk -f
BEGIN {
    FS=",";
}
$5<10{
if ($4!="follow") print $0;
}
