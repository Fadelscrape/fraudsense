# ============================================================
# FRAUDSENSE — Page Explicabilité
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
import json
import shap
import os
from utils.variables import VARIABLES_DICT, VARIABLES_NOTE, get_label, rename_features

# ── Chargement modèle + données ───────────────────────────
@st.cache_resource
def load_model():
    base = os.path.join(os.path.dirname(__file__), '../../model')
    model  = joblib.load(os.path.join(base, 'fraud_model.pkl'))
    scaler = joblib.load(os.path.join(base, 'scaler.pkl'))
    with open(os.path.join(base, 'config.json')) as f:
        config = json.load(f)
    return model, scaler, config

@st.cache_data(ttl=3600, show_spinner=False)
def compute_metrics(_model, _scaler, config):
    from utils.data_loader import download_dataset
    data_path, source = download_dataset()
    df = pd.read_csv(data_path)

    from sklearn.metrics import (roc_curve, precision_recall_curve,
                                 roc_auc_score, average_precision_score,
                                 confusion_matrix)

    features = config['features']
    df['Amount_scaled'] = df['Amount'].apply(
        lambda x: (x - 88.29) / 250.11
    )
    df['Time_scaled'] = df['Time'].apply(
        lambda x: (x - 94813) / 47488
    )

    available = [f for f in features if f in df.columns]
    X = df[available]
    y = df['Class']

    # Utiliser uniquement le test set (20%)
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    y_prob = _model.predict_proba(X_test)[:, 1]
    y_pred = _model.predict(X_test)

    fpr, tpr, _  = roc_curve(y_test, y_prob)
    prec, rec, _ = precision_recall_curve(y_test, y_prob)
    auc          = roc_auc_score(y_test, y_prob)
    auprc        = average_precision_score(y_test, y_prob)
    cm           = confusion_matrix(y_test, y_pred)

    # Renommer les features avec noms lisibles
    feature_names = [get_label(f) for f in X_test.columns]
    return fpr, tpr, prec, rec, auc, auprc, cm, feature_names

@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    from utils.data_loader import download_dataset
    data_path, source = download_dataset()
    df = pd.read_csv(data_path)
    df['Hour'] = (df['Time'] / 3600) % 24
    return df, source

@st.cache_data(show_spinner=False)
def compute_shap(_model, X_sample):
    explainer   = shap.TreeExplainer(_model)
    shap_values = explainer.shap_values(X_sample)
    X_sample = rename_features(X_sample)
    return shap_values, explainer, X_sample

def prepare_features(df, scaler, config):
    features = config['features']
    df = df.copy()
    df['Amount_scaled'] = df['Amount'].apply(
        lambda x: (x - 88.29) / 250.11
    )
    df['Time_scaled'] = df['Time'].apply(
        lambda x: (x - 94813) / 47488
    )
    available = [f for f in features if f in df.columns]
    return df[available]

def show():
    model, scaler, config = load_model()
    df, source = load_data()

    # ── Header ────────────────────────────────────────────
    st.markdown('''
        <div class="page-header">
            <h1> Explicabilité du modèle</h1>
            <p>Comprendre les décisions du modèle XGBoost Optuna · 
               SHAP Values · Performance détaillée</p>
        </div>
    ''', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        " Performance du modèle",
        " Importance des variables (SHAP)",
        " Analyse par transaction",
        " Dictionnaire des variables"
    ])

    # ════════════════════════════════════════════════════
    # TAB 1 — Performance
    # ════════════════════════════════════════════════════
    with tab1:

        with st.spinner("⏳ Calcul des métriques..."):
            fpr, tpr, prec, rec, auc, auprc, cm, feature_names = compute_metrics(
                model, scaler, config
            )

        precision_val = cm[1, 1] / (cm[1, 1] + cm[0, 1]) if (cm[1, 1] + cm[0, 1]) > 0 else 0
        recall_val    = cm[1, 1] / (cm[1, 1] + cm[1, 0]) if (cm[1, 1] + cm[1, 0]) > 0 else 0
        tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]

        # KPIs performance
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("🎯 AUPRC", f"{auprc:.4f}", "#1B3A6B",
             "Métrique principale recommandée"),
            ("📈 ROC-AUC", f"{auc:.4f}", "#2DC653",
             "Discrimination globale"),
            ("🎖️ Précision", f"{precision_val:.2f}", "#F4A261",
             "Fraudes sur alertes totales"),
            ("🔔 Rappel", f"{recall_val:.2f}", "#E63946",
             "Fraudes détectées sur total"),
        ]
        for col, (label, val, color, desc) in zip([c1,c2,c3,c4], metrics):
            with col:
                st.markdown(f'''
                    <div class="kpi-card" style="border-left-color:{color};">
                        <div style="font-size:24px;">{label.split()[0]}</div>
                        <div class="kpi-value" style="color:{color};">
                            {val}
                        </div>
                        <div class="kpi-label">{label.split(' ',1)[1]}</div>
                        <div style="font-size:11px; color:#9CA3AF; 
                                    margin-top:4px;">{desc}</div>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Comment lire ces métriques :</strong><br><br>
    Ces quatre métriques permettent d'évaluer la performance
    du modèle sous différents angles, comme des notes
    dans plusieurs matières.<br><br>
     <strong>AUPRC = {auprc:.4f}</strong> (métrique principale)<br>
    Cette métrique est particulièrement adaptée aux problèmes
    déséquilibrés, comme ici où les fraudes sont très rares
    (0,173%). Un score de {auprc:.2f} indique que le modèle
    parvient à détecter efficacement les fraudes tout en
    limitant les fausses alertes, ce qui est crucial
    en pratique.<br><br>
     <strong>ROC-AUC = {auc:.4f}</strong><br>
    Ce score mesure la capacité du modèle à distinguer
    les fraudes des transactions normales. Une valeur
    proche de 1 indique que le modèle attribue généralement
    un score plus élevé aux fraudes qu'aux transactions
    normales.<br><br>
     <strong>Précision = {tp/(tp+fp):.2f}</strong><br>
    Parmi les alertes générées par le modèle,
    {tp/(tp+fp)*100:.0f}% correspondent réellement à des
    fraudes, ce qui limite le nombre de fausses alertes.<br><br>
     <strong>Rappel = {tp/(tp+fn):.2f}</strong><br>
    Sur l'ensemble des fraudes présentes dans les données
    de test, le modèle en détecte {tp/(tp+fn)*100:.0f}%,
    ce qui reflète sa capacité à ne pas laisser passer
    les transactions frauduleuses.
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'XGBoost Optuna (AUC={auc:.4f})',
                line=dict(color='#1B3A6B', width=3),
                fill='tozeroy',
                fillcolor='rgba(27,58,107,0.1)'
            ))
            fig_roc.add_trace(go.Scatter(
                x=[0,1], y=[0,1],
                mode='lines',
                name='Aléatoire (AUC=0.50)',
                line=dict(color='gray', width=1, dash='dash')
            ))
            fig_roc.add_annotation(
                x=0.6, y=0.3,
                text=f"<b>AUC = {auc:.4f}</b>",
                showarrow=False,
                font=dict(size=16, color='#1B3A6B'),
                bgcolor='rgba(27,58,107,0.1)',
                bordercolor='#1B3A6B',
                borderwidth=1,
                borderpad=8
            )
            fig_roc.update_layout(
                title=dict(text="Courbe ROC",
                          font=dict(size=16, color='#1B3A6B')),
                xaxis=dict(title='Taux Faux Positifs'),
                yaxis=dict(title='Taux Vrais Positifs'),
                height=380,
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(x=0.4, y=0.1)
            )
            st.plotly_chart(fig_roc, use_container_width=True)

        with col2:
            fig_pr = go.Figure()
            fig_pr.add_trace(go.Scatter(
                x=rec, y=prec,
                mode='lines',
                name=f'XGBoost Optuna (AUPRC={auprc:.4f})',
                line=dict(color='#E63946', width=3),
                fill='tozeroy',
                fillcolor='rgba(230,57,70,0.1)'
            ))
            fig_pr.add_hline(
                y=0.00172,
                line=dict(color='gray', dash='dash', width=1),
                annotation_text="Baseline (0.172%)",
                annotation_position="right"
            )
            fig_pr.add_annotation(
                x=0.4, y=0.5,
                text=f"<b>AUPRC = {auprc:.4f}</b>",
                showarrow=False,
                font=dict(size=16, color='#E63946'),
                bgcolor='rgba(230,57,70,0.1)',
                bordercolor='#E63946',
                borderwidth=1,
                borderpad=8
            )
            fig_pr.update_layout(
                title=dict(text="Courbe Précision-Rappel",
                          font=dict(size=16, color='#1B3A6B')),
                xaxis=dict(title='Rappel'),
                yaxis=dict(title='Précision', range=[0, 1.05]),
                height=380,
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(x=0.3, y=0.1)
            )
            st.plotly_chart(fig_pr, use_container_width=True)

        col_interp1, col_interp2 = st.columns(2)

        with col_interp1:
            st.markdown("""
    <div style='background:#FEF3C7; border-radius:12px;
                padding:14px 20px; margin:8px 0;
                border-left:4px solid #F59E0B;'>
        💡 <strong>Comment lire la Courbe ROC :</strong><br><br>
        Cette courbe mesure la capacité du modèle à distinguer
        les fraudes des transactions normales. Plus la courbe
        est proche du coin supérieur gauche, meilleur est
        le modèle.<br><br>
        Notre score <strong>AUC = 0.9829</strong> signifie
        que si on prend une fraude et une transaction normale
        au hasard, le modèle identifie correctement laquelle
        est la fraude dans <strong>98% des cas</strong>.<br><br>
        La ligne pointillée représente un modèle aléatoire
        (pile ou face) — notre modèle est bien au-dessus.
    </div>
    """, unsafe_allow_html=True)

        with col_interp2:
            st.markdown("""
    <div style='background:#FEF3C7; border-radius:12px;
                padding:14px 20px; margin:8px 0;
                border-left:4px solid #F59E0B;'>
        💡 <strong>Comment lire la Courbe Précision-Rappel :</strong><br><br>
        C'est la métrique principale recommandée pour ce
        dataset car les fraudes sont très rares (0.173%).<br><br>
        Notre score <strong>AUPRC = 0.8861</strong> signifie
        que le modèle est capable de distinguer une transaction
        frauduleuse d'une transaction normale dans 88.61%
        des cas possibles.<br><br>
        Pour mettre ce chiffre en perspective : un système
        qui signalerait toutes les transactions comme suspectes
        n'aurait qu'une précision de 0.173%. Notre modèle est
        donc bien plus efficace, ce qui confirme qu'il a
        réellement appris à reconnaître les patterns de fraude.
    </div>
    """, unsafe_allow_html=True)

        # Matrice de confusion
        st.markdown("### Matrice de confusion — XGBoost Optuna")

        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            cm_data = cm.tolist()
            fig_cm = go.Figure(go.Heatmap(
                z=cm_data,
                x=['Prédit Normal', 'Prédit Fraude'],
                y=['Réel Normal', 'Réel Fraude'],
                colorscale=[[0,'#EFF6FF'],[0.5,'#3B82F6'],[1,'#1B3A6B']],
                showscale=False,
                text=[[f'{v:,}' for v in row] for row in cm_data],
                texttemplate='<b>%{text}</b>',
                textfont=dict(size=20)
            ))
            fig_cm.update_layout(
                height=280,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_cm, use_container_width=True)

        with col_m2:
            st.markdown("<br>", unsafe_allow_html=True)
            tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
            metrics_cm = [
                ("✅ Vrais Négatifs (TN)", f"{tn:,}",
                 "Transactions normales correctement classées", "#2DC653"),
                ("⚠️ Faux Positifs (FP)", f"{fp:,}",
                 "Transactions normales classées comme fraudes", "#F4A261"),
                ("❌ Faux Négatifs (FN)", f"{fn:,}",
                 "Fraudes non détectées — risque réel", "#E63946"),
                ("🎯 Vrais Positifs (TP)", f"{tp:,}",
                 "Fraudes correctement détectées", "#1B3A6B"),
            ]
            for label, val, desc, color in metrics_cm:
                st.markdown(f'''
                    <div style="display:flex; align-items:center; 
                                padding:10px; margin:6px 0;
                                background:#F8F9FC; border-radius:10px;
                                border-left:3px solid {color};">
                        <div style="min-width:50px; font-size:20px; 
                                    font-weight:700; color:{color};">
                            {val}
                        </div>
                        <div style="margin-left:12px;">
                            <div style="font-weight:600; font-size:13px;">
                                {label}
                            </div>
                            <div style="font-size:11px; color:#6B7280;">
                                {desc}
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown(f"""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Comment lire la matrice de confusion :</strong><br><br>
    Sur <strong>{tp+fn} fraudes réelles</strong> dans les données
    de test, le modèle en a détecté
    <strong>{tp} correctement</strong>.<br><br>
    Il a manqué <strong>{fn} fraudes</strong> (faux négatifs) —
    ces transactions ont été classées comme normales alors
    qu'elles étaient frauduleuses.<br><br>
    Il a également généré <strong>{fp} fausses alertes</strong>
    (faux positifs), des transactions normales signalées
    comme suspectes.<br><br>
    En contexte bancaire, manquer une fraude signifie qu'un
    client est débité pour un achat qu'il n'a pas effectué,
    ce qui est bien plus grave qu'un simple blocage temporaire
    de carte dû à une fausse alerte.
</div>
""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # TAB 2 — SHAP Global
    # ════════════════════════════════════════════════════
    with tab2:
        st.markdown("### Importance globale des variables (SHAP)")
        st.info(
            "💡 Les valeurs SHAP mesurent la contribution de chaque "
            "variable à la prédiction. Plus la valeur est élevée, "
            "plus la variable est importante."
        )

        # Calcul SHAP sur échantillon
        with st.spinner("⏳ Calcul des valeurs SHAP en cours..."):
            sample = df.sample(1000, random_state=42)
            X_sample = prepare_features(sample, scaler, config)
            shap_values, explainer, X_sample = compute_shap(model, X_sample)

        # Importance moyenne SHAP
        shap_vals = shap_values[1] if isinstance(shap_values, list) else shap_values
        mean_shap = pd.DataFrame({
            'Variable': X_sample.columns,
            'SHAP': np.abs(shap_vals).mean(axis=0)
        }).sort_values('SHAP', ascending=True).tail(15)

        fig_shap = go.Figure(go.Bar(
            x=mean_shap['SHAP'],
            y=mean_shap['Variable'],
            orientation='h',
            marker=dict(
                color=mean_shap['SHAP'],
                colorscale=[[0,'#E8EFF8'],[0.5,'#2E5BA8'],[1,'#1B3A6B']],
                showscale=False
            ),
            hovertemplate='%{y} : %{x:.4f}<extra></extra>'
        ))
        fig_shap.update_layout(
            title=dict(
                text="Importance moyenne des variables (|SHAP|)",
                font=dict(size=16, color='#1B3A6B')
            ),
            height=500,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Valeur SHAP moyenne')
        )
        st.plotly_chart(fig_shap, use_container_width=True)

        st.markdown("""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Comment lire ce graphique :</strong>
    Ce graphique montre quelles variables ont le plus
    influencé les décisions du modèle. Plus la barre
    est longue, plus cette variable est déterminante
    pour détecter les fraudes.<br><br>
    La <strong>"Distance inhabituelle entre terminaux"</strong>
    et le <strong>"Type et catégorie du marchand"</strong>
    sont les deux variables les plus importantes selon
    l'analyse SHAP sur cet échantillon. Ces résultats
    peuvent légèrement varier selon l'échantillon analysé,
    mais confirment que le comportement du terminal et
    du marchand sont des signaux clés de fraude.
</div>
""", unsafe_allow_html=True)

        # SHAP Scatter — impact + valeur
        st.markdown("### Impact des variables sur les prédictions")

        top_features = mean_shap.tail(8)['Variable'].tolist()
        selected_feat = st.selectbox(
            "Choisir une variable à analyser :",
            options=top_features[::-1]
        )

        feat_idx = list(X_sample.columns).index(selected_feat)
        fig_scatter = go.Figure(go.Scatter(
            x=X_sample[selected_feat].values,
            y=shap_values[:, feat_idx],
            mode='markers',
            marker=dict(
                color=shap_values[:, feat_idx],
                colorscale=[[0,'#2DC653'],[0.5,'#F4A261'],[1,'#E63946']],
                size=6,
                opacity=0.7,
                showscale=True,
                colorbar=dict(title='Valeur SHAP', thickness=15)
            ),
            hovertemplate=(
                f'{selected_feat} : %{{x:.3f}}<br>'
                f'Valeur SHAP : %{{y:.4f}}<extra></extra>'
            )
        ))
        fig_scatter.add_hline(
            y=0,
            line=dict(color='gray', dash='dash', width=1)
        )
        fig_scatter.update_layout(
            title=dict(
                text=f"Valeur de {selected_feat} vs impact SHAP",
                font=dict(size=16, color='#1B3A6B')
            ),
            xaxis=dict(title=f'Valeur de {selected_feat}'),
            yaxis=dict(title='Valeur SHAP'),
            height=400,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("""
<div style='background:#FEF3C7; border-radius:12px;
            padding:14px 20px; margin:16px 0;
            border-left:4px solid #F59E0B;'>
    💡 <strong>Comment lire ce graphique :</strong>
    Chaque point représente une transaction analysée.
    L'axe horizontal montre la valeur réelle de la variable
    pour cette transaction.<br><br>
    Les points <strong style='color:#E63946;'>rouges
    (au-dessus de 0)</strong> indiquent que cette variable
    pousse le modèle vers une décision
    <strong>"Fraude"</strong> pour cette transaction.<br>
    Les points <strong style='color:#2DC653;'>verts
    (en-dessous de 0)</strong> indiquent que cette variable
    pousse le modèle vers une décision
    <strong>"Normal"</strong>.<br><br>
    Par exemple, pour la "Distance inhabituelle entre
    terminaux" : quand la valeur est très négative
    (à gauche), le modèle détecte une anomalie et
    penche vers "Fraude" (points rouges en haut).
</div>
""", unsafe_allow_html=True)

        from utils.variables import VARIABLES_NOTE as VN
        st.caption(VN)

    # ════════════════════════════════════════════════════
    # TAB 3 — Analyse par transaction
    # ════════════════════════════════════════════════════
    with tab3:
        st.markdown("### Expliquer une transaction spécifique")
        st.markdown(
            "Sélectionnez une transaction du dataset "
            "pour voir pourquoi le modèle l'a classée ainsi."
        )

        classe = st.session_state.get('classe_select', 'Fraude (Classe=1)')
        classe_val = 1 if 'Fraude' in classe else 0
        subset = df[df['Class'] == classe_val].reset_index(drop=True)

        # Slider adapté au nombre réel de transactions disponibles
        max_idx = min(499, len(subset)-1) if classe_val == 1 else min(999, len(subset)-1)

        col1, col2 = st.columns(2)
        with col1:
            classe = st.selectbox(
                "Type de transaction",
                ['Fraude (Classe=1)', 'Normale (Classe=0)'],
                key='classe_select'
            )
        with col2:
            st.caption(f"📊 {len(subset):,} transactions disponibles")
            idx = st.slider(
                "Index de la transaction",
                0, max_idx, 0,
                help=f"Choisir parmi {len(subset):,} transactions"
            )

        row = subset.iloc[[idx]]
        X_row = prepare_features(row, scaler, config)
        X_row_display = rename_features(X_row)

        # Calcul SHAP direct sans cache pour cette transaction
        explainer_local = shap.TreeExplainer(model)
        shap_row = explainer_local.shap_values(X_row)[0]

        prob_row = model.predict_proba(X_row)[0][1]
        pred_row = int(prob_row >= 0.5)

        # Résultat
        color_r = '#E63946' if pred_row == 1 else '#2DC653'
        label_r = '🚨 FRAUDE' if pred_row == 1 else '✅ NORMAL'
        st.markdown(f'''
            <div style="background:{'#FEE2E2' if pred_row==1 else '#D1FAE5'};
                        border-radius:12px; padding:16px; margin:16px 0;
                        border-left:4px solid {color_r};
                        display:flex; align-items:center;
                        justify-content:space-between;">
                <div style="font-size:20px; font-weight:700; color:{color_r};">
                    {label_r}
                </div>
                <div style="font-size:24px; font-weight:700; color:{color_r};">
                    {prob_row*100:.2f}% de probabilité de fraude
                </div>
            </div>
        ''', unsafe_allow_html=True)

        # Waterfall SHAP
        shap_series = pd.Series(shap_row, index=X_row_display.columns)
        shap_df = shap_series.abs().sort_values().tail(12)
        shap_vals = shap_series[shap_df.index]

        colors_bar = ['#E63946' if v > 0 else '#2DC653'
                      for v in shap_vals.values]

        fig_wf = go.Figure(go.Bar(
            x=shap_vals.values,
            y=shap_vals.index,
            orientation='h',
            marker_color=colors_bar,
            text=[f'{v:+.4f}' for v in shap_vals.values],
            textposition='outside',
            hovertemplate='%{y} : %{x:.4f}<extra></extra>'
        ))
        fig_wf.add_vline(x=0, line=dict(color='black', width=1.5))
        fig_wf.update_layout(
            title=dict(
                text=f"Contribution SHAP — Transaction #{idx} | "
                     f"Prob fraude: {prob_row*100:.2f}%",
                font=dict(size=14, color='#1B3A6B')
            ),
            height=500,
            margin=dict(t=60, b=20, l=150, r=80),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='Contribution SHAP',
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5
            ),
            yaxis=dict(title=''),
            showlegend=False
        )
        st.plotly_chart(fig_wf, use_container_width=True)

        # Détail des valeurs de la transaction
        with st.expander(" Voir les valeurs de la transaction"):
            st.dataframe(X_row_display.T.rename(columns={X_row_display.index[0]: 'Valeur'}),
                        use_container_width=True)

    # ════════════════════════════════════════════════════
    # TAB 4 — Dictionnaire des variables
    # ════════════════════════════════════════════════════
    with tab4:
        from utils.variables import (VARIABLES_DICT, VARIABLES_NOTE,
                                      VARIABLES_DESCRIPTIONS, TOP_VARIABLES)

        st.markdown("### Dictionnaire des variables")
        st.markdown("""
    Ce tableau présente toutes les variables utilisées
    par le modèle, avec leur signification et leur
    impact sur la détection de fraude.
    """)

        st.info(VARIABLES_NOTE)

        st.markdown("### Variables les plus importantes")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🔴 Signaux forts de FRAUDE**")
            for var in ['V17', 'V14', 'V12', 'V10', 'V16', 'V3', 'V7']:
                if var in VARIABLES_DESCRIPTIONS:
                    d = VARIABLES_DESCRIPTIONS[var]
                    st.markdown(f"""
                <div style='background:#FEE2E2; padding:12px;
                            border-radius:8px; margin:6px 0;
                            border-left:4px solid #E63946;'>
                    <strong>{var} — {d["nom"]}</strong><br>
                    <small style='color:#6B7280;'>{d["explication"]}</small><br>
                    <small style='color:#E63946;'>💡 {d["exemple"]}</small>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("**🟢 Signaux de transaction NORMALE**")
            for var in ['V11', 'V4', 'V2']:
                if var in VARIABLES_DESCRIPTIONS:
                    d = VARIABLES_DESCRIPTIONS[var]
                    st.markdown(f"""
                <div style='background:#D1FAE5; padding:12px;
                            border-radius:8px; margin:6px 0;
                            border-left:4px solid #2DC653;'>
                    <strong>{var} — {d["nom"]}</strong><br>
                    <small style='color:#6B7280;'>{d["explication"]}</small><br>
                    <small style='color:#065F46;'>💡 {d["exemple"]}</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("**⚪ Variables descriptives**")
        for var in ['Amount', 'Time']:
            if var in VARIABLES_DESCRIPTIONS:
                d = VARIABLES_DESCRIPTIONS[var]
                st.markdown(f"""
        <div style='background:#F3F4F6; padding:12px;
                    border-radius:8px; margin:6px 0;
                    border-left:4px solid #6B7280;'>
            <strong>{var} — {d["nom"]}</strong><br>
            <small style='color:#6B7280;'>{d["explication"]}</small><br>
            <small style='color:#374151;'>💡 {d["exemple"]}</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Tableau complet des variables")

        rows = []
        for var, label in VARIABLES_DICT.items():
            if var in ['Amount_scaled', 'Time_scaled']:
                continue
            desc = VARIABLES_DESCRIPTIONS.get(var, {})
            corr = desc.get('correlation', 0.0)
            if corr < -0.15:
                signal = '🔴 Fort signal fraude'
            elif corr < -0.05:
                signal = '🟡 Signal fraude modéré'
            elif corr > 0.05:
                signal = '🟢 Signal normalité'
            else:
                signal = '⚪ Neutre'
            rows.append({
                'Variable': var,
                'Signification': label,
                'Signal': signal,
                'Corrélation': round(corr, 3),
                'Exemple concret': desc.get('exemple', 'N/A')
            })

        df_dict = pd.DataFrame(rows)
        df_dict = df_dict.sort_values('Corrélation')

        st.dataframe(
            df_dict,
            use_container_width=True,
            hide_index=True,
            height=600
        )

    # ── Footer ────────────────────────────────────────────
    st.markdown('''
        <div style="text-align:center; padding:20px; 
                    color:#6B7280; font-size:12px; margin-top:20px;">
            FraudSense · XGBoost Optuna · 
            Explicabilité par SHAP (SHapley Additive exPlanations)
        </div>
    ''', unsafe_allow_html=True)