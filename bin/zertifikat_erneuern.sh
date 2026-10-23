echo 
echo "Verwaltung der SSL-Zertifikate"
echo "=============================="
echo " Login auf https://login.ionos.de/ (ggf. dort auf Mein IONOS)" 
echo " weiter zu Domains & SSL"
echo " und zu Zertifikatseinstellungen: Domain *.goettinger-klimabuendnis.de"
echo " - dort neues Zertifikat erzeugen -> den private key"
echo " dann zurück auf Domain *.goettinger-klimabuendnis.de"
echo " SSL-Zertifikat herunterladen - den public key"
echo
ls -lrt /home/uschwar1/Downloads/|tail -5
echo
echo "Frage: Dateiname des private key in ~/Downloads?"
read PRIVNAME
mv /home/uschwar1/Downloads/${PRIVNAME} /tmp/goettinger-klimabuendnis.de_private_key.key
echo
echo "Frage: Dateiname des public key in ~/Downloads?"
read PUBLNAME
mv /home/uschwar1/Downloads/${PUBLNAME} /tmp/goettinger-klimabuendnis.de_public.crt

MOD1=`openssl rsa -modulus -noout -in /tmp/goettinger-klimabuendnis.de_private_key.key | openssl md5`
MOD2=`openssl x509 -modulus -noout -in /tmp/goettinger-klimabuendnis.de_public.crt | openssl md5`
if [[ ${MOD1} == ${MOD2} ]]; then
    echo
    echo Die Moduli stimmem überein. Folgende Befehle sind auszuführen:
    echo
    echo    scp /tmp/goettinger-klimabuendnis.de_private_key.key goettinger-klimabuendnis.de_public.crt gkb_user@goettinger-klimabuendnis.de:Docker/nginx-latest/
    echo    ssh gkb_user@goettinger-klimabuendnis.de bin/docker_reload.sh
else
    echo "Fehler: unterschiedlicher Modulus der public und private Zertifcate"
fi
echo
echo Im Anschluss:
echo " https://goettinger-klimabuendnis.de neu im Browser laden und Zertifikat ansehen:"
echo " - Seiteninformationen - Sicherheitsinformationen der Seite (Schlosszeichen neben der Seiten-URL"
echo " - weitere Informationen - Zertifikat anzeigen"
