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