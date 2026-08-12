## Context

Ce projet a été réalisé dans le cadre du parcours de formation Data Engineer d'OpenClassrooms.

Titre du projet :

`Mettez en place un pipeline d'orchestration des flux`

L'objectif est de mettre en place un pipeline ETL/ELT automatisé permettant de nettoyer des données de ventes, vérifier leur qualité, calculer le chiffre d'affaires, produire un rapport Excel et classer les produits selon un score Z afin de distinguer les vins premium des vins ordinaires.

Le projet exploite des données issues de plusieurs fichiers Excel, puis orchestre les traitements via Kestra avec Docker.

![Architecture](image/architecture_bottleneck.png)

---

## Prérequis

### Docker

Pour exécuter le workflow Kestra :

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS)
- [Docker Engine](https://docs.docker.com/engine/install/) (Linux)


## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd p10_
```

### 2. Lancer Kestra avec Docker

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

> Note : le workflow Kestra utilise des namespace files. Il faut donc créer le namespace `com.bottleneck.analytics` et y charger les différents scripts depuis comme suit :

```text
.
├── data/
│   ├── Fichier_erp.xlsx
│   ├── fichier_liaison.xlsx
│   ├── Fichier_web.xlsx
│   └── exploration_data.py
├── scripts/
│   ├── 01_cleaning.py
│   ├── 02_test_cleaning.py
│   ├── 03_join.py
│   ├── 04_test_join.py
│   ├── 05_calculate_ca.py
│   ├── 06_test_totals.py
│   ├── 07_export_report.py
│   ├── 08_classify_wines.py
│   ├── 09_test_scores.py
│   └── 10_export_wines.py
└── sql/
│   ├── doublons.sql
│   ├── jointures.sql
│   └── nettoyage.sql
```

Le fichier `kestra/bottleneck_pipeline_kestra.yml` orchestre les tâches dans l'ordre suivant.

### 1. Netoyage des données

- `01_cleaning.py`
- nettoyage des colonnes et des types ;
- suppression des doublons ;
- normalisation des tables sources.

### 2. Tests de qualité après nettoyage

- `02_test_cleaning.py`
- vérifie qu'il n'y a pas de doublons sur `product_id` et `id_web` ;
- vérifie le nombre attendu de lignes après nettoyage.

### 3. Jointure des données

- `03_join.py`
- fusion des tables ERP, web et liaison ;
- construction d'une table unique de produits.

### 4. Tests de cohérence après jointure

- `04_test_join.py`
- validation des clés ;
- contrôle du volume final ;
- détection des doublons restants.

### 5. Calcul du chiffre d'affaires

- `05_calculate_ca.py`
- calcule le `chiffre_affaires` par ligne ;
- totalise le CA global.

### 6. Contrôle des totaux

- `06_test_totals.py`
- vérifie que le CA calculé est bien égal au montant attendu : `70568.60 €`.

### 7. Export du rapport

- `07_export_report.py`
- génère un fichier Excel : `output/rapport_chiffre_affaires.xlsx`.

### 8. Classification des vins

- `08_classify_wines.py`
- calcule le z-score sur les prix ;
- distingue les vins premium (`z_score > 2`) des vins ordinaires (`z_score <= 2`).

### 9. Validation du tri

- `09_test_scores.py`
- vérifie que 30 vins sont classés premium ;
- vérifie que les autres lignes restent dans la catégorie ordinaire.

### 10. Export final

- `10_export_wines.py`
- produit les fichiers :
  - `output/vins_premium.csv`
  - `output/vins_ordinaires.csv`

---

## Règles métier et contrôles de qualité

Le pipeline vérifie plusieurs règles importantes :

- absence de doublons sur les identifiants clés ;
- volume attendu après nettoyage : `825` lignes pour ERP nettoyé ;
- volume attendu après jointure : `714` lignes ;
- CA total attendu : `70568.60 €` ;
- classification premium : `30` produits ;
- les vins premium doivent avoir un `z_score` strictement supérieur à `2`.
