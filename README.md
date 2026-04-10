# 🛡️ FraudSense — Détection de Fraude Bancaire

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red)
![XGBoost](https://img.shields.io/badge/XGBoost-3.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Description

FraudSense est une application web de détection de fraude bancaire développée avec Python et Streamlit. Elle utilise un modèle XGBoost optimisé par Optuna pour détecter les transactions frauduleuses en temps réel.

## 🎯 Performance du modèle

| Métrique | Score |
|----------|-------|
| AUPRC | **0.8833** |
| ROC-AUC | **0.9817** |
| Precision | **0.83** |
| Recall | **0.86** |

## 🚀 Fonctionnalités

- 📊 **Dashboard** — Visualisation interactive des transactions et fraudes
- 🔍 **Prédiction** — Analyse en temps réel via upload CSV ou saisie manuelle
- 🧠 **Explicabilité** — Interprétation des décisions via SHAP Values

## 🛠️ Stack technique

- **Langage** : Python 3.13
- **Application** : Streamlit
- **Modèle** : XGBoost + Optuna
- **Explicabilité** : SHAP
- **Visualisation** : Plotly
- **Rééquilibrage** : SMOTE

## 📁 Structure du projet

```
fraudsense/
├── app/
│   ├── app.py              # Application principale
│   ├── assets/
│   │   └── style.css       # Styles personnalisés
│   └── views/
│       ├── dashboard.py    # Page Dashboard
│       ├── prediction.py   # Page Prédiction
│       └── explicabilite.py# Page Explicabilité
├── data/
│   └── creditcard_sample.csv
├── model/
│   ├── fraud_model.pkl     # Modèle XGBoost
│   ├── scaler.pkl          # Scaler
│   └── config.json         # Configuration
├── notebooks/
│   └── 01_eda_model.ipynb  # Notebook EDA + Modélisation
└── requirements.txt
```

## 📊 Dataset

- **Source** : [Credit Card Fraud Detection — Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Transactions** : 284,807
- **Fraudes** : 492 (0.173%)
- **Variables** : Time, Amount, V1-V28 (PCA)

## ⚙️ Installation locale

```bash
# Cloner le repo
git clone https://github.com/Fadelscrape/fraudsense.git
cd fraudsense

# Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
cd app
streamlit run app.py
```

## 🧠 Méthodologie

1. **EDA** — Analyse exploratoire du déséquilibre des classes
2. **Preprocessing** — StandardScaler + scale_pos_weight
3. **Modélisation** — XGBoost optimisé par Optuna (50 essais)
4. **Évaluation** — AUPRC comme métrique principale (recommandation dataset)
5. **Explicabilité** — SHAP Values pour interpréter les décisions

## 👤 Auteur

**Fadel SOHOU** — Data Analyst & Data Scientist

---
*Développé avec Python, Streamlit, XGBoost & SHAP*
