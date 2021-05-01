INDIR="/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis"
GITDIR="/home/uschwar1/Dokumente/goettinger-klimabuendnis"

find ${INDIR} -type f -iname "*~"  -exec /bin/rm {} \;
cp -au ${INDIR}/* ${GITDIR}

ORIPATH=`echo $PATH`
cd ${GITDIR}
echo "provide commit message:"
read inp
if [[ ${inp} != "" ]]; then
  git add *
  git commit -m "${inp}"
  git push origin master
else
  echo "no commit without message"
fi

cd ${ORIPATH}
