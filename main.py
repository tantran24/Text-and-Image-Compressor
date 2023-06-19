import streamlit as st
from PIL import Image

import huffman
import lz77
import lzw
import rle

def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


def text_compression():
    st.title("Text Compression")

    input_text = st.text_area("Enter the text to compress:")
    output_text = st.empty()

    compression_options = ['Huffman', 'LZ77', 'RLE', 'LZW']
    compression_algorithm = st.sidebar.selectbox("Select compression algorithm", compression_options)

    if st.sidebar.button("Compress"):
        if not input_text:
            st.warning("Please enter some text.")
            return

        if compression_algorithm == 'Huffman':
            encoding, tree, codes, before, after = huffman.encoding_text(input_text)

            output_text.text(f"Encoded output: {encoding}")

            st.subheader("Encoding Table:")
            table_data = [["Symbol", "Code"]]
            for symbol, code in codes.items():
                table_data.append([symbol, code])
            st.table(table_data)

        elif compression_algorithm == 'LZ77':
            pass
        elif compression_algorithm == 'RLE':
            pass
        elif compression_algorithm == 'LZW':
            pass
        percent_saved = (1 - after / before) * 100

        st.markdown("### Compression Results")
        st.text(f"Original Size: {before} bits")
        st.text(f"Compressed Size: {after} bits")
        st.text(f"Percent Saved: {percent_saved:.2f}%")

    if st.sidebar.button("Decompress"):
        if input_text:
            if compression_algorithm == 'Huffman':
                encoding, tree, codes, before, after = huffman.encoding_text(input_text)
                decoded_output = huffman.decoding_text(encoding, tree)
            elif compression_algorithm == 'LZ77':
                pass
            elif compression_algorithm == 'RLE':
                pass
            elif compression_algorithm == 'LZW':
                pass

            st.text(f"Encoded output: {encoding}")
            output_text.text(f"Decoded output: {decoded_output}")


def image_compression():
    st.title("Image Compression")

    st.markdown("**Upload up to 20 images**")
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'],
                                      key="image")

    compression_options = ['Huffman', 'LWZ']
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
                pass
            elif compression_algorithm == 'Huffman':
                pass

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
