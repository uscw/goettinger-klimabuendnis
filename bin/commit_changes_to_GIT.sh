GITDIR="/home/uschwar1/Dokumente/goettinger-klimabuendnis"
GITPARENTDIR="/home/uschwar1/Dokumente"
HUGO="${GITDIR}/bin/hugo"
SERVER_USR="gkb_user"
SERVER_LOC="${SERVER_USR}@goettinger-klimabuendnis.de"
SERVER_DIR="Docker/nginx-alpine"

# PoW-Archiv aktualisieren
python3 ${GITDIR}/bin/archiv_pow.py

find ${GITDIR} -type f -iname "*~"  -exec /bin/rm {} \;

ORIPWD=`echo $PWD`
cd ${GITDIR}
${HUGO}

git pull origin main
if [[ $? != "0" ]]; then
  echo "Error: Branches differ! Check consistency"
  exit 1
fi 

echo "provide commit message:"
read inp
if [[ ${inp} == "" ]]; then
  inp="Aktualisierung des Web-Inhaltes"
fi
git add --all
git commit -m "${inp}"

git push origin main
# exit 0

rsync -avze ssh --delete public ${SERVER_LOC}:${SERVER_DIR}
echo "wait"; sleep 2

cd ${ORIPWD}

echo "ssh $SERVER_LOC /home/${SERVER_USR}/bin/docker_reload.sh"
ssh $SERVER_LOC /home/${SERVER_USR}/bin/docker_reload.sh

