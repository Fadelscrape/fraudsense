# ============================================================
# FRAUDSENSE — Page Prédiction
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import json
import os

# ── Chargement du modèle ──────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    base = os.path.join(os.path.dirname(__file__), '../../model')
    model  = joblib.load(os.path.join(base, 'fraud_model.pkl'))
    scaler = joblib.load(os.path.join(base, 'scaler.pkl'))
    with open(os.path.join(base, 'config.json')) as f:
        config = json.load(f)
    return model, scaler, config

def gauge_chart(prob):
    color = '#E63946' if prob > 0.5 else '#F4A261' if prob > 0.3 else '#2DC653'
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prob * 100,
        number=dict(suffix='%', font=dict(size=36, color=color)),
        delta=dict(reference=50, valueformat='.1f'),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1,
                     tickcolor='#1B3A6B', dtick=25),
            bar=dict(color=color, thickness=0.3),
            bgcolor='#F8F9FC',
            borderwidth=0,
            steps=[
                dict(range=[0, 30],  color='#D1FAE5'),
                dict(range=[30, 60], color='#FEF3C7'),
                dict(range=[60, 100], color='#FEE2E2')
            ],
            threshold=dict(
                line=dict(color='#1B3A6B', width=3),
                thickness=0.8, value=50
            )
        ),
        title=dict(text="Score de risque", font=dict(size=16))
    ))
    fig.update_layout(
        height=280,
        margin=dict(t=30, b=10, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def predict_transactions(df_input, model, scaler, config):
    features = config['features']
    # Normalisation Amount et Time
    if 'Amount' in df_input.columns and 'Time' in df_input.columns:
        df_input['Amount_scaled'] = df_input['Amount'].apply(
            lambda x: (x - 88.29) / 250.11
        )
        df_input['Time_scaled'] = df_input['Time'].apply(
            lambda x: (x - 94813) / 47488
        )
    elif 'Amount' in df_input.columns:
        df_input['Amount_scaled'] = df_input['Amount'].apply(
            lambda x: (x - 88.29) / 250.11
        )

    # Sélection des features
    available = [f for f in features if f in df_input.columns]
    X = df_input[available]

    probs  = model.predict_proba(X)[:, 1]
    preds  = (probs >= 0.5).astype(int)
    return probs, preds

def show():
    model, scaler, config = load_model()

    # ── Header ────────────────────────────────────────────
    st.markdown('''
        <div class="page-header">
            <h1>🔍 Prédiction de fraude</h1>
            <p>Analysez vos transactions en temps réel · 
               Modèle : XGBoost Optuna · AUPRC : 0.8833</p>
        </div>
    ''', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📁 Charger un CSV", "✏️ Saisie manuelle"])

    # ════════════════════════════════════════════════════
    # TAB 1 — Upload CSV
    # ════════════════════════════════════════════════════
    with tab1:

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📂 Charger un fichier de transactions")
            st.markdown(
                "Chargez un fichier CSV contenant vos transactions. "
                "Le fichier doit contenir les colonnes `Time`, `Amount`, `V1`...`V28`."
            )
            uploaded = st.file_uploader(
                "Choisir un fichier CSV",
                type=['csv'],
                help="Format attendu : colonnes Time, Amount, V1-V28"
            )

        with col2:
            st.markdown("### 📋 Format attendu")
            sample = pd.DataFrame({
                'Time': [0, 1, 2],
                'Amount': [149.62, 2.69, 378.66],
                'V1': [-1.36, 1.19, -1.36],
                'V2': [-0.07, 0.26, -0.07],
                '...': ['...', '...', '...']
            })
            st.dataframe(sample, hide_index=True, use_container_width=True)

        if uploaded:
            df_upload = pd.read_csv(uploaded)
            probs, preds = predict_transactions(
                df_upload.copy(), model, scaler, config
            )

            df_upload['Probabilité (%)'] = (probs * 100).round(2)
            df_upload['Prédiction'] = preds
            df_upload['Statut'] = df_upload['Prédiction'].map(
                {0: '✅ Normal', 1: '🚨 Fraude'}
            )
            df_upload['Risque'] = pd.cut(
                probs,
                bins=[0, 0.3, 0.6, 1.0],
                labels=['🟢 Faible', '🟡 Moyen', '🔴 Élevé']
            )

            # ── KPIs résultats ────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            nb_fraudes = preds.sum()
            nb_normal  = len(preds) - nb_fraudes
            taux_f     = nb_fraudes / len(preds) * 100
            moy_prob   = probs.mean() * 100

            with c1:
                st.markdown(f'''
                    <div class="kpi-card">
                        <div style="font-size:28px;">📊</div>
                        <div class="kpi-value">{len(preds):,}</div>
                        <div class="kpi-label">Transactions analysées</div>
                    </div>
                ''', unsafe_allow_html=True)
            with c2:
                st.markdown(f'''
                    <div class="kpi-card" style="border-left-color:#E63946;">
                        <div style="font-size:28px;">🚨</div>
                        <div class="kpi-value" style="color:#E63946;">
                            {nb_fraudes}
                        </div>
                        <div class="kpi-label">Fraudes détectées</div>
                    </div>
                ''', unsafe_allow_html=True)
            with c3:
                st.markdown(f'''
                    <div class="kpi-card" style="border-left-color:#2DC653;">
                        <div style="font-size:28px;">✅</div>
                        <div class="kpi-value" style="color:#2DC653;">
                            {nb_normal:,}
                        </div>
                        <div class="kpi-label">Transactions normales</div>
                    </div>
                ''', unsafe_allow_html=True)
            with c4:
                st.markdown(f'''
                    <div class="kpi-card" style="border-left-color:#F4A261;">
                        <div style="font-size:28px;">📉</div>
                        <div class="kpi-value" style="color:#F4A261;">
                            {taux_f:.2f}%
                        </div>
                        <div class="kpi-label">Taux de fraude</div>
                    </div>
                ''', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Filtres ───────────────────────────────
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filtre_statut = st.multiselect(
                    "Filtrer par statut",
                    ['✅ Normal', '🚨 Fraude'],
                    default=['✅ Normal', '🚨 Fraude']
                )
            with col_f2:
                filtre_risque = st.multiselect(
                    "Filtrer par niveau de risque",
                    ['🟢 Faible', '🟡 Moyen', '🔴 Élevé'],
                    default=['🟢 Faible', '🟡 Moyen', '🔴 Élevé']
                )

            df_filtered = df_upload[
                (df_upload['Statut'].isin(filtre_statut)) &
                (df_upload['Risque'].isin(filtre_risque))
            ]

            # ── Tableau résultats ─────────────────────
            cols_display = ['Time', 'Amount', 'Probabilité (%)',
                           'Statut', 'Risque']
            cols_display = [c for c in cols_display
                           if c in df_filtered.columns]
            # Limite l'affichage à 1000 lignes max
            df_display = df_filtered[cols_display].head(1000)

            if len(df_display) < 50000:
                st.dataframe(
                    df_display.style.background_gradient(
                        subset=['Probabilité (%)'],
                        cmap='RdYlGn_r',
                        vmin=0, vmax=100
                    ),
                    use_container_width=True,
                    height=400
                )
            else:
                st.dataframe(
                    df_display,
                    use_container_width=True,
                    height=400
                )

            if len(df_filtered) > 1000:
                st.info(f"Affichage limité à 1000 lignes sur {len(df_filtered):,} résultats.")

            # ── Export ────────────────────────────────
            csv_export = df_filtered.to_csv(index=False)
            st.download_button(
                label="⬇️ Télécharger les résultats",
                data=csv_export,
                file_name="fraudsense_resultats.csv",
                mime="text/csv"
            )

    # ════════════════════════════════════════════════════
    # TAB 2 — Saisie manuelle
    # ════════════════════════════════════════════════════
    with tab2:
        st.markdown("### ✏️ Saisir une transaction manuellement")
        st.markdown(
            "Entrez les caractéristiques d'une transaction "
            "pour obtenir une prédiction instantanée."
        )

        col1, col2 = st.columns(2)
        with col1:
            time_val   = st.number_input("⏱️ Time (secondes)",
                                          min_value=0.0, value=50000.0)
            amount_val = st.number_input("💰 Amount (€)",
                                          min_value=0.0, value=150.0,
                                          step=0.01)
        with col2:
            st.markdown("**Variables V1 - V28** *(composantes PCA)*")
            st.info(
                "💡 Ces variables sont anonymisées. "
                "Laissez à 0 pour une transaction type."
            )

        # Sliders V1-V28 en 4 colonnes
        v_values = {}
        important_vars = {
            'V17': -0.33, 'V14': -0.30, 'V12': -0.26,
            'V10': -0.22, 'V11': 0.15,  'V4':  0.13
        }

        st.markdown("**🔑 Variables les plus importantes :**")
        cols = st.columns(3)
        for i, (var, corr) in enumerate(important_vars.items()):
            with cols[i % 3]:
                v_values[var] = st.slider(
                    f"{var} (corr: {corr:+.2f})",
                    min_value=-30.0,
                    max_value=30.0,
                    value=0.0,
                    step=0.1
                )

        with st.expander("⚙️ Autres variables V1-V28"):
            all_vars = [f'V{i}' for i in range(1, 29)]
            remaining = [v for v in all_vars if v not in important_vars]
            cols2 = st.columns(4)
            for i, var in enumerate(remaining):
                with cols2[i % 4]:
                    v_values[var] = st.slider(
                        var,
                        min_value=-30.0,
                        max_value=30.0,
                        value=0.0,
                        step=0.1,
                        key=f"slider_{var}"
                    )

        # ── Bouton Prédire ────────────────────────────
        if st.button("🔍 Analyser cette transaction", type="primary"):
            # Préparation des données
            row = {'Time': time_val, 'Amount': amount_val}
            row.update(v_values)
            df_manual = pd.DataFrame([row])

            probs_m, preds_m = predict_transactions(
                df_manual.copy(), model, scaler, config
            )
            prob  = probs_m[0]
            pred  = preds_m[0]

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Résultat principal ────────────────────
            col_r1, col_r2 = st.columns([1, 2])

            with col_r1:
                if pred == 1:
                    st.markdown(f'''
                        <div class="card" style="border-left:4px solid #E63946;
                                                  text-align:center;">
                            <div style="font-size:60px;">🚨</div>
                            <div style="font-size:24px; font-weight:700;
                                        color:#E63946; margin:10px 0;">
                                FRAUDE DÉTECTÉE
                            </div>
                            <div style="font-size:14px; color:#6B7280;">
                                Probabilité : {prob*100:.2f}%
                            </div>
                            <div style="margin-top:12px;">
                                <span class="badge-fraud">🔴 Risque élevé</span>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                        <div class="card" style="border-left:4px solid #2DC653;
                                                  text-align:center;">
                            <div style="font-size:60px;">✅</div>
                            <div style="font-size:24px; font-weight:700;
                                        color:#2DC653; margin:10px 0;">
                                TRANSACTION NORMALE
                            </div>
                            <div style="font-size:14px; color:#6B7280;">
                                Probabilité de fraude : {prob*100:.2f}%
                            </div>
                            <div style="margin-top:12px;">
                                <span class="badge-normal">🟢 Risque faible</span>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

            with col_r2:
                st.plotly_chart(
                    gauge_chart(prob),
                    use_container_width=True
                )