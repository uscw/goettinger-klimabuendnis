git pull origin master

rm -r /home/gkb_user/Docker/nginx-alpine/public/*
cp -a /home/gkb_user/goettinger-klimabuendnis/public/* /home/gkb_user/Docker/nginx-alpine/public

cd /home/gkb_user/Docker/nginx-alpine/
docker build . -t goettinger-klimabuendnis
docker run -d --name goettinger-klimabuendnis goettinger-klimabuendnis
