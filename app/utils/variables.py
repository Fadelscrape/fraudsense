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

# Descriptions détaillées pour le dictionnaire
VARIABLES_DESCRIPTIONS = {
    'Time': {
        'nom': 'Temps écoulé depuis la 1ère transaction',
        'explication': 'Nombre de secondes écoulées entre cette transaction et la première transaction du dataset.',
        'interpretation': 'Variable neutre — utilisée pour analyser les patterns temporels.',
        'correlation': 0.0,
        'exemple': 'Une transaction à 2h du matin (temps = 7200s) est plus suspecte.'
    },
    'Amount': {
        'nom': 'Montant de la transaction (€)',
        'explication': 'Le montant en euros de la transaction bancaire.',
        'interpretation': 'Un montant inhabituel par rapport aux habitudes du client est un signal de fraude.',
        'correlation': 0.006,
        'exemple': 'Un client qui achète toujours pour 20€ fait soudain un achat de 800€ → suspect.'
    },
    'V17': {
        'nom': 'Comportement suspect du terminal',
        'explication': 'Mesure le niveau de suspicion associé au terminal utilisé.',
        'interpretation': '⚠️ Signal le plus fort de fraude. Quand ce score est très négatif, le terminal a un comportement anormal — il a enregistré beaucoup de transactions suspectes récemment.',
        'correlation': -0.33,
        'exemple': 'Un terminal de distributeur ATM piraté aura un score très négatif.'
    },
    'V14': {
        'nom': 'Distance inhabituelle entre terminaux',
        'explication': 'Mesure la cohérence géographique entre transactions successives.',
        'interpretation': '⚠️ Signal fort de fraude. Quand ce score est très négatif, le client fait des transactions sur des terminaux géographiquement impossibles à atteindre en si peu de temps.',
        'correlation': -0.30,
        'exemple': 'Transaction à Paris à 10h00, puis à Lyon à 10h05 → physiquement impossible.'
    },
    'V12': {
        'nom': 'Fréquence anormale de transactions',
        'explication': 'Mesure si le nombre de transactions récentes est inhabituel.',
        'interpretation': '⚠️ Signal fort. Quand ce score est très négatif, le nombre de transactions est anormalement élevé en très peu de temps.',
        'correlation': -0.26,
        'exemple': '15 achats en 5 minutes → comportement typique d\'un fraudeur qui teste une carte volée.'
    },
    'V10': {
        'nom': 'Écart par rapport au profil client',
        'explication': 'Compare le comportement actuel avec les habitudes historiques du client.',
        'interpretation': 'Quand ce score est très négatif, le comportement actuel est très différent des habitudes normales du client.',
        'correlation': -0.22,
        'exemple': 'Un client qui n\'achète jamais en ligne fait soudain 3 achats en ligne → suspect.'
    },
    'V16': {
        'nom': 'Transactions suspectes sur le terminal',
        'explication': 'Historique de fraudes associé au terminal utilisé.',
        'interpretation': 'Quand ce score est très négatif, le terminal a un historique de fraudes détectées.',
        'correlation': -0.20,
        'exemple': 'Un terminal de magasin signalé pour skimming (vol de données de carte).'
    },
    'V3': {
        'nom': 'Écart du montant vs habitudes client',
        'explication': 'Compare le montant de cette transaction avec la moyenne habituelle du client.',
        'interpretation': 'Quand ce score est très négatif, le montant est très inhabituel par rapport aux dépenses habituelles.',
        'correlation': -0.19,
        'exemple': 'Client avec montant moyen de 30€ — transaction de 500€ → écart suspect.'
    },
    'V7': {
        'nom': 'Heure inhabituelle de transaction',
        'explication': 'Mesure si l\'heure de la transaction correspond aux habitudes du client.',
        'interpretation': 'Quand ce score est très négatif, la transaction se fait à une heure inhabituelle.',
        'correlation': -0.19,
        'exemple': 'Un client qui achète toujours entre 9h et 18h fait une transaction à 3h du matin → suspect.'
    },
    'V11': {
        'nom': 'Score de confiance du titulaire',
        'explication': 'Score de confiance basé sur l\'historique positif du client.',
        'interpretation': '✅ Signal de normalité. Quand ce score est élevé, le client a un long historique de transactions normales.',
        'correlation': 0.15,
        'exemple': 'Un client avec 5 ans d\'historique sans fraude a un score de confiance élevé.'
    },
    'V4': {
        'nom': 'Type et catégorie du marchand',
        'explication': 'Cohérence entre la catégorie du marchand et les habitudes d\'achat du client.',
        'interpretation': '✅ Signal de normalité. Quand ce score est élevé, la catégorie du marchand correspond aux habitudes du client.',
        'correlation': 0.13,
        'exemple': 'Un client qui achète souvent dans les supermarchés — transaction en supermarché → normal.'
    },
    'V2': {
        'nom': 'Distance géographique entre transactions',
        'explication': 'Cohérence de la localisation géographique des transactions.',
        'interpretation': '✅ Signal de normalité. Quand ce score est élevé, les transactions se font dans des zones cohérentes.',
        'correlation': 0.09,
        'exemple': 'Un client parisien qui achète toujours à Paris — transaction à Paris → normal.'
    },
}

# Dictionnaire inverse
VARIABLES_DICT_INVERSE = {v: k for k, v in VARIABLES_DICT.items()}

# Note de transparence
VARIABLES_NOTE = """⚠️ Note de transparence : Les variables V1-V28 sont des composantes issues d'une transformation PCA (Analyse en Composantes Principales) appliquée pour des raisons de confidentialité bancaire (dataset Worldline/ULB). Les interprétations proposées sont basées sur la littérature scientifique en détection de fraude — Fraud Detection Handbook (ULB)."""

# Top variables importantes
TOP_VARIABLES = [
    'V17', 'V14', 'V12', 'V10', 'V16',
    'V3',  'V7',  'V11', 'V4',  'V2'
]

def get_label(var):
    return VARIABLES_DICT.get(var, var)

def rename_features(df):
    return df.rename(columns=VARIABLES_DICT)
