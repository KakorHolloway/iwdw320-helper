# Consignes de l'examen 

Cet examen a pour but de vous permettre de pratiquer les différentes solutions vu en cours et de vous introduire à Ansible. 

Le rendu sera ce projet git modifié avec les fichiers demandés au format zip sur moncampus. 

Un fichier md présentant le procéssus pour chaque étape est attendu sous le nom DESCRIPTION.md, le nom des différents participants doit être indiqué. 

## Préparation de gitlab et de gitlab runner 

A partir de la documentation de gitlab créez le fichier docker-compose.yml permettant de créer un conteneur gitlab qui exposera l'adresse ip de votre machine en *http*

Connectez vous à gitlab. (récupérez le mot de passe sur le conteneur gitlab-ce dans /etc/gitlab/initial_root_password)

Ajoutez à ce fichier docker-compose.yml une section gitlab-runner. Ce conteneur va créer un gitlab-runner qui va lui-même créer des conteneurs sur votre machine qui vont exécuter des commandes spécifiques de votre CI/CD.

Pour fonctionner avec docker, gitlab-runner doit monter les volumes suivants : 

```
'/var/run/docker.sock:/var/run/docker.sock'
'./runner:/etc/gitlab-runner'
```

Avec la commande gitlab-runner register, ajoutez le runner à votre gitlab principal. (ex: ```docker exec -it <idgitlab-runner> gitlab-runner register  --url http://172.18.212.234  --token glrt-t1_86g72huU3asYYMs44mnG ```)
Mettez l'image ruby:2.7 par défaut et docker comme executor


Créez un nouveau projet sur gitlab nommé CI/CD (ou autre..) et poussez ce repo git dessus pour plus tard. 

## Mise en place de la pipeline CI/CD

Le but de la stage build est de créer une nouvelle image docker qui va exposer une application python flask contenue dans le dossier app-python. 

En vous aidant de la documentation suivante: https://devopssec.fr/article/creer-ses-propres-images-docker-dockerfile, ajoutez les section manquantes commentées. 

Modifiez la pipeline du fichier .gitlab-ci.yml pour que le conteneur soit déployé sur la container registry https://harbor.kakor.ovh (user ipi et mdp B4teau123!)

Pour ce faire, renseignez les variables CI_REGISTRY_USER et CI_REGISTRY_PASSWORD sur gitlab. 

## Mise en place d'un fichier docker-compose.yml et démarrage via ansible

Afin de déployer le fichier docker compose, nous allons utiliser un playbook ansible. 

Pour qu'ansible fonctionne, on possède un fichier hosts qui sert pour faire un inventaire des vm et le fichier playbook.yml qui va permettre de déployer. (cf: ansible/) (plus d'info dans https://devopssec.fr/article/creation-playbook-ansible-stack-lamp)

Afin de l'utiliser, il va falloir créer une clé rsa pour vous authentifier à votre machine. Créez cette clé et testez là. 

Renseignez la variable CI/CD SSH_PRIVATE_KEY dans gitlab. 

Créez dans ansible/files le fichier docker-compose.yml qui va permettre de déployer le conteneur build dans l'étape d'avant. 

Modifier le fichier playbook.yml pour correspondre aux bons chemin sur git et sur la vm. 

Ajoutez au fichier playbook.yml un nouveau module shell afin de lancer la commande docker-compose up -d /path/to/file

## testez l'accès à votre conteneur depuis votre VM 

Testez d'accès à votre conteneur et prenez une capture d'écran que vous mettrez dans votre repo git.

Modifiez bien le fichier DESCRIPTION.md et téléchargez le repo git en zip avant de me l'envoyer sur mon campus. 
