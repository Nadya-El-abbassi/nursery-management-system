# Pépinière — Branche `feature-m2-crud`

Module **CRUD** (stock, ventes, catégories) pour l'application de gestion de pépinière.  
        Projet final — **Maintenance logicielle** · 2ACI INFO · Flask · SQLite.

> Cette branche couvre la **Partie M2** du projet .  


---

## Périmètre de cette branche

| Module | Route | Description |
|--------|-------|-------------|
| **Stock (CRUD)** | `/plants/` | Ajouter, modifier, supprimer des plantes |
| **Ventes** | `/sales/` | Historique et enregistrement de ventes (stock décrémenté automatiquement) |
| **Catégories (CRUD)** | `/categories/` | Gérer les catégories produits |


---

## Stack technique

- **Backend** : Python 3.10+, Flask 3
- **Base de données** : SQLite (`data/pepiniere.db`)
- **Frontend** : HTML, templates Jinja2
- **Devise** : MAD (dirham marocain)

---

## Fichiers livrés sur cette branche

```
app/
├── __init__.py
├── config.py
├── database.py
├── repositories/
│   ├── plant_repository.py
│   ├── sale_repository.py
│   └── category_repository.py
├── services/
│   ├── plant_service.py
│   ├── sale_service.py
│   ├── category_service.py
│   └── stock_alert_service.py
├── routes/
│   ├── plants.py
│   ├── sales.py
│   └── categories.py
└── templates/
    ├── plants/
    ├── sales/
    └── categories/
run.py
requirements.txt
sonar-project.properties
```

---

## Installation (branche M2)

### Prérequis

- Python **3.10** ou supérieur

### Étapes

```bash
git clone https://github.com/<votre-org>/nursery-management-system.git
git checkout feature-m2-crud
cd nursery-management-system

python -m venv venv
venv\Scripts\activate          # Windows

pip install -r requirements.txt
python run.py
```

Ouvrir **http://127.0.0.1:5000/plants/** (routes CRUD M2).

> **Note :** les templates M2 utilisent `base.html`, fourni par la branche M3.  
---

## Base de données

Tables créées par `app/database.py` :

| Table | Rôle |
|-------|------|
| `plants` | Stock de plantes (nom, espèce, prix MAD, quantité, seuil d'alerte) |
| `sales` | Ventes liées aux plantes |
| `categories` | Catégories produits (nom unique, description) |

Au premier lancement, des **données de démonstration** sont insérées :

- 6 plantes (lavande, rosier, olivier, menthe, géranium, thym)
- 4 catégories (Plantes, Engrais, Pots, Outils)

---

## Routes API / pages

| Méthode | URL | Action |
|---------|-----|--------|
| GET | `/plants/` | Liste du stock |
| GET/POST | `/plants/add` | Ajouter une plante |
| GET/POST | `/plants/<id>/edit` | Modifier une plante |
| POST | `/plants/<id>/delete` | Supprimer une plante |
| GET | `/sales/` | Historique des ventes |
| GET/POST | `/sales/new` | Nouvelle vente |
| GET | `/categories/` | Liste des catégories |
| GET/POST | `/categories/add` | Ajouter une catégorie |
| GET/POST | `/categories/<id>/edit` | Modifier une catégorie |
| POST | `/categories/<id>/delete` | Supprimer une catégorie |
