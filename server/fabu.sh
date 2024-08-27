appName=$1
envName=$2
gitAddress=$3
gitCommit=$4

gitName=`echo $gitAddress | awk -F / '{print$NF}' | awk -F . '{print$1}'`
 
root=`pwd`

mkdir -p codeDown/$appName/$envName/

if [ -f $root/logs/$appName-$envName-down.log ] ; then 
  :
else 
   cd $root/logs && touch $appName-$envName-down.log
fi

if [ -f $root/logs/$appName-$envName-fabu.log ] ; then 
  :
else 
   cd $root/logs && touch $appName-$envName-fabu.log
fi


if [ -d  $root/codeDown/$appName/$envName/$gitName ]; then
   cd $root/codeDown/$appName/$envName/$gitName
   ###切换到master分支, git pull 拉取最新tag 
   git checkout master && git pull 
   ## 切换目标分支，拉取最新代码
   git checkout $gitCommit && git pull > $root/logs/$appName-$envName-down.log 
 
else
   cd  $root/codeDown/$appName/$envName/ && git clone $gitAddress && cd $gitName && git checkout $gitCommit > $root/logs/$appName-$envName-down.log  
fi



cp devops/$appName/$envName/fabu.sh .

bash  fabu.sh > $root/logs/$appName-$envName-fabu.log  

