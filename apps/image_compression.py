import os

import streamlit as st
from PIL import Image

from .algorithms import lzw


def get_file_size(file_path):
    return os.path.getsize(file_path)


def compress_images(uploaded_files, compression_algorithm):
    compressed_files = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image_path = f"Text-and-Image-Compressor-main/temp_images/{uploaded_file.name}"
        image.save(image_path)

        original_file_size = get_file_size(image_path)

        if compression_algorithm == 'Adaptive Huffman':
            pass

        elif compression_algorithm == 'LZW':
            compressed_file_path = f"Text-and-Image-Compressor-main/CompressedFiles/{uploaded_file.name.split('.')[0]}_LZWCompressed.txt"

            lzw.compress(image_path, compressed_file_path)
            compressed_file_size = get_file_size(compressed_file_path)

            compression_ratio = original_file_size / compressed_file_size
            compression_percent = (1 - (compressed_file_size / original_file_size)) * 100

            compressed_files.append((compressed_file_path, original_file_size, compressed_file_size, compression_ratio,
                                     compression_percent))

    return compressed_files


def decompress_images(compressed_files, decompression_algorithm):
    decompressed_images = []

    for compressed_file in compressed_files:
        file_name = compressed_file.name

        if decompression_algorithm == 'Adaptive Huffman':
            pass

        elif decompression_algorithm == 'LZW':
            compressed_file_path = f"CompressedFiles/{file_name}"
            decompressed_file_path = f"DecompressedFiles/{file_name.split('_LZWCompressed.txt')[0]}_LZWDecompressed.jpg"

            decompressed_image = lzw.decompress(compressed_file_path, decompressed_file_path)
            decompressed_images.append(decompressed_image)

    return decompressed_images


def image_compression():
    st.title("Image Compression")

    mode_options = ['Compress', 'Decompress']
    mode = st.selectbox("Select mode", mode_options)

    if mode == 'Compress':
        st.markdown("**Upload up to 20 images**")
        uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True,
                                          type=['jpg', 'jpeg', 'png'], key="image")

        compression_options = ['Adaptive Huffman', 'LZW', 'JPEG']
        compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

        if st.button("Compress"):
            if not uploaded_files:
                st.warning("Please upload at least one image.")
                return

            compressed_files = compress_images(uploaded_files, compression_algorithm)

            st.markdown("**Download compressed files:**")
            for compressed_file in compressed_files:
                st.markdown(f"**File Name:** {os.path.basename(compressed_file[0])}")
                st.markdown(f"**Original File Size:** {compressed_file[1]} bytes")
                st.markdown(f"**Compressed File Size:** {compressed_file[2]} bytes")
                st.markdown(f"**Compression Ratio:** {compressed_file[3]:.2f}")
                st.markdown(f"**Compression Percent:** {compressed_file[4]:.2f}%")

                st.download_button(
                    label="Download",
                    data=compressed_file[0],
                    file_name=os.path.basename(compressed_file[0])
                )
                st.markdown("---")

    elif mode == 'Decompress':
        st.markdown("**Upload compressed files**")
        compressed_files = st.file_uploader("Choose files", accept_multiple_files=True, type=['txt'],
                                            key="compressed_files")

        decompression_options = ['Adaptive Huffman', 'LZW', 'JPEG']
        decompression_algorithm = st.selectbox("Select decompression algorithm", decompression_options)

        if st.button("Decompress"):
            if not compressed_files:
                st.warning("Please upload at least one compressed file.")
                return

            decompressed_images = decompress_images(compressed_files, decompression_algorithm)

            st.markdown("----")
            st.success("Decompression completed!")
            st.markdown("**Original Images:**")
            for image in decompressed_images:
                st.image(image)


def run():
    st.sidebar.title("Image Compression App")
    image_compression()
