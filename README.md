# DataOps / MLOps — Air Quality

Projet collaboratif de mise en place d'une infrastructure **DataOps/MLOps** autour de données de qualité de l'air. Le dépôt contient une base technique conteneurisée, un premier DAG de démonstration, une API de santé, un serveur de suivi des expériences et un pipeline d'intégration continue.

> **État actuel : infrastructure de développement opérationnelle sur le poste de test.** Le traitement réel des données, l'entraînement de modèles et le déploiement automatisé ne sont pas encore démontrés.

## 1. Objectifs

- Collecter et transporter des données via **Apache Kafka**.
- Stocker les données dans **PostgreSQL**.
- Orchestrer les traitements avec **Apache Airflow**.
- Suivre les expériences et les modèles avec **MLflow**.
- Exposer des services HTTP avec **FastAPI**.
- Automatiser les vérifications du dépôt avec **Jenkins**.
- Collaborer avec **Git et GitHub**, via branches et pull requests.

## 2. Architecture actuelle

```text
                  GitHub (branches / pull requests)
                              |
                              v
                       Jenkins (CI)

   Sources de données (à intégrer)
                 |
                 v
        Kafka : raw_data
                 |
                 v
      Traitements (à développer) <---- Airflow (orchestration)
                 |
          +------+-------+
          |              |
          v              v
 Kafka : processed_data  Kafka : anomalies
          |
          v
 PostgreSQL (stockage à intégrer)
          |
          +----------> FastAPI (API à enrichir)
          |
          +----------> MLflow (suivi ML à intégrer)
```

**Important :** ce schéma représente le flux cible. Les échanges de données entre les services ne sont pas tous implémentés à ce stade.

## 3. Technologies

| Outil | Rôle | État constaté |
| --- | --- | --- |
| Docker Compose | Démarrage des services | Fonctionnel |
| PostgreSQL 16 | Base de données `air_quality` | Fonctionnel, contrôle de santé OK |
| Apache Kafka 3.9.1 | Messagerie événementielle | Fonctionnel ; topics créés |
| Apache Airflow 2.10.5 | Orchestration des tâches | Interface accessible ; DAG de test réussi |
| MLflow 2.22.0 | Suivi des expériences ML | Interface accessible ; expérience de test enregistrée |
| FastAPI | API HTTP | Documentation Swagger accessible ; routes `/` et `/health` |
| Jenkins | Intégration continue | Premier pipeline exécuté avec succès |
| GitHub | Versionnement et revues | Branches et pull requests utilisées |
| Portainer | Visualisation des conteneurs | Utilisé localement ; installation séparée |

## 4. Organisation du dépôt

Structure représentative observée au cours de la configuration :

```text
dataOPsTest/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Jenkinsfile
├── README.md
├── airflow/
│   └── dags/
│       └── test_pipeline.py
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
└── mlflow/
    └── Dockerfile
```

Le fichier `Jenkinsfile` a été lu depuis la branche `main` par Jenkins. Vérifier la structure exacte du dépôt après chaque fusion.

## 5. Prérequis

- Ubuntu ou autre système prenant en charge Docker.
- Docker Engine et le plugin Docker Compose.
- Git.
- Ports locaux disponibles : **5432**, **9092**, **8080**, **5000**, **8000** ; **8081** si Jenkins est installé localement.
- Mémoire et espace disque suffisants pour les images Docker.

## 6. Installation et démarrage

### Cloner le projet

```bash
git clone https://github.com/otheruser-14/dataOPsTest.git
cd dataOPsTest
```

### Préparer les variables d'environnement

```bash
cp .env.example .env
```

Adapter les variables de `.env` à l'environnement local. **Ne jamais versionner `.env`**. Les valeurs présentes dans `.env.example` sont des valeurs de démonstration ; remplacer le mot de passe avant tout usage partagé ou exposé.

### Valider la configuration

```bash
sudo docker compose config --quiet
```

### Démarrer les services principaux

```bash
sudo docker compose up -d --build
```

### Démarrer Airflow et MLflow (profils optionnels)

```bash
sudo docker compose --profile orchestration --profile mlops up -d --build
```

### Vérifier l'état

```bash
sudo docker compose --profile orchestration --profile mlops ps -a
```

Le conteneur **`kafka-init`** est un processus d'initialisation : un état `Exited (0)` après exécution est normal.

> Si Docker fonctionne sans `sudo` sur votre machine, vous pouvez retirer `sudo`. Le réglage des permissions Docker peut être effectué séparément.

## 7. Accès aux interfaces locales

| Service | Adresse locale | Remarques |
| --- | --- | --- |
| FastAPI Swagger | `http://localhost:8000/docs` | Documentation interactive |
| FastAPI santé | `http://localhost:8000/health` | Vérification HTTP |
| Airflow | `http://localhost:8080` | Identifiants configurés localement |
| MLflow | `http://localhost:5000` | Expériences et runs |
| Jenkins | `http://localhost:8081` | Service Jenkins installé séparément |
| Portainer | `https://localhost:9443` | Outil local optionnel, installé séparément |
| PostgreSQL | `127.0.0.1:5432` | Connexion SQL, pas une page web |
| Kafka | `127.0.0.1:9092` | Connexion client, pas une page web |

Les ports de la configuration partagée sont publiés sur `127.0.0.1` : ils sont accessibles depuis la machine hôte, pas directement depuis les autres ordinateurs du réseau.

## 8. Vérifications manuelles

### PostgreSQL

```bash
sudo docker exec dataops-postgres pg_isready -U dataops -d air_quality
sudo docker exec -it dataops-postgres psql -U dataops -d air_quality
```

Quitter `psql` avec `\q`.

### Kafka

```bash
sudo docker exec dataops-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:29092 --list
```

Topics créés lors des essais :

- `raw_data` : messages entrants.
- `processed_data` : messages transformés.
- `anomalies` : anomalies détectées.

### Airflow

```bash
sudo docker exec dataops-airflow airflow dags list
sudo docker exec dataops-airflow airflow dags list-import-errors
```

Le DAG de démonstration **`test_dataops_pipeline`** comporte trois tâches exécutées avec succès : `extraction` → `transformation` → `chargement`. Il valide le fonctionnement de l'orchestrateur, **pas encore un pipeline de données de production**.

### MLflow

L'expérience **`DataOps-AirQuality`** et le run **`test_infrastructure`** ont été créés avec succès. Cela confirme l'accès au serveur de suivi ; aucun entraînement réel n'est encore documenté.

### FastAPI

Ouvrir `/docs` et tester les routes `GET /` et `GET /health` depuis Swagger.

## 9. Intégration continue avec Jenkins

Un job Jenkins **`DataOps-CI`** est connecté au dépôt GitHub et lit le `Jenkinsfile` depuis `main`.

Le premier pipeline a été exécuté avec le résultat **`Finished: SUCCESS`**. Il a réalisé :

1. Le checkout du dépôt GitHub.
2. La vérification de l'existence de `docker-compose.yml`.
3. La vérification de `api/Dockerfile` et `api/requirements.txt`.
4. La lecture du dernier commit Git.

**Limite actuelle :** ces contrôles valident surtout la structure du dépôt. Ils ne prouvent pas que les tests unitaires, les builds Docker ou les tests d'intégration sont automatisés.

### Améliorations prévues pour la CI

- Ajouter des tests Python avec `pytest`.
- Vérifier la configuration Docker Compose.
- Construire les images dans un environnement CI approprié.
- Ajouter des tests d'intégration entre services.
- Déclencher les vérifications automatiquement pour les pull requests.
- Éviter de placer des secrets dans les scripts ou les logs Jenkins.

## 10. Méthode de travail Git

Le projet suit un flux de travail basé sur `main`, des branches courtes et des pull requests.

Exemples de branches utilisées :

```text
feature/docker-infrastructure
feature/airflow-infrastructure
feature/mlflow-infrastructure
feature/jenkins-pipeline
docs/team-environment
```

Exemple de contribution :

```bash
git switch main
git pull origin main
git switch -c feature/ma-fonctionnalite

# Modifier les fichiers, puis :
git add .
git commit -m "feat: description de la fonctionnalite"
git push -u origin feature/ma-fonctionnalite
```

Créer ensuite une pull request vers `main`, faire relire les modifications et fusionner après validation.

## 11. Limites connues

- Airflow utilise actuellement **SQLite** et `SequentialExecutor` : configuration adaptée aux tests locaux, **pas à la production**. Migration vers PostgreSQL reportée.
- Les services n'ont pas tous des healthchecks ni des politiques de sécurité finalisées.
- Le pipeline Kafka → traitement → PostgreSQL reste à développer et tester de bout en bout.
- MLflow fonctionne, mais le suivi d'un véritable entraînement n'est pas encore documenté.
- FastAPI propose pour l'instant des endpoints de base.
- Le pipeline Jenkins ne lance pas encore de tests automatisés applicatifs.
- Les accès, mots de passe et ressources nécessaires à une équipe doivent être configurés sur chaque environnement.

## 12. Prochaines étapes

1. Définir le format et la source des données de qualité de l'air.
2. Développer un producteur Kafka et un consommateur de traitement.
3. Créer le schéma PostgreSQL et persister les observations.
4. Construire un DAG Airflow orchestrant un traitement réel.
5. Ajouter la détection d'anomalies ou un modèle ML suivi par MLflow.
6. Exposer des résultats via FastAPI.
7. Ajouter les tests automatiques et renforcer Jenkins CI.
8. Migrer les métadonnées Airflow de SQLite vers PostgreSQL lorsque l'équipe sera prête.
9. Documenter les variables, les rôles et les procédures de contribution.

## 13. Arrêt des services

```bash
sudo docker compose --profile orchestration --profile mlops down
```

**Attention :** ne pas ajouter `-v` sans intention explicite de supprimer les volumes persistants (et donc potentiellement les données PostgreSQL, Airflow et MLflow).

---

**Statut :** socle d'infrastructure validé localement ; pipeline DataOps/MLOps métier à construire.
