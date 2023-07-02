import os
import streamlit as st
from PIL import Image

from .algorithms import adaptive_huffman, lzw

def compress_images(uploaded_files, compression_algorithm):
    compressed_files = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image_path = f"temp_images/{uploaded_file.name}"
        image.save(image_path)

        if compression_algorithm == 'Adaptive Huffman':
            compressor = adaptive_huffman.AdaptiveHuffman_IMG(image_path)
            compressor.compress()
            compressed_file_path = f"CompressedFiles/{uploaded_file.name.split('.')[0]}_AdaptiveHuffmanCompressed.txt"
            compressed_files.append(compressed_file_path)

        elif compression_algorithm == 'LZW':
            compressor = lzw.LZW_IMG(image_path)
            compressor.compress()
            compressed_file_path = f"CompressedFiles/{uploaded_file.name.split('.')[0]}_LZWCompressed.txt"
            compressed_files.append(compressed_file_path)

    return compressed_files


def decompress_images(compressed_files, decompression_algorithm):
    decompressed_images = []

    for compressed_file in compressed_files:
        decompressed_file_path = ""

        if decompression_algorithm == 'Adaptive Huffman':
            decompressed_file_path = f"DecompressedFiles/{os.path.basename(compressed_file).split('_AdaptiveHuffmanCompressed.txt')[0]}_AdaptiveHuffmanDecompressed.jpg"
            compressor = adaptive_huffman.AdaptiveHuffman_IMG(compressed_file)

        elif decompression_algorithm == 'LZW':
            decompressed_file_path = f"DecompressedFiles/{os.path.basename(compressed_file).split('_LZWCompressed.txt')[0]}_LZWDecompressed.jpg"
            compressor = lzw.LZW_IMG(compressed_file)

        compressor.decompress()
        decompressed_image = Image.open(decompressed_file_path)
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

    compression_options = ['Adaptive Huffman', 'LZW', 'LZ77','JPEG']
    compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

    if compression_algorithm == 'LZ77':
        searchWindow = st.slider("Enter the search window sze:", min_value=1,  step=1)
        previewWindow = st.slider("Enter the preview window ize:", min_value=1,  step=1)

    if st.button("Compress"):
        if not uploaded_files:
            st.warning("Please upload at least one image.")
            return

        compressed_files = compress_images(uploaded_files, compression_algorithm)

        st.markdown("----")
        st.success("Compression completed!")
        st.markdown("**Download compressed files:**")
        for compressed_file in compressed_files:
            st.download_button(
                label="DOWNLOAD " + os.path.basename(compressed_file),
                data=compressed_file,
                file_name=os.path.basename(compressed_file)
            )

    elif mode == 'Decompress':
        st.markdown("**Upload compressed files**")
        compressed_files = st.file_uploader("Choose files", accept_multiple_files=True, type=['txt'], key="compressed_files")

        decompression_options = ['Adaptive Huffman', 'LZW']
        decompression_algorithm = st.selectbox("Select decompression algorithm", decompression_options)

        if st.button("Decompress"):
            if not compressed_files:
                st.warning("Please upload at least one compressed file.")
                return

            decompressed_images = decompress_images(compressed_files, decompression_algorithm)

            elif compression_algorithm == 'LZ77':
                compressor = lz77.LZ77(image_path, searchWindowSize=searchWindow, previewWindowSize=previewWindow)
                compressor.compress()
                # before = compressor.original_file_size
                # after = compressor.compressed_file_size

                decompressor = lz77.LZ77(os.path.join("CompressedFiles",uploaded_file.name.split('.')[0] + "_LZ77compressed.txt"))
                decompressor.decompress()

            st.markdown("----")
            st.success("Decompression completed!")
            st.markdown("**Original Images:**")
            for image in decompressed_images:
                st.image(image)


def run():
    st.sidebar.title("Image Compression App")
    image_compression()