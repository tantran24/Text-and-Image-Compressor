import os

import streamlit as st
from PIL import Image

from .algorithms import adaptive_huffman, lzw, lz77


def get_file_size(file_path):
    return os.path.getsize(file_path)


def compress_images(uploaded_files, compression_algorithm, searchWindow=6, previewWindow=6):
    compressed_files = []


    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image_path = f"temp_images/{uploaded_file.name}"
        image.save(image_path)

        # original_file_size = get_file_size(image_path)
        original_file_size = 1
        if compression_algorithm == 'Adaptive Huffman':
            compressor = adaptive_huffman.AdaptiveHuffman_IMG(image_path)
            compressed_file = f"CompressedFiles/{os.path.splitext(uploaded_file.name)[0]}.txt"
            compressor.compress()
            os.makedirs(os.path.dirname(compressed_file), exist_ok=True)
            os.rename(
                os.path.join(os.getcwd(), "CompressedFiles", f"{os.path.splitext(uploaded_file.name)[0]}_AdaptiveHuffmanCompressed.txt"),
                compressed_file)
            compressed_file = f"CompressedFiles/{os.path.splitext(uploaded_file.name)[0]}_AdaptiveHuffmanCompressed.txt"

        elif compression_algorithm == 'LZW':
            compressor = lzw.LZW_IMG(image_path)
            compressed_file = compressor.compress()

        elif compression_algorithm == 'LZ77':
            compressor = lz77.LZ77(path = image_path, searchWindowSize=searchWindow, previewWindowSize=previewWindow)
            compressed_file = compressor.compress()
        
        # compressed_file_size = get_file_size(compressed_file)
        compressed_file_size=1
        compression_ratio = original_file_size / compressed_file_size
        compression_percent = (1 - compressed_file_size / original_file_size) * 100

        compressed_files.append((compressed_file, original_file_size, compressed_file_size, compression_ratio,
                                    compression_percent))
    return compressed_files


def decompress_images(compressed_files, decompression_algorithm):
    decompressed_images = []
    
    for compressed_file in compressed_files:
        file_name = compressed_file.name

        if decompression_algorithm == 'Adaptive Huffman':
            pass
        elif decompression_algorithm == 'LZW':
            decompressor = lzw.LZW_IMG(compressed_file)
            decompressed_image = decompressor.decompress()
        elif decompression_algorithm == 'LZ77':
            decompressor = lz77.LZ77(file=compressed_file)
            decompressed_image = decompressor.decompress()

        decompressed_images.append(decompressed_image)

    return decompressed_images


def image_compression():
    st.title("Image Compression")

    mode_options = ['Compress', 'Decompress']
    mode = st.selectbox("Select mode", mode_options)

    

    if mode == 'Compress':
        st.markdown("**Upload up to 20 images**")
        uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True,
                                          type=['bmp'], key="image")

        compression_options = ['Adaptive Huffman', 'LZW', 'LZ77', 'JPEG']
        compression_algorithm = st.selectbox("Select compression algorithm", compression_options)
        if compression_algorithm == 'LZ77':
            searchWindow = st.slider("Enter the search window size:", min_value=1,  step=1)
            previewWindow = st.slider("Enter the preview window size:", min_value=1,  step=1)

        if st.button("Compress"):
            if not uploaded_files:
                st.warning("Please upload at least one image.")
                return
            if compression_algorithm == 'LZ77':
                compressed_files = compress_images(uploaded_files, compression_algorithm, searchWindow, previewWindow)

            compressed_files = compress_images(uploaded_files, compression_algorithm)
            st.markdown("**Download compressed files:**")
            for compressed_file in compressed_files:
                # st.markdown(f"**File Name:** {compressed_file.name}")
                st.markdown(f"**Original File Size:** {compressed_file[1]} bytes")
                st.markdown(f"**Compressed File Size:** {compressed_file[2]} bytes")
                st.markdown(f"**Compression Ratio:** {compressed_file[3]:.2f}")
                st.markdown(f"**Compression Percent:** {compressed_file[4]:.2f}%")

                st.download_button(
                    label="Download",
                    data=compressed_file[0],
                    file_name="1"
                )
                st.markdown("---")

    elif mode == 'Decompress':
        st.markdown("**Upload compressed files**")
        compressed_files = st.file_uploader("Choose files", accept_multiple_files=True, type=['txt'],
                                            key="compressed_files")

        decompression_options = ['Adaptive Huffman', 'LZW', 'LZ77', 'JPEG']
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
