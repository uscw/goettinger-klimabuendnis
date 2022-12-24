INDIR="/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis"
GITDIR="/home/uschwar1/Dokumente/goettinger-klimabuendnis"
GITPARENTDIR="/home/uschwar1/Dokumente"
HUGO="/home/uschwar1/ownCloud/AC/html/hugo/hugo"
SERVER_USR="gkb_user"
SERVER_LOC="${SERVER_USR}@1b14c95.online-server.cloud"
SERVER_DIR="Docker/nginx-alpine"

# PoW-Archiv aktualisieren
python3 ${INDIR}/bin/archiv_pow.py

find ${INDIR} -type f -iname "*~"  -exec /bin/rm {} \;
chmod -R +rwX public/

rsync -aHAXx --delete --exclude ".git" ${INDIR} ${GITPARENTDIR}
sed -i "s/https:\\/\\/localhost:1313/http:\\/\\/goettinger-klimabuendnis.de/g" ${GITDIR}/config.toml
echo "wait"; sleep 2

ORIPWD=`echo $PWD`
cd ${GITDIR}
${HUGO}

echo "provide commit message:"
read inp
if [[ ${inp} == "" ]]; then
  inp="Aktualisierung des Web-Inhaltes"
fi
git add --all
git commit -m "${inp}"
git push origin master

rsync -avze ssh --delete public ${SERVER_LOC}:${SERVER_DIR}
echo "wait"; sleep 2

cd ${ORIPWD}

ssh $SERVER_LOC /home/${SERVER_USR}/bin/docker_reload.sh

