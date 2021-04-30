cd /home/gkb_user/goettinger-klimabuendnis

git pull origin master

/home/gkb_user/bin/hugo

rm -r /home/gkb_user/Docker/nginx-alpine/public/*
cp -a /home/gkb_user/goettinger-klimabuendnis/public/* /home/gkb_user/Docker/nginx-alpine/public

cd /home/gkb_user/Docker/nginx-alpine/
docker build . -t goettinger-klimabuendnis
docker run -d --name goettinger-klimabuendnis -p 80:80 goettinger-klimabuendnis
