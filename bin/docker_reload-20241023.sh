UDIR="/home/gkb_user"
PDIR=${UDIR}/"goettinger-klimabuendnis"
DDIR=${UDIR}/"/Docker/nginx-latest"
HUGO=${UDIR}"/bin/hugo"
TAG="goettinger-klimabuendnis"


cd ${PDIR}
rm -r public
/usr/bin/git checkout . # to remove all local changes (which are never authorative)
/usr/bin/git pull origin master
${HUGO}

rm -r ${DDIR}/public
cp -a public ${DDIR}
cp ${DDIR}/public/404.html ${DDIR}/public/50x.html # ssl error page also needed
cd ${DDIR}

/usr/bin/docker build . -t ${TAG}
if [[ $? == 0 ]]; then
  /usr/bin/docker stop  ${TAG}
  /usr/bin/docker run -d --name ${TAG} -p 80:80 -p 443:443 --rm ${TAG}
  /usr/bin/docker image prune -a -f
fi
