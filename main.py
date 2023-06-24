import streamlit as st

from apps import text_compression, image_compression

apps = {
    'Text Compression': text_compression,
    'Image Compression': image_compression
}

selected_app = st.sidebar.radio('Select App', list(apps.keys()))

apps[selected_app].run()
