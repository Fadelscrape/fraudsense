import os
import streamlit as st

def download_dataset():
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, '../../../data/creditcard.csv')

    if os.path.exists(data_path):
        return data_path

    st.info("⏳ Téléchargement du dataset complet depuis Kaggle (143MB)...")

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

        if os.path.exists(data_path):
            st.success("✅ Dataset complet téléchargé — 284,807 transactions !")
            return data_path
        else:
            st.error("❌ Fichier non trouvé après téléchargement")
            st.stop()

    except KeyError:
        st.error("❌ Credentials Kaggle manquants dans les secrets Streamlit")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
        st.stop()
