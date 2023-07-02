import cv2
import numpy as np
import streamlit as st
from PIL import Image
import os
from .algorithms import adaptive_huffman, lzw, lz77
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

    compression_options = ['Adaptive Huffman', 'LZW', 'LZ77','JPEG']
    compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

    if compression_algorithm == 'LZ77':
        searchWindow = st.slider("Enter the search window sze:", min_value=1,  step=1)
        previewWindow = st.slider("Enter the preview window ize:", min_value=1,  step=1)

    if st.button("Compress"):
        if not uploaded_files:
            st.warning("Please upload at least one image.")
            return

        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_path = f"temp_images/{uploaded_file.name}"
            image.save(image_path)
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

            elif compression_algorithm == 'LZW':
                compressor = lzw.LZW_IMG(image_path)
                compressor.compress()
                before = compressor.original_file_size
                after = compressor.compressed_file_size

                decompressor = lzw.LZW_IMG(os.path.join("CompressedFiles",uploaded_file.name.split('.')[0] + "_LZWcompressed.txt"))
                decompressor.decompress()

            elif compression_algorithm == 'LZ77':
                compressor = lz77.LZ77(image_path, searchWindowSize=searchWindow, previewWindowSize=previewWindow)
                compressor.compress()
                # before = compressor.original_file_size
                # after = compressor.compressed_file_size

                decompressor = lz77.LZ77(os.path.join("CompressedFiles",uploaded_file.name.split('.')[0] + "_LZ77compressed.txt"))
                decompressor.decompress()

            st.markdown("----")


def run():
    st.sidebar.title("Image Compression App")
    image_compression()
