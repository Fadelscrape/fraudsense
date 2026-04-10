import os
import streamlit as st

def download_dataset():
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, '../../../data/creditcard.csv')

    if os.path.exists(data_path):
        return data_path

    st.warning("⏳ Dataset complet non trouvé — téléchargement depuis Kaggle...")

    try:
        os.environ['KAGGLE_USERNAME'] = st.secrets['kaggle']['username']
        os.environ['KAGGLE_KEY'] = st.secrets['kaggle']['key']

        import kaggle
        kaggle.api.authenticate()

        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        kaggle.api.dataset_download_files(
            'mlg-ulb/creditcardfraud',
            path=os.path.dirname(data_path),
            unzip=True
        )
        st.success("✅ Dataset téléchargé avec succès !")
        return data_path

    except Exception as e:
        st.info("ℹ️ Mode démonstration — utilisation de l'échantillon")
        sample_path = os.path.join(base, '../../../data/creditcard_sample.csv')
        if os.path.exists(sample_path):
            return sample_path
        st.error(f"❌ Aucun dataset disponible : {e}")
        st.stop()
