# Instruction pour IMDW 320

## Paramétrage des prérequis

1) Installez une vm ubuntu 
2) Mettez à jour votre vm et installez le package docker.io en root :
```
sudo apt-get update 
sudo apt-get install docker.io -y
```
3) Vérifiez que docker fonctionne bien en lançant cette commande :
```
sudo docker run hello-world
```

4) Installez nginx :

```
docker run -d nginx

docker ps # lister les conteneurs
```

5) Testez nginx 

```
docker inspect <iddevotreconteneur>
```
Faites un curl sur l'ip du conteneur pour vérifier que nginx fonctionne

6) Supprimez le conteneur 

Arrêtez le conteneur avec la commande 

```
docker stop <idconteneur>

docker ps # vérifiez que seul les conteneurs actifs sont listez 

docker ps -a # vérifiez que tous vos conteneurs créés existent 

docker rm <idconteneur> # nettoyez tous les conteneurs 

docker ps -a # vérifiez que c'est bon 
```

## Exercice avec docker 

1) Regardez les options de docker avec ```docker --help```
2) En une seule commande :
 - Créez un conteneur nginx avec l'image nginx:1.26 
 - Donnez lui le nom docker "monnginx"
 - faites en sorte que nginx écoute sur le port 8080 avec la variable d'environnement NGINX_PORT
 - configurez l'accès depuis votre machine hôte à votre conteneur depuis un navigateur internet (http://ipdemavm:9090)

Pour tester l'env ```docker exec <id> env ```

Correction ```docker run --name "monnginx" -e NGINX_PORT=8080 -p 9090:80 -d nginx:1.26```

Astuce pour tout delete plus vite!

```
for cont in $(docker ps -aq); do docker stop $cont; done
for cont in $(docker ps -aq); do docker rm $cont; done
```

3) Le problème de docker c'est qu'il n'est pas capable de stocker de la donnée persistente. 

En effet si votre conteneur est supprimé, les données sont perdues.

De fait vous pouvez créer des volumes via ``` docker volume create monvolume ```

Ce volume est stocké dans votre vm sur /var/lib/docker/volumes. 

- Rentrez dans votre conteneur via la commande ```docker exec -it <idconteneur> /bin/bash```. En regardant dans le dossier /etc/nginx/conf.d, identifiez l'emplacement du fichier index.html responsable de la page d'acceuil nginx

- Supprimez le conteneur nginx précédemment créé
- Créez un nouveau volume nginx
- via l'option -v monter un volume sur un conteneur nginx basé sur la commande de l'exercice 2 afin que ce volume soit monté sur le répertoire contenant le fichier index.html
- Pour vérifier le fonctionnement, éditer le fichier index.html et rechargez la page de votre navigateur
- vérifiez la persistence en supprimant et en recréant le conteneur tel quel. 

Correction :

```
#Création du volume 
docker volume create monvolume
#Montage du volume 
docker run --name "monnginx" -e NGINX_PORT=8080 -v monvolume:/usr/share/nginx/html -p 9090:80 -d nginx:1.26
#Modification du fichier depuis la machine hôte 
vi /var/lib/docker/volumes/monvolume/_data/index.html
# Il n'y as plus qu'a supprimer et relancer la deuxième commande pour confirmer la persistence
```

## Exemple docker compose 
Créez le dossier suivant :
```
mkdir owncloud-docker-server
cd owncloud-docker-server
```

Créez le fichier docker-compose.yml suivant :
```
version: "3"

volumes:
  files:
    driver: local
  mysql:
    driver: local
  redis:
    driver: local

services:
  owncloud:
    image: owncloud/server:${OWNCLOUD_VERSION}
    container_name: owncloud_server
    restart: always
    ports:
      - ${HTTP_PORT}:8080
    depends_on:
      - mariadb
      - redis
    environment:
      - OWNCLOUD_DOMAIN=${OWNCLOUD_DOMAIN}
      - OWNCLOUD_TRUSTED_DOMAINS=${OWNCLOUD_TRUSTED_DOMAINS}
      - OWNCLOUD_DB_TYPE=mysql
      - OWNCLOUD_DB_NAME=owncloud
      - OWNCLOUD_DB_USERNAME=owncloud
      - OWNCLOUD_DB_PASSWORD=owncloud
      - OWNCLOUD_DB_HOST=mariadb
      - OWNCLOUD_ADMIN_USERNAME=${ADMIN_USERNAME}
      - OWNCLOUD_ADMIN_PASSWORD=${ADMIN_PASSWORD}
      - OWNCLOUD_MYSQL_UTF8MB4=true
      - OWNCLOUD_REDIS_ENABLED=true
      - OWNCLOUD_REDIS_HOST=redis
    healthcheck:
      test: ["CMD", "/usr/bin/healthcheck"]
      interval: 30s
      timeout: 10s
      retries: 5
    volumes:
      - files:/mnt/data

  mariadb:
    image: mariadb:10.11 # minimum required ownCloud version is 10.9
    container_name: owncloud_mariadb
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=owncloud
      - MYSQL_USER=owncloud
      - MYSQL_PASSWORD=owncloud
      - MYSQL_DATABASE=owncloud
      - MARIADB_AUTO_UPGRADE=1
    command: ["--max-allowed-packet=128M", "--innodb-log-file-size=64M"]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-u", "root", "--password=owncloud"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - mysql:/var/lib/mysql

  redis:
    image: redis:6
    container_name: owncloud_redis
    restart: always
    command: ["--databases", "1"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - redis:/data
```

Créez le fichier .env suivant 

```
OWNCLOUD_VERSION=10.15
OWNCLOUD_DOMAIN=localhost:8080
OWNCLOUD_TRUSTED_DOMAINS=localhost
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
HTTP_PORT=8080
```

Lancez votre application avec la commande 
```
docker compose up -d 
```

Testez l'accès à votre application. 