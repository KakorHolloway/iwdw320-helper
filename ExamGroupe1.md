# Examen IMDW320

## Préparation 

Sur une vm ubuntu ou debian, installez docker et docker compose. 

```apt-get install docker docker-compose -y```

Installez gitlab à partir du fichier docker-compose.yml de ce repo nommé "docker-compose-gitlab.yml".

Renommez ce fichier docker-compose.yml dans votre machine et lancez la commande :

```docker-compose up -d```

## Mise en place du repo 

A partir de maintenant, modifiez le fichier DESCRIPTION.md pour indiquer ce que vous faites pour créer la pipeline et modifier les valeurs des secret par exemple. 

Sur le gitlab nouvellement créé, créez un nouveau projet git à partir de celui-ci (regardez via la commande git set-url)

Modifiez la pipeline gitlab-ci.yml pour que le nom de l'image créé soit adaptée à celui de votre groupe. 

## Déploiement sur Openshift 

Ajoutez une nouvelle pipeline pour déployer l'application sur openshift à partir de l'image. 

Pour ce faire, à partir de l'image harbor.kakor.ovh/public/oc-helm, lancez les commandes suivantes à travers un nouveau stage :

```
oc login --token=sha256~v-aayWujKJno9kFgCTVtkDmXx9JcC7uvSorB588y90Q --server=https://api.openshift.kakor.ovh:6443 --insecure-skip-tls-verify=true
oc run pod-groupe-x --image=nomdelimage:tag
```

Connectez vous sur l'interface avec le user ipi-gp-10 et le mot de passe indiqué au tableau pour vérifier le déploiement. 

Stockez le token dans une variables gitlab. 

Rendez moi le zip de votre repo sur moncampus. 