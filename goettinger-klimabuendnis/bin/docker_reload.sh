UDIR="/home/gkb_user"
PDIR=${UDIR}/"goettinger-klimabuendnis"
DDIR=${UDIR}/"/Docker/nginx-alpine"
HUGO=${UDIR}"/bin/hugo"
TAG="goettinger-klimabuendnis"


cd ${PDIR}
git pull origin master

rm -r ${DDIR}/public
cp -a public ${DDIR}
cd ${DDIR}

docker build . -t ${TAG}
docker stop  ${TAG}
docker run -d --name ${TAG} -p 80:80 -p 433:433 --rm ${TAG}
