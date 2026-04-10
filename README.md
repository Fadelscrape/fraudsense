# 🛡️ FraudSense — Détection de Fraude Bancaire

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red)
![XGBoost](https://img.shields.io/badge/XGBoost-3.2-green)
![SHAP](https://img.shields.io/badge/SHAP-0.51-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> Application de détection de fraude par carte bancaire
> propulsée par XGBoost Optuna et expliquée par SHAP.

🔗 **[Voir l'application en ligne](https://fraudsense-d965nmu29nca4pyjzud59n.streamlit.app)**

---

## 📋 Contexte

Les sociétés de cartes de crédit doivent être capables
de reconnaître les transactions frauduleuses afin que
les clients ne soient pas facturés pour des achats
qu'ils n'ont pas effectués.

Ce projet utilise le dataset
[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
de Kaggle contenant **284,807 transactions** réelles
effectuées par des titulaires européens en septembre 2013.

---

## 🎯 Problématique

Le dataset est **extrêmement déséquilibré** :
- 284,315 transactions normales (99.827%)
- 492 transactions frauduleuses (0.173%)

La métrique principale recommandée est l'**AUPRC**
(Area Under Precision-Recall Curve) plutôt que
la précision classique.

---

## Architecture du projet

```
fraudsense/
├── data/
│   └── creditcard_sample.csv    ← échantillon 10,000 lignes
├── notebooks/
│   └── 01_eda_model.ipynb       ← EDA + modélisation
├── model/
│   ├── fraud_model.pkl          ← modèle XGBoost Optuna
│   ├── scaler.pkl               ← StandardScaler
│   └── config.json              ← configuration
├── app/
│   ├── app.py                   ← application principale
│   ├── assets/
│   │   └── style.css            ← styles CSS
│   ├── views/
│   │   ├── dashboard.py         ← page Dashboard
│   │   ├── prediction.py        ← page Prédiction
│   │   └── explicabilite.py     ← page Explicabilité
│   └── utils/
│       └── data_loader.py       ← chargement dataset
└── requirements.txt
```

---

## 📊 Résultats du modèle

| Modèle | AUPRC | ROC-AUC | Précision | Recall | F1 Fraude |
|--------|-------|---------|-----------|--------|-----------|
| SMOTE + XGBoost | 0.8270 | 0.9760 | 0.35 | 0.87 | 0.49 |
| scale_pos_weight | 0.8675 | 0.9758 | 0.76 | 0.84 | 0.80 |
| GridSearch | 0.8737 | 0.9748 | 0.87 | 0.83 | 0.85 |
| **XGBoost Optuna ✅** | **0.8861** | **0.9828** | **0.84** | **0.85** | **0.84** |

### Matrice de confusion — Modèle final

| | Prédit Normal | Prédit Fraude |
|--|--|--|
| **Réel Normal** | 56,848 ✅ | 16 ⚠️ |
| **Réel Fraude** | 15 ❌ | 83 ✅ |

- Taux de détection des fraudes : **84.7%** (83/98)
- Précision fraude : **83.8%**
- Fausses alertes : seulement **16** sur 56,864 transactions normales

---

## 🚀 Fonctionnalités de l'application

### 📊 Dashboard
- KPIs en temps réel (transactions, fraudes, taux, montants)
- Distribution des classes (graphique donut)
- Analyse temporelle des fraudes par heure
- Corrélation des variables V1-V28 avec la fraude
- Distribution des montants par classe

### 🔍 Prédiction
- Upload de fichier CSV de transactions
- Prédiction en temps réel avec score de probabilité
- Gauge chart de risque
- Filtres par statut et niveau de risque
- Export des résultats en CSV
- Saisie manuelle d'une transaction

### Explicabilité (SHAP)
- Importance globale des variables
- Impact des variables sur les prédictions
- Analyse SHAP par transaction individuelle
- Courbes ROC et Précision-Rappel

---

## Technologies utilisées

| Catégorie | Outils |
|-----------|--------|
| **Langage** | Python 3.13 |
| **ML** | XGBoost, Scikit-learn, Optuna |
| **Explicabilité** | SHAP |
| **Visualisation** | Plotly, Matplotlib, Seaborn |
| **Application** | Streamlit |
| **Données** | Pandas, NumPy |

---

##  Installation locale

```bash
# Cloner le repo
git clone https://github.com/Fadelscrape/fraudsense.git
cd fraudsense

# Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt

# Télécharger le dataset
# Placer creditcard.csv dans le dossier data/

# Lancer l'application
cd app
streamlit run app.py
```

---

## Dataset

Le dataset complet (143MB) n'est pas inclus dans
ce repository. L'application le télécharge
automatiquement depuis Kaggle au démarrage.

Pour une utilisation locale, téléchargez le dataset
depuis [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
et placez `creditcard.csv` dans le dossier `data/`.

---

## 👤 Auteur

**SOHOU Fadel** Data Analyst & Data scientist junior
- GitHub: [@Fadelscrape](https://github.com/Fadelscrape)

---

## Licence

Ce projet est sous licence MIT — voir le fichier
[LICENSE](LICENSE) pour plus de détails.
