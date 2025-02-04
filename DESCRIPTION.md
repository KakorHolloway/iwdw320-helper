# Création de gitlab

Sur la vm je créé le dossier gitlab

```
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

##Mettez la suite sous la même forme ici.... 