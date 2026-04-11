# 📋 Model Card — FraudSense

> Document de référence pour l'utilisation 
> et la compréhension du modèle de détection 
> de fraude bancaire.

---

## 1. 📌 Informations générales

| Champ | Détail |
|-------|--------|
| **Nom du modèle** | FraudSense — XGBoost Optuna |
| **Version** | 1.0 |
| **Date de création** | Avril 2026 |
| **Auteur** | SOHOU Fadel |
| **Type de problème** | Classification binaire (Fraude / Normal) |
| **Domaine** | Gestion des risques financiers |
| **Langue** | Python 3.13 |

---

## 2. 🎯 Objectif du modèle

Ce modèle a pour objectif de **détecter automatiquement 
les transactions bancaires frauduleuses** par carte de crédit, 
afin de protéger les clients contre les pertes financières.

Il répond à la problématique suivante :

> *"Comment identifier une transaction frauduleuse parmi 
> des centaines de milliers de transactions normales, 
> sachant que les fraudes représentent moins de 0,2% 
> des transactions ?"*

---

## 3. 📊 Dataset utilisé

| Champ | Détail |
|-------|--------|
| **Source** | [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| **Producteurs** | Worldline & Université Libre de Bruxelles (ULB) |
| **Période** | Septembre 2013 (2 jours) |
| **Transactions totales** | 284,807 |
| **Transactions frauduleuses** | 492 (0.173%) |
| **Transactions normales** | 284,315 (99.827%) |
| **Format** | CSV |
| **Taille** | 143 MB |

### Déséquilibre des classes

Le dataset est **extrêmement déséquilibré** : les fraudes 
représentent seulement 0.173% des transactions. C'est pourquoi 
la métrique principale recommandée est l'**AUPRC** 
(Area Under Precision-Recall Curve) plutôt que l'accuracy.

---

## 4. 📋 Description des variables

### Variables connues

| Variable | Type | Description |
|----------|------|-------------|
| `Time` | float | Secondes écoulées depuis la 1ère transaction |
| `Amount` | float | Montant de la transaction en euros |
| `Class` | int | Variable cible : 0=Normal, 1=Fraude |

### Variables anonymisées (V1-V28)

Les variables V1 à V28 sont des **composantes principales** 
obtenues par transformation PCA (Analyse en Composantes 
Principales), appliquée pour des raisons de confidentialité 
bancaire par Worldline.

> ⚠️ Les variables originales ne peuvent pas être divulguées 
> pour des raisons de confidentialité.

Basé sur la littérature en détection de fraude 
([Fraud Detection Handbook, ULB](https://fraud-detection-handbook.github.io/fraud-detection-handbook/)), 
voici les interprétations probables :

| Variable | Interprétation probable | Corrélation fraude | Signal |
|----------|------------------------|-------------------|--------|
| `V17` | Comportement suspect du terminal | -0.3265 | 🔴 Fort |
| `V14` | Distance inhabituelle entre terminaux | -0.3025 | 🔴 Fort |
| `V12` | Fréquence anormale de transactions | -0.2606 | 🔴 Fort |
| `V10` | Écart par rapport au profil client | -0.2169 | 🔴 Fort |
| `V16` | Transactions suspectes sur le terminal | -0.1965 | 🔴 Fort |
| `V3`  | Écart du montant vs habitudes client | -0.1930 | 🔴 Fort |
| `V7`  | Heure inhabituelle de transaction | -0.1873 | 🔴 Fort |
| `V18` | Tendance des montants récents | -0.1115 | 🟡 Modéré |
| `V1`  | Cohérence de localisation du client | -0.1013 | 🟡 Modéré |
| `V9`  | Volume de transactions récentes | -0.0977 | 🟡 Modéré |
| `V5`  | Fréquence journalière des transactions | -0.0950 | 🟡 Modéré |
| `V6`  | Cohérence horaire des transactions | -0.0436 | 🟡 Modéré |
| `V11` | Score de confiance du titulaire | +0.1549 | 🟢 Normal |
| `V4`  | Type et catégorie du marchand | +0.1334 | 🟢 Normal |
| `V2`  | Distance géographique entre transactions | +0.0913 | 🟢 Normal |
| `V21` | Indicateur de fraude historique | +0.0404 | 🟢 Faible |
| `V19` | Anomalie dans le pattern client | +0.0348 | 🟢 Faible |
| `V8`  | Répétition de transactions similaires | +0.0199 | ⚪ Neutre |
| `V20` | Cohérence du canal de paiement | +0.0201 | ⚪ Neutre |
| `V27` | Score de risque comportemental | +0.0176 | ⚪ Neutre |
| `V28` | Indicateur composite de fraude | +0.0095 | ⚪ Neutre |
| `V22` | Type appareil de paiement | +0.0008 | ⚪ Neutre |
| `V25` | Cohérence avec le profil bancaire | +0.0033 | ⚪ Neutre |
| `V26` | Variation du comportement client | +0.0045 | ⚪ Neutre |
| `V13` | Cohérence entre client et terminal | -0.0046 | ⚪ Neutre |
| `V15` | Historique utilisation de la carte | -0.0042 | ⚪ Neutre |
| `V23` | Niveau de sécurité de la transaction | -0.0027 | ⚪ Neutre |
| `V24` | Ratio montant vs limite de carte | -0.0072 | ⚪ Neutre |

---

## 5. 🤖 Architecture du modèle

| Champ | Détail |
|-------|--------|
| **Algorithme** | XGBoost (Extreme Gradient Boosting) |
| **Optimisation** | Optuna — Optimisation Bayésienne (50 essais) |
| **Gestion déséquilibre** | scale_pos_weight = 577.3 |
| **Split données** | 80% entraînement / 20% test |
| **Validation** | Cross-validation 3 folds |

### Hyperparamètres optimaux (Optuna)
```python
{
    'n_estimators'    : 416,
    'max_depth'       : 5,
    'learning_rate'   : 0.0997,
    'min_child_weight': 7,
    'subsample'       : 0.717,
    'colsample_bytree': 0.703,
    'gamma'           : 0.572,
    'reg_alpha'       : 1.518,
    'reg_lambda'      : 1.337,
    'scale_pos_weight': 577.3
}
```

---

## 6. 📈 Performance du modèle

### Métriques principales

| Métrique | Valeur | Description |
|----------|--------|-------------|
| **AUPRC** ⭐ | **0.8861** | Métrique principale recommandée |
| **ROC-AUC** | 0.9828 | Discrimination globale |
| **Précision fraude** | 0.84 | Sur 100 alertes, 84 sont vraies |
| **Rappel fraude** | 0.85 | 85% des fraudes détectées |
| **F1-Score fraude** | 0.84 | Équilibre précision/rappel |

### Matrice de confusion

| | Prédit Normal | Prédit Fraude |
|--|--|--|
| **Réel Normal** | 56,848 ✅ | 16 ⚠️ |
| **Réel Fraude** | 15 ❌ | 83 ✅ |

### Interprétation

- ✅ **83 fraudes détectées** sur 98 (84.7%)
- ⚠️ **16 fausses alertes** — transactions normales bloquées
- ❌ **15 fraudes manquées** — risque résiduel

---

## 7. ⚙️ Comment utiliser le modèle

### Prérequis
```python
# Packages nécessaires
pip install xgboost==3.2.0 scikit-learn==1.8.0 
            joblib==1.5.3 pandas==3.0.2 numpy==2.4.4
```

### Format des données d'entrée

Le modèle attend un DataFrame avec exactement 
ces colonnes dans cet ordre :
```python
colonnes_requises = [
    'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7',
    'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14',
    'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21',
    'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28',
    'Amount_scaled',  # Amount normalisé
    'Time_scaled'     # Time normalisé
]
```

### Normalisation obligatoire
```python
# Avant de faire une prédiction, normaliser Amount et Time
df['Amount_scaled'] = (df['Amount'] - 88.29) / 250.11
df['Time_scaled']   = (df['Time'] - 94813) / 47488
```

### Exemple de prédiction
```python
import joblib
import pandas as pd

# Charger le modèle
model = joblib.load('model/fraud_model.pkl')

# Préparer les données
df['Amount_scaled'] = (df['Amount'] - 88.29) / 250.11
df['Time_scaled']   = (df['Time'] - 94813) / 47488

features = ['V1','V2','V3','V4','V5','V6','V7','V8',
            'V9','V10','V11','V12','V13','V14','V15',
            'V16','V17','V18','V19','V20','V21','V22',
            'V23','V24','V25','V26','V27','V28',
            'Amount_scaled','Time_scaled']

X = df[features]

# Prédiction
probabilites = model.predict_proba(X)[:, 1]
predictions  = model.predict(X)

# Résultat
df['probabilite_fraude'] = probabilites
df['prediction'] = predictions.map({0: 'Normal', 1: 'Fraude'})
```

---

## 8. ⚠️ Limitations et biais

- **Données datées** : Le dataset date de septembre 2013 — 
  les patterns de fraude ont évolué depuis.
- **Données européennes** : Le modèle est entraîné sur 
  des transactions européennes — peut ne pas généraliser 
  à d'autres régions.
- **Variables anonymisées** : L'interprétabilité est limitée 
  car les variables originales sont inconnues.
- **Dataset statique** : Le modèle ne s'adapte pas aux 
  nouvelles formes de fraude sans réentraînement.
- **Seuil fixe** : Le seuil de décision (0.5) peut nécessiter 
  un ajustement selon le contexte métier.

---

## 9. 🔒 Considérations éthiques

- Ce modèle est conçu pour **assister** les analystes, 
  pas pour remplacer le jugement humain.
- Toute décision de bloquer une transaction doit être 
  **vérifiée manuellement** avant action.
- Les fausses alertes peuvent causer de l'inconfort 
  aux clients — minimiser les faux positifs est important.
- Le modèle doit être **régulièrement réévalué** pour 
  détecter tout biais émergent.

---

## 10. 📚 Références

- Dal Pozzolo et al. (2015). *Calibrating Probability with 
  Undersampling for Unbalanced Classification*. IEEE CIDM.
- Le Borgne & Bontempi (2022). *Reproducible Machine Learning 
  for Credit Card Fraud Detection*. ULB.
- [Fraud Detection Handbook](https://fraud-detection-handbook.github.io/fraud-detection-handbook/)
- [Dataset Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

---

## 11. 📁 Fichiers du modèle

| Fichier | Description |
|---------|-------------|
| `model/fraud_model.pkl` | Modèle XGBoost entraîné |
| `model/scaler.pkl` | StandardScaler (Amount + Time) |
| `model/config.json` | Configuration et métriques |
| `app/utils/variables.py` | Dictionnaire des variables |

---

*FraudSense v1.0 — Avril 2026 — SOHOU Fadel Data Analyst & Data scientist junior*
