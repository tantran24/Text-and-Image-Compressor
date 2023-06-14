import streamlit as st
from PIL import Image

import huffman_compression
import lz77_compression
import lzw_compression
import rle_compression

global encoding_table


def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


def text_compression():
    st.title("Text Compression")

    text = st.text_area("Enter the text to compress", height=200)
    compression_options = ['Huffman', 'LZ77', 'RLE', 'LZW']
    compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

    if st.button("Compress"):
        if not text:
            st.warning("Please enter some text.")
            return

        if compression_algorithm == 'Huffman':
            compressed_text, encoding_table = huffman_compression.compress(text)
        elif compression_algorithm == 'LZ77':
            compressed_text, encoding_table = lz77_compression.compress(text)
        elif compression_algorithm == 'RLE':
            compressed_text, encoding_table = rle_compression.compress(text)
        elif compression_algorithm == 'LZW':
            compressed_text, encoding_table = lzw_compression.compress_text(text)

        compressed_size = len(compressed_text.encode())
        original_size = len(text.encode())
        saved_percent = ((original_size - compressed_size) / original_size) * 100

        st.markdown("**Compression Results**")
        st.markdown(f"Compressed text: {compressed_text}")
        st.markdown(f"Compressed size: {compressed_size} bytes")
        st.markdown(f"Original size: {original_size} bytes")
        st.markdown(f"Percent saved: {saved_percent:.2f}%")

        st.markdown("**Character Encoding Table**")
        st.table(encoding_table)

    if st.button("Decompress"):
        if not text:
            st.warning("Please enter some text.")
            return

        if compression_algorithm == 'LZ77':
            decompressed_text = lz77_compression.decompress(text)
        elif compression_algorithm == 'Huffman':
            decompressed_text = huffman_compression.decompress(text, encoding_table)
        elif compression_algorithm == 'RLE':
            decompressed_text = rle_compression.decompress(text, encoding_table)
        elif compression_algorithm == 'LZW':
            decompressed_text = lzw_compression.decompress(text, encoding_table)

        st.markdown(f"Decompressed text: {decompressed_text}")


def image_compression():
    st.title("Image Compression")

    st.markdown("**Upload up to 20 images**")
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'],
                                      key="image")

    compression_options = ['LWZ', 'Huffman']
    compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

    if st.button("Compress"):
        if not uploaded_files:
            st.warning("Please upload at least one image.")
            return

        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_path = f"temp_images/{uploaded_file.name}"
            image.save(image_path)

            if compression_algorithm == 'LWZ':
                compressed_path = lwz_compression.compress(image_path)
            elif compression_algorithm == 'Huffman':
                compressed_path = huffman_compression.compress(image_path)

            compressed_size = get_file_size(compressed_path)
            original_size = get_file_size(image_path)
            saved_percent = ((original_size - compressed_size) / original_size) * 100

            st.markdown(f"**Image: {uploaded_file.name}**")
            st.markdown(f"Compressed size: {compressed_size} bytes")
            st.markdown(f"Original size: {original_size} bytes")
            st.markdown(f"Percent saved: {saved_percent:.2f}%")

            st.image(image)
            st.markdown("----")


def main():
    st.sidebar.title("Compression App")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Text Compression", "Image Compression"])

    if app_mode == "Text Compression":
        text_compression()
    elif app_mode == "Image Compression":
        image_compression()


if __name__ == "__main__":
    main()
