appName=$1
envName=$2
gitAddress=$3

gitName=`echo $gitAddress | awk -F / '{print$NF}' | awk -F . '{print$1}'`
 
root=`pwd`


cd  $root/codeDown/$appName/$envName/$gitName && bash start.sh 
