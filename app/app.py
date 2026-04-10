# ============================================================
# FRAUDSENSE — Application principale
# ============================================================
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import base64
import os
import gc
gc.enable()

# Configuration performance
st.set_option('client.showErrorDetails', False)
st.set_option('client.toolbarMode', 'minimal')

# ── Configuration de la page ──────────────────────────────
st.set_page_config(
    page_title="FraudSense — Détection de Fraude",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
        ## FraudSense 🛡️
        **Application de détection de fraude bancaire**

        - Modèle : XGBoost Optuna
        - AUPRC : 0.8861
        - ROC-AUC : 0.9828
        - Dataset : Credit Card Fraud Detection (Kaggle)

        Développé avec Python, Streamlit & SHAP
        """
    }
)

# ── Chargement du CSS ─────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# ── Chargement du logo ────────────────────────────────────
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
    with open(logo_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    # Logo + Titre
    try:
        logo_b64 = get_logo_base64()
        st.markdown(f'''
            <div style="text-align:center; padding: 20px 0 10px;">
                <img src="data:image/png;base64,{logo_b64}" 
                     width="80" style="border-radius:12px; margin-bottom:12px;">
                <div class="sidebar-title">FraudSense</div>
                <div class="sidebar-subtitle">Fraud Detection AI</div>
            </div>
        ''', unsafe_allow_html=True)
    except:
        st.markdown('''
            <div style="text-align:center; padding: 20px 0 10px;">
                <div style="font-size:48px;">🛡️</div>
                <div class="sidebar-title">FraudSense</div>
                <div class="sidebar-subtitle">Fraud Detection AI</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Menu navigation
    selected = option_menu(
        menu_title=None,
        options=["Tableau de bord", "Prédiction", "Explicabilité"],
        icons=["bar-chart-fill", "search", "cpu"],
        default_index=0,
        styles={
            "menu-title": {"color": "transparent", "font-size": "0px"},
            "container": {
                "padding": "4px",
                "background-color": "#1B3A6B",
                "border-radius": "12px",
                "border": "none"
            },
            "icon": {
                "color": "rgba(255,255,255,0.85)",
                "font-size": "16px"
            },
            "nav-link": {
                "font-size": "14px",
                "color": "rgba(255,255,255,0.85)",
                "border-radius": "8px",
                "margin": "2px 0",
                "padding": "10px 16px",
                "background-color": "transparent"
            },
            "nav-link-selected": {
                "background-color": "rgba(255,255,255,0.2)",
                "color": "white",
                "font-weight": "600"
            },
        }
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Infos modèle dans sidebar
    st.markdown('''
        <div style="padding: 16px; background: rgba(255,255,255,0.08); 
                    border-radius: 12px; margin-top: 10px;">
            <div style="font-size:11px; color:rgba(255,255,255,0.5); 
                        text-transform:uppercase; letter-spacing:1px;">
                Modèle actif
            </div>
            <div style="font-size:14px; font-weight:600; margin-top:6px;">
                XGBoost Optuna
            </div>
            <div style="font-size:12px; color:rgba(255,255,255,0.6); margin-top:4px;">
                AUPRC : 0.8861 &nbsp;|&nbsp; AUC : 0.9829
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
        <div style="position:fixed; bottom:20px; left:0; right:0; 
                    text-align:center; font-size:11px; 
                    color:rgba(255,255,255,0.3);">
            FraudSense v1.0 © 2026
        </div>
    ''', unsafe_allow_html=True)

# ── Routing des pages ─────────────────────────────────────
if selected == "Tableau de bord":
    from views.dashboard import show
    show()
elif selected == "Prédiction":
    from views.prediction import show
    show()
elif selected == "Explicabilité":
    from views.explicabilite import show
    show()