if [[ $2 == "" ]]; then
	echo "usage: $0 oriString replaceString"
	exit 1
fi

origStr=$1
replStr=$2

echo "#########"
echo " Preview"
echo "#########"
for i in `grep -r ${origStr} content/ |cut -d " " -f 1`
do 
	j=`echo ${i}|cut  -f 1 -d ':'`
	k=`echo ${i}|cut  -f 2 -d ':'`
	l=${j}:${k}
	echo ${l}
	sed "s/${origStr}/${replStr}/g" ${l} | grep ${replStr} 
done

echo "#########"
echo " Change?"
echo "#########"
read ans
if [[ ${ans} == "y" ]]; then
	for i in `grep -r ${origStr} content/ |cut -d " " -f 1`
	do 
		j=`echo ${i}|cut  -f 1 -d ':'`
		k=`echo ${i}|cut  -f 2 -d ':'`
		l=${j}:${k}
		echo ${l}
		sed -i "s/${origStr}/${replStr}/g" ${l} 
	done
fi
