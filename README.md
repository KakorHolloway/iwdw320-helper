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