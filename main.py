import os

import streamlit as st

from apps import text_compression, image_compression

folders = ['CompressedFiles', 'DecompressedFiles', 'temp_images']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

apps = {
    'Text Compression': text_compression,
    'Image Compression': image_compression
}

selected_app = st.sidebar.radio('Select App', list(apps.keys()))

apps[selected_app].run()
