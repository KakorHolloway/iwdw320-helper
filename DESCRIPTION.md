# Correction Exam 

## Création de gitlab

Sur la vm je créé le dossier gitlab

```
apt-get install docker.io docker-compose -y
mkdir gitlab
cd gitlab
```

Créez le fichier docker-compose.yml dans le dossier gitlab (en changeant l'adresse ip de gitlab pour celle de la vm) :

```
version: '3.7'
volumes:
  logs:
    driver: local
  config:
    driver: local
  data:
    driver: local
  runner:
    driver: local
services:
  gitlab:
    restart: unless-stopped
    image: harbor.kakor.ovh/public/gitlab-ce:latest
    container_name: gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        gitlab_rails['gitlab_shell_ssh_port'] = 2222
        external_url 'http://<ip>'
    ports:
      - '80:80'
      - '2222:22'
    volumes:
      - 'data:/var/opt/gitlab'
      - 'config:/etc/gitlab'
      - 'logs:/var/log/gitlab'
  gitlab-runner:
    restart: unless-stopped
    image: harbor.kakor.ovh/public/gitlab-runner:latest
    container_name: gitlab-runner
    volumes:
      - '/var/run/docker.sock:/var/run/docker.sock'
      - 'runner:/etc/gitlab-runner'
      - 'config:/etc/gitlab'
```

Lancez la commande suivante pour lancer les conteneurs :

```
docker-compose up -d 
```

## Mise en place du runner 

Pour mettre en place le runner, sur gitlab allez dans le chemin Admin > CI/CD > Runners > New instance runner. 

Afin de créer un runner universel, lors de la création, il faut bien faire attention à cocher la case ```Run untagged jobs```. 

Une fois sur votre VM, rentrez la commande suivante : 
```docker exec -it gitlab-runner register```

Et indiquez les différentes informations (url de votre gitlab sous la forme http://monip et le token indiqué sous la forme glrt-salxklzakcjldcj... )

## Création du fichier .gitlab-ci.yaml 

Afin de mettre à jour le fichier .gitlab-ci.yml, faites bien attention à changer la ligne 15 par le nom de votre nouvelle image :

```      --destination "harbor.kakor.ovh/ipi/<nomimage>-${CI_PROJECT_NAME}:${CI_COMMIT_TAG}" ```

Remplacez les lignes du Dockerfile par les lignes suivantes en suivant les instructions données :

```
FROM python:3.9

# placez vous dans le dossier /app
WORKDIR /app
# installez flask avec pip
RUN pip install flask
# copiez le contenu du dossier app-python dans le dossier courant 
COPY app-python/ .
# exposez le port 5000
EXPOSE 5000

ENV FLASK_APP=/app/main.py
CMD ["flask", "run", "--host", "0.0.0.0"]
```

N'oubliez pas avant de lancer la pipeline CI/CD à bien mettre en place les variables **CI_REGISTRY_USER** et **CI_REGISTRY_PASSWORD** dans les option du projet Gitlab > CI/CD.

## Mise en place de la partie de la partie ansible.

En root sur votre VM créé une clé ssh :

```ssh-keygen```

Copiez le contenu du fichier /root/.ssh/id_rsa.pub dans /root/.ssh/authorized_keys 

Gardez le fichier /root/.ssh/id_rsa pour le mettre en tant que variable dans le projet Gitlab CI/CD sour le nom **SSH_PRIVATE_KEY**

Créez le fichier ansible/files/docker-compose.yml avec les éléments suivant pour récupérer le conteneur :
```
services:
  gitlab:
    restart: unless-stopped
    image: harbor.kakor.ovh/ipi/gp-x:v0.0
    container_name: gitlab
```

Afin de récupérer ce fichier, on va modifier le fichier ansible/playbook.yml pour créer le dossier /root/docker-compose et copier le fichier à cet emplacement. 

On va également lancer la commende docker-compose à traver le module ansible 'shell' :

```
---
- name: Copy docker-compose file
  hosts: docker
  tasks:
    - name: Créer un dossier
      file:
        path: /root/docker-compose
        state: directory
        mode: '0755'
    - name: Copier le fichier docker-compose.yml
      copy:
        src: files/docker-compose.yml
        dest: /root/docker-compose/docker-compose.yml
    - name: Launch docker docker-compose
      shell:
        "docker-compose up -d -f /root/docker-compose/docker-compose.yml"
```

Le projet est prêt à l'emploi. 

