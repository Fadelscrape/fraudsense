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
        'explication': 'Nombre de secondes écoulées entre cette transaction et la première transaction du dataset (sur 2 jours).',
        'interpretation': 'Variable temporelle neutre — utilisée pour reconstruire les patterns horaires.',
        'correlation': -0.0123,
        'signal': '⚪ Neutre',
        'exemple': 'Les transactions enregistrées dans les premières heures du dataset correspondent à la nuit, période plus risquée pour la fraude.'
    },
    'Amount': {
        'nom': 'Montant de la transaction (€)',
        'explication': 'Le montant en euros de la transaction bancaire.',
        'interpretation': 'Variable descriptive — le montant seul ne suffit pas à détecter une fraude mais combiné aux autres variables il apporte une information utile.',
        'correlation': 0.006,
        'signal': '⚪ Neutre',
        'exemple': 'Montant médian des fraudes : 9€ vs 22€ pour les transactions normales — les fraudeurs préfèrent les petits montants.'
    },
    'V17': {
        'nom': 'Comportement suspect du terminal',
        'explication': 'Mesure le niveau de suspicion associé au terminal utilisé.',
        'interpretation': '⚠️ Signal le plus fort de fraude. Quand ce score est très négatif, le terminal a un comportement anormal — il a enregistré beaucoup de transactions suspectes récemment.',
        'correlation': -0.3265,
        'signal': '🔴 Fort signal fraude',
        'exemple': 'Un terminal de distributeur ATM piraté aura un score très négatif.'
    },
    'V14': {
        'nom': 'Distance inhabituelle entre terminaux',
        'explication': 'Mesure la cohérence géographique entre transactions successives.',
        'interpretation': '⚠️ Signal fort de fraude. Quand ce score est très négatif, le client fait des transactions sur des terminaux géographiquement impossibles à atteindre en si peu de temps.',
        'correlation': -0.3025,
        'signal': '🔴 Fort signal fraude',
        'exemple': 'Transaction à Paris à 10h00, puis à Lyon à 10h05 → physiquement impossible.'
    },
    'V12': {
        'nom': 'Fréquence anormale de transactions',
        'explication': 'Mesure si le nombre de transactions récentes est inhabituel.',
        'interpretation': '⚠️ Signal fort. Quand ce score est très négatif, le nombre de transactions est anormalement élevé en très peu de temps.',
        'correlation': -0.2606,
        'signal': '🔴 Fort signal fraude',
        'exemple': '15 achats en 5 minutes → comportement typique d\'un fraudeur qui teste une carte volée.'
    },
    'V10': {
        'nom': 'Écart par rapport au profil client',
        'explication': 'Compare le comportement actuel avec les habitudes historiques du client.',
        'interpretation': 'Quand ce score est très négatif, le comportement actuel est très différent des habitudes normales du client.',
        'correlation': -0.2169,
        'signal': '🔴 Fort signal fraude',
        'exemple': 'Un client qui n\'achète jamais en ligne fait soudain 3 achats en ligne → suspect.'
    },
    'V16': {
        'nom': 'Transactions suspectes sur le terminal',
        'explication': 'Historique de fraudes associé au terminal utilisé.',
        'interpretation': 'Quand ce score est très négatif, le terminal a un historique de fraudes détectées.',
        'correlation': -0.1965,
        'signal': '🔴 Fort signal fraude',
        'exemple': 'Un terminal de magasin signalé pour skimming (vol de données de carte).'
    },
    'V3': {
        'nom': 'Écart du montant vs habitudes client',
        'explication': 'Compare le montant de cette transaction avec la moyenne habituelle du client.',
        'interpretation': 'Quand ce score est très négatif, le montant est très inhabituel par rapport aux dépenses habituelles.',
        'correlation': -0.1930,
        'signal': '🔴 Fort signal fraude',
        'exemple': 'Client avec montant moyen de 30€ — transaction de 500€ → écart suspect.'
    },
    'V7': {
        'nom': 'Heure inhabituelle de transaction',
        'explication': 'Mesure si l\'heure de la transaction correspond aux habitudes du client.',
        'interpretation': 'Quand ce score est très négatif, la transaction se fait à une heure inhabituelle.',
        'correlation': -0.1873,
        'signal': '🔴 Fort signal fraude',
        'exemple': 'Un client qui achète toujours entre 9h et 18h fait une transaction à 3h du matin → suspect.'
    },
    'V11': {
        'nom': 'Score de confiance du titulaire',
        'explication': 'Score de confiance basé sur l\'historique positif du client.',
        'interpretation': '✅ Signal de normalité. Quand ce score est élevé, le client a un long historique de transactions normales.',
        'correlation': 0.1549,
        'signal': '🟢 Signal normalité',
        'exemple': 'Un client avec 5 ans d\'historique sans fraude a un score de confiance élevé.'
    },
    'V4': {
        'nom': 'Type et catégorie du marchand',
        'explication': 'Cohérence entre la catégorie du marchand et les habitudes d\'achat du client.',
        'interpretation': '✅ Signal de normalité. Quand ce score est élevé, la catégorie du marchand correspond aux habitudes du client.',
        'correlation': 0.1334,
        'signal': '🟢 Signal normalité',
        'exemple': 'Un client qui achète souvent dans les supermarchés — transaction en supermarché → normal.'
    },
    'V2': {
        'nom': 'Distance géographique entre transactions',
        'explication': 'Cohérence de la localisation géographique des transactions.',
        'interpretation': '✅ Signal de normalité. Quand ce score est élevé, les transactions se font dans des zones cohérentes.',
        'correlation': 0.0913,
        'signal': '🟢 Signal normalité',
        'exemple': 'Un client parisien qui achète toujours à Paris — transaction à Paris → normal.'
    },
    'V1': {
        'nom': 'Cohérence de localisation du client',
        'explication': 'Mesure si la localisation de la transaction correspond à la zone habituelle du client.',
        'interpretation': 'Quand ce score est très négatif, le client effectue une transaction dans une zone géographique inhabituelle.',
        'correlation': -0.1013,
        'signal': '🟡 Signal fraude modéré',
        'exemple': 'Un client qui achète toujours à Abidjan fait une transaction à Paris sans voyage prévu → suspect.'
    },
    'V5': {
        'nom': 'Fréquence journalière des transactions',
        'explication': 'Nombre moyen de transactions effectuées par jour par ce client.',
        'interpretation': 'Une fréquence anormalement élevée en une journée peut indiquer une fraude.',
        'correlation': -0.0950,
        'signal': '🟡 Signal fraude modéré',
        'exemple': 'Un client qui fait 1-2 achats par jour en fait soudain 20 → comportement suspect.'
    },
    'V6': {
        'nom': 'Cohérence horaire des transactions',
        'explication': 'Mesure si les horaires des transactions correspondent aux habitudes du client.',
        'interpretation': 'Des transactions à des heures inhabituelles sont un signal de fraude.',
        'correlation': -0.0436,
        'signal': '🟡 Signal fraude modéré',
        'exemple': 'Un client qui achète toujours entre 8h et 20h fait une transaction à 4h du matin.'
    },
    'V8': {
        'nom': 'Répétition de transactions similaires',
        'explication': 'Détecte les transactions répétitives avec des montants similaires en peu de temps.',
        'interpretation': "Des achats répétitifs identiques sont typiques d'un fraudeur qui teste une carte volée.",
        'correlation': 0.0199,
        'signal': '⚪ Neutre',
        'exemple': '5 achats de 9.99€ en 10 minutes → test de carte volée.'
    },
    'V9': {
        'nom': 'Volume de transactions récentes',
        'explication': 'Nombre total de transactions effectuées par le client dans les dernières heures.',
        'interpretation': 'Un volume inhabituel de transactions récentes est un signal d\'alerte.',
        'correlation': -0.0977,
        'signal': '🟡 Signal fraude modéré',
        'exemple': '30 transactions en 2 heures pour un client qui en fait normalement 2 par jour → suspect.'
    },
    'V13': {
        'nom': 'Cohérence entre client et terminal',
        'explication': 'Mesure la compatibilité entre le profil du client et le terminal utilisé.',
        'interpretation': 'Une incohérence entre le client et le terminal peut indiquer une usurpation.',
        'correlation': -0.0046,
        'signal': '⚪ Neutre',
        'exemple': 'Un client particulier qui utilise un terminal professionnel réservé aux entreprises.'
    },
    'V15': {
        'nom': 'Historique utilisation de la carte',
        'explication': 'Ancienneté et fréquence d\'utilisation de la carte bancaire.',
        'interpretation': 'Une carte nouvellement émise avec beaucoup de transactions est suspecte.',
        'correlation': -0.0042,
        'signal': '⚪ Neutre',
        'exemple': 'Une carte émise il y a 2 jours avec déjà 50 transactions → suspect.'
    },
    'V18': {
        'nom': 'Tendance des montants récents',
        'explication': 'Évolution des montants des transactions sur les dernières heures.',
        'interpretation': 'Une tendance à la hausse rapide des montants est un signal de fraude.',
        'correlation': -0.1115,
        'signal': '🟡 Signal fraude modéré',
        'exemple': '10€, 50€, 200€, 800€ en quelques heures → escalade typique de fraude.'
    },
    'V19': {
        'nom': 'Anomalie dans le pattern client',
        'explication': 'Détecte les comportements qui s\'écartent significativement des habitudes du client.',
        'interpretation': 'Plus ce score est élevé, plus le comportement est cohérent avec le profil habituel.',
        'correlation': 0.0348,
        'signal': '🟢 Signal normalité',
        'exemple': 'Un client qui achète toujours des vêtements fait soudain des achats en bijouterie → anomalie.'
    },
    'V20': {
        'nom': 'Cohérence du canal de paiement',
        'explication': 'Vérifie si le canal utilisé (en ligne, physique, sans contact) correspond aux habitudes.',
        'interpretation': 'Un changement soudain de canal de paiement peut indiquer une fraude.',
        'correlation': 0.0201,
        'signal': '⚪ Neutre',
        'exemple': 'Un client qui paie toujours en physique fait soudain 10 achats en ligne → suspect.'
    },
    'V21': {
        'nom': 'Indicateur de fraude historique',
        'explication': 'Score basé sur l\'historique de fraudes similaires dans la base de données.',
        'interpretation': 'Plus ce score est élevé, plus la transaction ressemble à des fraudes passées connues.',
        'correlation': 0.0404,
        'signal': '🟢 Signal normalité',
        'exemple': 'Transaction similaire à 500 fraudes détectées précédemment → signal fort.'
    },
    'V22': {
        'nom': 'Type appareil de paiement',
        'explication': 'Caractéristiques de l\'appareil utilisé pour effectuer la transaction.',
        'interpretation': 'Un appareil inconnu ou inhabituel peut indiquer une fraude.',
        'correlation': 0.0008,
        'signal': '⚪ Neutre',
        'exemple': 'Paiement depuis un appareil jamais utilisé par ce client → vérification nécessaire.'
    },
    'V23': {
        'nom': 'Niveau de sécurité de la transaction',
        'explication': 'Score de sécurité basé sur le protocole d\'authentification utilisé.',
        'interpretation': 'Une transaction sans authentification forte est plus risquée.',
        'correlation': -0.0027,
        'signal': '⚪ Neutre',
        'exemple': 'Transaction sans code PIN ni 3D Secure sur un gros montant → risque élevé.'
    },
    'V24': {
        'nom': 'Ratio montant vs limite de carte',
        'explication': 'Composante PCA liée aux caractéristiques financières de la transaction.',
        'interpretation': 'Signal neutre — faible impact sur la détection de fraude.',
        'correlation': -0.0072,
        'signal': '⚪ Neutre',
        'exemple': 'Cette variable a peu d\'influence sur la décision du modèle (corrélation < 0.01).'
    },
    'V25': {
        'nom': 'Cohérence avec le profil bancaire',
        'explication': 'Compatibilité entre la transaction et le profil bancaire global du client.',
        'interpretation': 'Une transaction incompatible avec le profil bancaire est suspecte.',
        'correlation': 0.0033,
        'signal': '⚪ Neutre',
        'exemple': 'Un compte épargne qui fait soudain des achats de luxe → incohérence de profil.'
    },
    'V26': {
        'nom': 'Variation du comportement client',
        'explication': 'Mesure le degré de changement dans le comportement d\'achat du client.',
        'interpretation': 'Une variation soudaine et importante du comportement est un signal d\'alerte.',
        'correlation': 0.0045,
        'signal': '⚪ Neutre',
        'exemple': 'Habituellement 2 achats/semaine → soudainement 20 achats en 1 jour.'
    },
    'V27': {
        'nom': 'Score de risque comportemental',
        'explication': 'Score composite basé sur l\'analyse du comportement global de la transaction.',
        'interpretation': 'Ce score agrège plusieurs signaux comportementaux en un indicateur unique.',
        'correlation': 0.0176,
        'signal': '⚪ Neutre',
        'exemple': 'Score élevé = combinaison de plusieurs signaux suspects détectés simultanément.'
    },
    'V28': {
        'nom': 'Indicateur composite de fraude',
        'explication': 'Indicateur final combinant plusieurs facteurs de risque identifiés.',
        'interpretation': 'Ce score résume l\'ensemble des signaux d\'alerte détectés sur la transaction.',
        'correlation': 0.0095,
        'signal': '⚪ Neutre',
        'exemple': 'Un score élevé signifie que plusieurs critères de fraude sont réunis en même temps.'
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
