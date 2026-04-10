# ============================================================
# FRAUDSENSE — Page Dashboard
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from utils.variables import VARIABLES_DICT, VARIABLES_NOTE, get_label

# ── Chargement des données ────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    from utils.data_loader import download_dataset
    data_path, source = download_dataset()
    df = pd.read_csv(data_path)
    df['Hour'] = (df['Time'] / 3600) % 24
    df['Amount_log'] = np.log1p(df['Amount'])
    df['Class_label'] = df['Class'].map({0: 'Normal', 1: 'Fraude'})
    return df, source

def show():
    df, source = load_data()
    if source == "kaggle":
        st.toast("Dataset téléchargé depuis Kaggle — 284,807 transactions", icon="✅")
    elif source == "sample":
        st.toast("ℹ️ Mode démonstration — échantillon 10,000 transactions", icon="ℹ️")
    df_sample = df.sample(50000, random_state=42) if len(df) > 50000 else df

    # ── 1. Header ─────────────────────────────────────────
    st.markdown('''
        <div class="page-header">
            <h1>📊 Dashboard — Vue générale</h1>
            <p>Analyse exploratoire des transactions bancaires · Dataset : 284 807 transactions</p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown("""
<div style='background:#EFF6FF; border-radius:12px;
            padding:16px 20px; margin-bottom:20px;
            border-left:4px solid #1B3A6B;'>
    <strong>📌 Contexte de l'analyse</strong><br><br>
    Ce dashboard analyse <strong>284 807 transactions</strong>
    par carte bancaire effectuées en septembre 2013 par des
    titulaires européens. Sur ces transactions,
    <strong style='color:#E63946;'>492 sont frauduleuses</strong>,
    soit environ <strong>1 fraude sur 578 transactions</strong>.
    L'objectif est d'identifier automatiquement ces fraudes
    grâce au machine learning pour protéger les clients.
</div>
""", unsafe_allow_html=True)

    # ── 2. KPI Cards ──────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    fraudes = df['Class'].sum()
    taux = fraudes / total * 100
    montant_moyen_fraude = df[df['Class']==1]['Amount'].mean()

    with col1:
        st.markdown(f'''
            <div class="kpi-card">
                <div style="font-size:32px;">💳</div>
                <div class="kpi-value">{total:,}</div>
                <div class="kpi-label">Transactions totales</div>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
            <div class="kpi-card" style="border-left-color:#E63946;">
                <div style="font-size:32px;">🚨</div>
                <div class="kpi-value" style="color:#E63946;">{fraudes:,}</div>
                <div class="kpi-label">Fraudes détectées</div>
            </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
            <div class="kpi-card" style="border-left-color:#F4A261;">
                <div style="font-size:32px;">📉</div>
                <div class="kpi-value" style="color:#F4A261;">{taux:.3f}%</div>
                <div class="kpi-label">Taux de fraude</div>
            </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown(f'''
            <div class="kpi-card" style="border-left-color:#2DC653;">
                <div style="font-size:32px;">💰</div>
                <div class="kpi-value" style="color:#2DC653;">{montant_moyen_fraude:.0f}€</div>
                <div class="kpi-label">Montant moyen fraude</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 3. Interprétation des KPIs ────────────────────────
    st.markdown("""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Ce que ces chiffres signifient :</strong>
    Sur 578 transactions bancaires, une seule est frauduleuse.
    Bien que rare (0.173%), chaque fraude représente une perte
    financière réelle pour le client. Le montant moyen d'une
    fraude est de <strong>122€</strong> — soit plus que la
    moyenne des transactions normales (88€).
</div>
""", unsafe_allow_html=True)

    # ── 4. Répartition des classes + Distribution montants ─
    col1, col2 = st.columns([1, 2])

    with col1:
        fig_pie = go.Figure(go.Pie(
            labels=['Normal', 'Fraude'],
            values=[total - fraudes, fraudes],
            hole=0.65,
            marker=dict(colors=['#1B3A6B', '#E63946'],
                       line=dict(color='white', width=2)),
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>%{value:,} transactions<br>%{percent}<extra></extra>'
        ))
        fig_pie.add_annotation(
            text=f"<b>{taux:.3f}%</b><br>fraudes",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#E63946')
        )
        fig_pie.update_layout(
            title=dict(text="Répartition des classes",
                      font=dict(size=16, color='#1B3A6B')),
            showlegend=True,
            height=320,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', y=-0.1)
        )
        with st.container(border=True):
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df_sample[df_sample['Class']==0]['Amount'],
            name='Normal',
            marker_color='#1B3A6B',
            boxpoints='outliers',
            line=dict(width=2)
        ))
        fig_box.add_trace(go.Box(
            y=df_sample[df_sample['Class']==1]['Amount'],
            name='Fraude',
            marker_color='#E63946',
            boxpoints='outliers',
            line=dict(width=2)
        ))
        fig_box.update_layout(
            title=dict(text="Distribution des montants par classe",
                      font=dict(size=16, color='#1B3A6B')),
            yaxis=dict(title='Montant (€)', type='log'),
            height=320,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )
        with st.container(border=True):
            st.plotly_chart(fig_box, use_container_width=True)

    # ── 5. Interprétation montants ────────────────────────
    st.markdown("""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Observation clé :</strong>
    Contrairement aux idées reçues, les fraudeurs n'effectuent
    <strong>pas de grosses transactions</strong>. Avec une médiane
    de seulement <strong>9€</strong>, ils préfèrent de petits
    montants pour passer inaperçus et éviter les alertes
    automatiques des banques.
</div>
""", unsafe_allow_html=True)

    # ── 6. Timeline transactions & taux de fraude ─────────
    fraude_rate = df.groupby(df['Hour'].astype(int))['Class'].agg(['sum', 'count'])
    fraude_rate['taux'] = fraude_rate['sum'] / fraude_rate['count'] * 100

    fig_timeline = make_subplots(specs=[[{"secondary_y": True}]])
    fig_timeline.add_trace(
        go.Bar(
            x=fraude_rate.index,
            y=fraude_rate['count'],
            name='Total des transactions',
            marker_color='#E8EFF8',
            hovertemplate='%{x}h : %{y:,} transactions<extra></extra>'
        ), secondary_y=False
    )
    fig_timeline.add_trace(
        go.Scatter(
            x=fraude_rate.index,
            y=fraude_rate['taux'],
            name='Taux de fraude (%)',
            line=dict(color='#E63946', width=3),
            mode='lines+markers',
            marker=dict(size=8, color='#E63946'),
            hovertemplate='%{x}h : %{y:.3f}%<extra></extra>'
        ), secondary_y=True
    )
    fig_timeline.update_layout(
        title=dict(text="📅 Timeline : Transactions & Taux de fraude par heure",
                  font=dict(size=16, color='#1B3A6B')),
        height=350,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', y=-0.15),
        xaxis=dict(
            title='Heure de la journée',
            dtick=1,
            range=[-0.5, 23.5],
            tick0=0,
            tickmode='linear'
        )
    )
    fig_timeline.update_yaxes(title_text="Nombre de transactions",
                               secondary_y=False)
    fig_timeline.update_yaxes(title_text="Taux de fraude (%)",
                               secondary_y=True,
                               color='#E63946')
    with st.container(border=True):
        st.plotly_chart(fig_timeline, use_container_width=True)

    # ── 7. Interprétation timeline ────────────────────────
    st.markdown("""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Observation clé :</strong>
    Le risque de fraude est <strong>10 fois plus élevé</strong>
    entre <strong>minuit et 5h du matin</strong> (taux jusqu'à 1.7%)
    comparé au reste de la journée (0.17% en moyenne).
    C'est la période où les victimes dorment et ne surveillent
    pas leurs comptes bancaires.
</div>
""", unsafe_allow_html=True)

    # ── 8. Corrélations + Fraudes par heure ───────────────
    col1, col2 = st.columns(2)

    with col1:
        # Corrélations avec signe (sans .abs())
        df_numeric = df.select_dtypes(include=[np.number])
        correlations = df_numeric.corr()['Class'].drop(
            ['Class', 'Hour', 'Amount_log'], errors='ignore'
        ).sort_values()

        # Garder top 8 négatives + top 7 positives
        corr_neg = correlations.head(8)
        corr_pos = correlations.tail(7)
        correlations_display = pd.concat([corr_neg, corr_pos])
        correlations_display.index = [
            get_label(v) for v in correlations_display.index
        ]

        # Couleurs selon le signe
        colors = ['#E63946' if v < 0 else '#1B3A6B'
                  for v in correlations_display.values]

        fig_corr = go.Figure(go.Bar(
            x=correlations_display.values,
            y=correlations_display.index,
            orientation='h',
            marker_color=colors,
            hovertemplate='%{y} : %{x:.4f}<extra></extra>'
        ))
        fig_corr.add_vline(x=0, line=dict(color='black', width=1.5))
        fig_corr.update_layout(
            title=dict(
                text="🔍 Corrélations avec la fraude (négatif = signal fort)",
                font=dict(size=16, color='#1B3A6B')
            ),
            height=500,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='Corrélation',
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
                range=[-0.4, 0.2]
            )
        )
        with st.container(border=True):
            st.plotly_chart(fig_corr, use_container_width=True)

    with col2:
        pivot = df.groupby([df['Hour'].astype(int)])['Class'].agg(
            ['sum', 'count']
        )
        pivot['taux'] = pivot['sum'] / pivot['count'] * 100

        fig_heat = go.Figure(go.Bar(
            x=pivot.index,
            y=pivot['sum'],
            marker=dict(
                color=pivot['taux'],
                colorscale=[[0, '#E8EFF8'], [0.5, '#F4A261'], [1, '#E63946']],
                showscale=True,
                colorbar=dict(title='Taux %', thickness=15)
            ),
            hovertemplate='%{x}h<br>Fraudes : %{y}<br>Taux : %{marker.color:.3f}%<extra></extra>'
        ))
        fig_heat.update_layout(
            title=dict(text="🕐 Fraudes par heure (intensité = taux)",
                      font=dict(size=16, color='#1B3A6B')),
            height=400,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Heure', dtick=1),
            yaxis=dict(title='Nombre de fraudes')
        )
        with st.container(border=True):
            st.plotly_chart(fig_heat, use_container_width=True)

    # ── 9. Interprétation corrélations ────────────────────
    st.markdown("""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Comment lire ces graphiques :</strong>
    À gauche — les barres <strong style='color:#E63946;'>rouges</strong>
    sont les signaux les plus forts de fraude. Le
    <strong>"Comportement suspect du terminal"</strong> est
    le signal le plus puissant (corrélation -0.33).
    À droite — <strong>2h du matin</strong> est l'heure
    la plus risquée avec le taux de fraude le plus élevé.
</div>
""", unsafe_allow_html=True)

    # ── 10. Footer ────────────────────────────────────────
    st.markdown('''
        <div style="text-align:center; padding:20px;
                    color:#6B7280; font-size:12px; margin-top:20px;">
            FraudSense · Powered by XGBoost Optuna ·
            Dataset : Credit Card Fraud Detection (Kaggle)
        </div>
    ''', unsafe_allow_html=True)