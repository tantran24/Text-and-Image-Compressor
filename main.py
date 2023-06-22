from decimal import getcontext

import pandas as pd
import streamlit as st
from PIL import Image

import ae
import huffman


def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


def text_compression():
    st.title("Text Compression")

    input_text = st.text_area("Enter the text to compress:")
    output_text = st.empty()

    compression_options = ['Huffman', 'Arithmetic', 'LZ77', 'LZW']
    compression_algorithm = st.sidebar.selectbox("Select compression algorithm", compression_options)

    if st.sidebar.button("Compress"):
        if not input_text:
            st.warning("Please enter some text.")
            return

        if compression_algorithm == 'Huffman':
            encoding, tree, codes, before, after = huffman.encoding_text(input_text)

            output_text.text(f"Encoded output: {encoding}")

            st.subheader("Encoding Table:")
            table_data = []
            for symbol, code in codes.items():
                table_data.append([symbol, code])

            table = pd.DataFrame(
                table_data,
                columns=("Symbol", "Code"))

            st.table(table)

            percent_saved = (1 - after / before) * 100

            st.markdown("### Compression Results")
            st.text(f"Original Size: {before} bits")
            st.text(f"Compressed Size: {after} bits")
            st.text(f"Percent Saved: {percent_saved:.2f}%")

            st.session_state.compression_results = {
                'algorithm': compression_algorithm,
                'encoded_output': encoding,
                'tree': tree,
                'codes': codes
            }

        elif compression_algorithm == 'Arithmetic':
            precision = st.number_input("Enter the precision:", min_value=1, value=28, step=1)

            getcontext().prec = precision

            frequency_table = {}
            for char in input_text:
                if char in frequency_table:
                    frequency_table[char] += 1
                else:
                    frequency_table[char] = 1

            AE = ae.ArithmeticEncoding(frequency_table=frequency_table)

            st.text(f"Original Message: {input_text}")
            encoded_msg, encoder, interval_min_value, interval_max_value = AE.encode(msg=input_text,
                                                                                     probability_table=AE.probability_table)
            st.text(f"Encoded Message: {encoded_msg}")
            binary_code, encoder_binary = AE.encode_binary(float_interval_min=interval_min_value,
                                                           float_interval_max=interval_max_value)
            st.text(f"The binary code is: {binary_code}")

            st.session_state.compression_results = {
                'algorithm': compression_algorithm,
                'encoded_msg': encoded_msg,
                'encoder': encoder
            }

    if st.sidebar.button("Decompress"):
        if input_text:
            compression_results = st.session_state.get('compression_results', {})
            compression_algorithm = compression_results.get('algorithm')

            if compression_algorithm == 'Huffman':
                encoding = compression_results.get('encoded_output')
                tree = compression_results.get('tree')
                decoded_output = huffman.decoding_text(encoding, tree)
                st.text(f"Encoded output: {encoding}")
                output_text.text(f"Decoded output: {decoded_output}")

            elif compression_algorithm == 'Arithmetic':
                encoded_msg = compression_results.get('encoded_msg')
                decoded_msg, decoder = AE.decode(encoded_msg, len(input_text), AE.probability_table)
                decoded_msg = "".join(decoded_msg)
                st.text(f"Decoded Message: {decoded_msg}")
                st.text(f"Message Decoded Successfully? {input_text == decoded_msg}")


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
