# Examen IMDW320

## Préparation 

Sur une vm ubuntu ou debian, installez docker et docker compose. 

```apt-get install docker docker-compose -y```

Installez gitlab à partir du fichier docker-compose.yml de ce repo nommé "docker-compose-gitlab.yml".

Renommez ce fichier docker-compose.yml dans votre machine et lancez la commande :

```sudo docker-compose up -d```

Configurez gitlab et gitlab-runner pour que gitlab-runner utilise gitlab.

Afin de lancer des commandes dans un conteneur, vous pouvez utiliser les commandes suivantes :

```
docker exec -it gitlab-runner /bin/bash
#ou bien en fonction de l'instance
docker exec -it gitlab /bin/bash
```

Pour transférez ce projet vers votre Gitlab vous pouvez lancer les commandes suivantes :
```
git clone https://github.com/KakorHolloway/iwdw320-helper
git clone http://urldevotreprojetgit.git
cp iwdw320-helper/.gitlab-ci.yml dossierdevotrerepo/
rm -rf iwdw320-helper/.git
cp -r iwdw320-helper/* dossierdevotrerepo/
cd dossierdevotrerepo/
git add .
git commit -am "first commit"
# en cas d'erreur du commit lancez les commandes git config indiqués dans l'erreur
git push 
```

## Mise en place du repo 

A partir de maintenant, modifiez le fichier DESCRIPTION.md pour indiquer ce que vous faites pour créer la pipeline et modifier les valeurs des secret par exemple. 

Sur le gitlab nouvellement créé, créez un nouveau projet git à partir de celui-ci (regardez via la commande git set-url)

Modifiez la pipeline gitlab-ci.yml pour que le nom de l'image créé soit adaptée à celui de votre groupe. 

Modifiez les variables d'authentification CI_REGISTRY_USER par ipi et CI_REGISTRY_PASSWORD par le mot de passe indiqué au tableau. 

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