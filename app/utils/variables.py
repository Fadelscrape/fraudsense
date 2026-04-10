# ============================================================
# DICTIONNAIRE DES VARIABLES — FraudSense
# Basé sur la littérature en détection de fraude bancaire
# Source : Fraud Detection Handbook (ULB/Worldline)
# ============================================================

VARIABLES_DICT = {
    'Time'          : 'Temps écoulé depuis la 1ère transaction',
    'Amount'        : 'Montant de la transaction (€)',
    'Amount_scaled' : 'Montant normalisé',
    'Time_scaled'   : 'Temps normalisé',
    'V1'  : 'Cohérence de localisation du client',
    'V2'  : 'Distance géographique entre transactions',
    'V3'  : 'Écart du montant vs habitudes client',
    'V4'  : 'Type et catégorie du marchand',
    'V5'  : 'Fréquence journalière des transactions',
    'V6'  : 'Cohérence horaire des transactions',
    'V7'  : 'Heure inhabituelle de transaction',
    'V8'  : 'Répétition de transactions similaires',
    'V9'  : 'Volume de transactions récentes',
    'V10' : 'Écart par rapport au profil client',
    'V11' : 'Score de confiance du titulaire',
    'V12' : 'Fréquence anormale de transactions',
    'V13' : 'Cohérence entre client et terminal',
    'V14' : 'Distance inhabituelle entre terminaux',
    'V15' : 'Historique utilisation de la carte',
    'V16' : 'Transactions suspectes sur le terminal',
    'V17' : 'Comportement suspect du terminal',
    'V18' : 'Tendance des montants récents',
    'V19' : 'Anomalie dans le pattern client',
    'V20' : 'Cohérence du canal de paiement',
    'V21' : 'Indicateur de fraude historique',
    'V22' : 'Type appareil de paiement',
    'V23' : 'Niveau de sécurité de la transaction',
    'V24' : 'Ratio montant vs limite de carte',
    'V25' : 'Cohérence avec le profil bancaire',
    'V26' : 'Variation du comportement client',
    'V27' : 'Score de risque comportemental',
    'V28' : 'Indicateur composite de fraude',
}

# Dictionnaire inverse (nom lisible → nom technique)
VARIABLES_DICT_INVERSE = {v: k for k, v in VARIABLES_DICT.items()}

# Note de transparence
VARIABLES_NOTE = """
⚠️ Note : Les variables V1-V28 sont des composantes issues
d'une transformation PCA appliquée pour des raisons de
confidentialité bancaire (dataset Worldline/ULB).
Les interprétations proposées sont basées sur la littérature
en détection de fraude — Fraud Detection Handbook (ULB).
"""

# Top variables les plus importantes (basé sur SHAP)
TOP_VARIABLES = [
    'V17', 'V14', 'V12', 'V10', 'V16',
    'V3',  'V7',  'V11', 'V4',  'V2'
]

def get_label(var):
    return VARIABLES_DICT.get(var, var)

def rename_features(df):
    return df.rename(columns=VARIABLES_DICT)
