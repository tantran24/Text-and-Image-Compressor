from decimal import getcontext

import pandas as pd
import streamlit as st

from apps.algorithms import ae
from apps.algorithms import huffman

def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())

global AttributeError
def text_compression():
    st.title("Text Compression")

    mode = st.sidebar.radio('Select App', ["Compress", "Decompress"])

    input_text = st.text_area("Enter the text to compress:")
    output_text = st.empty()

    compression_options = ['Huffman', 'Arithmetic', 'LZ77', 'LZW']
    compression_algorithm = st.sidebar.selectbox("Select compression algorithm", compression_options)

    if mode == "Compress":
        if not input_text:
            st.warning("Please enter some text.")
            return

        if compression_algorithm == 'Huffman':
            if st.button("Compress"):

                HF = huffman.Huffman(input_text)

                encoding, tree, codes, before, after = HF.encode_text()

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

        elif compression_algorithm == 'Arithmetic':
            precision = st.number_input("Enter the precision:", min_value=1, value=28, step=1)

            getcontext().prec = precision
            if st.button("Compress"):
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

    if mode == "Decompress":
        if compression_algorithm == 'Huffman':
            if st.button("Decompress"):
                HF = huffman.Huffman(input_text)
                encoding, tree, codes, before, after = HF.encode_text()
                decoded_output = HF.decoding_text(encoding, tree)
                st.text(f"Encoded output: {encoding}")
                output_text.text(f"Decoded output: {decoded_output}")

        elif compression_algorithm == 'Arithmetic':
            if st.button("Decompress"):
                pass
                decoded_msg, decoder = AE.decode(encoded_msg, len(input_text), AE.probability_table)
                decoded_msg = "".join(decoded_msg)
                st.text(f"Decoded Message: {decoded_msg}")
                st.text(f"Message Decoded Successfully? {input_text == decoded_msg}")


def run():
    st.sidebar.title("Text Compression App")
    text_compression()
