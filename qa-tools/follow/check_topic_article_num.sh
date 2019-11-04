echo "发现文章数<=num的topic比例"
echo arg1: file, arg2: num

cat $1 | sort | uniq | sort \
| awk -F "," -v num=$2 '\
BEGIN{sum=0;n=0;oper=0} \
{\
    if($1!=oper){ \
        if(oper!=0) print oper,n,sum,n/sum; \
        oper=$1;sum=0;n=0;\
    } \
    sum+=1; \
    if($5<=num)n+=1; \
} \
END{print n,sum,n/sum}'
