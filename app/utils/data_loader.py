import os
import streamlit as st

def download_dataset():
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, '../../../data/creditcard.csv')

    if os.path.exists(data_path):
        return data_path, "local"

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
            return data_path, "kaggle"
        else:
            st.stop()

    except KeyError:
        st.stop()
    except Exception:
        st.stop()
