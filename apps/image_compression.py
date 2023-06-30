import cv2
import numpy as np
import streamlit as st
from PIL import Image

from .algorithms import adaptive_huffman
from .algorithms.utils.utils import get_raw_img


def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image


def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


def image_compression():
    st.title("Image Compression")

    st.markdown("**Upload up to 20 images**")
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png', 'raw'],
                                      key="image")

    compression_options = ['Adaptive Huffman', 'JPEG']
    compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

    if st.button("Compress"):
        if not uploaded_files:
            st.warning("Please upload at least one image.")
            return

        for uploaded_file in uploaded_files:
            # image = Image.open(uploaded_file)
            # image.save(image_path)
            image_path = f"temp_images/{uploaded_file.name}"

            if compression_algorithm == 'Adaptive Huffman':
                ah = adaptive_huffman
                alphabet_range = (0, 255)
                dpcm = False
                ah.compress(uploaded_file.name, 'compressed',
                            alphabet_range=alphabet_range, dpcm=dpcm)
                ah.extract('compressed', 'extracted.raw',
                           alphabet_range=alphabet_range, dpcm=dpcm)

                comparison = get_raw_img(uploaded_file.name, 'extracted.raw', size=(512, 512))

                st.image(comparison)

            elif compression_algorithm == 'LWZ':
                pass

            st.markdown("----")


def run():
    st.sidebar.title("Image Compression App")
    image_compression()
