## Context

Ce projet a été réalisé dans le cadre du parcours de formation Data Engineer d'OpenClassrooms.

Titre du projet :

**Mettez en place un pipeline d'orchestration des flux**

L'objectif est de mettre en place un pipeline ETL/ELT automatisé permettant de nettoyer des données de ventes, vérifier leur qualité, calculer le chiffre d'affaires, produire un rapport Excel et classer les produits selon un score Z afin de distinguer les vins premium des vins ordinaires.

Le projet exploite des données issues de plusieurs fichiers Excel, puis orchestre les traitements via Kestra avec Docker.

L’intérêt d’une orchestration avec Kestra réside dans la capacité à découper un workflow complexe en tâches indépendantes, chacune ayant un rôle précis : nettoyage, validation, jointure, calcul, export et classification. Ce découpage facilite la maintenance, améliore la traçabilité des erreurs et permet de relancer uniquement la partie concernée en cas de problème. Il rend également le pipeline plus lisible, plus modulaire et plus facilement évolutif.

---

## Prérequis

### Docker

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS)
- [Docker Engine](https://docs.docker.com/engine/install/) (Linux)


## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Ben-TerraPi/p10_Kestra_etl_pipeline.git
cd p10_Kestra_etl_pipeline
```

### 2. Lancer Kestra avec docker-compose.yml

```bash
docker compose up -d
```

Le service Kestra est accessible ici :

```text
http://localhost:8080/
```

Arrêt et nettoyage :

```bash
docker compose down -v
```

---

## Déroulé du workflow Kestra

Ce workflow Kestra utilise des namespace files. Les namespace files permettent de stocker et d’exécuter des scripts Python directement depuis Kestra. Cela simplifie la gestion des fichiers de code et des dépendances, rend le workflow portable et permet de centraliser la logique métier de chaque étape dans un environnement d’exécution bien défini.

> Note : Il faut donc créer le namespace `com.bottleneck.analytics` et y charger les différents fichiers selon cette arborescence :

```text
.
├── data/
│   ├── Fichier_erp.xlsx
│   ├── fichier_liaison.xlsx
│   └── Fichier_web.xlsx
├── scripts/
│   ├── 01_cleaning.py
│   ├── 03_join.py
│   ├── 05_calculate_ca.py
│   ├── 07_export_report.py
│   ├── 08_classify_wines.py
│   └── 10_export_wines.py
└── sql/
    ├── jointures.sql
    └── nettoyage.sql
```

Le fichier `kestra/bottleneck_pipeline_kestra.yml` orchestre les tâches selon l'architecture suivante.

![Architecture](image/architecture_bottleneck.png)

### 1. Chargement et netoyage des données

- `01_cleaning.py`
- nettoyage des colonnes et des types ;
- suppression des doublons ;
- normalisation des tables sources.

### 2. Tests de qualité après nettoyage

- vérifie qu'il n'y a pas de doublons sur `product_id` et `id_web` ;
- vérifie le nombre attendu de lignes après nettoyage.

### 3. Jointure des données

- `03_join.py`
- fusion des tables ERP, web et liaison ;
- construction d'une table unique de produits.

### 4. Tests de cohérence après jointure

- validation des clés ;
- contrôle du volume final ;
- détection des doublons restants.

### 5. Calcul du chiffre d'affaires

- `05_calculate_ca.py`
- calcule le `chiffre_affaires` par ligne ;
- totalise le CA global.

### 6. Contrôle des totaux

- vérifie que le CA calculé est bien égal au montant attendu : `70568.60 €`.

### 7. Export du rapport

- `07_export_report.py`
- génère un fichier Excel : `output/rapport_chiffre_affaires.xlsx`.

### 8. Classification des vins

- `08_classify_wines.py`
- calcule le z-score sur les prix ;
- distingue les vins premium (`z_score > 2`) des vins ordinaires (`z_score <= 2`).

### 9. Validation du tri

- vérifie que 30 vins sont classés premium ;
- vérifie que les autres lignes restent dans la catégorie ordinaire.

### 10. Export final

- `10_export_wines.py`
- produit les fichiers :
  - `output/vins_premium.csv`
  - `output/vins_ordinaires.csv`