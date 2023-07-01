from decimal import getcontext

import pandas as pd
import streamlit as st
from apps.algorithms import ae
from apps.algorithms import huffman
from apps.algorithms import lzw



def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


global AttributeError


def text_compression():
    st.title("Text Compression")
    mode = st.sidebar.radio('Select App', ["Compress", "Decompress"])

    options = ['Enter', 'Upload']
    selection = st.sidebar.selectbox("Select option ", options)
    input_text = None
    output_text = st.empty()
    check_point = 0       
    compression_options = ['Huffman', 'Arithmetic', 'LZ77', 'LZW']
    compression_algorithm = st.sidebar.selectbox("Select compression algorithm", compression_options)

    def compress(input_text, name_path=None):
        encoding, encoding_text = " a", " b "
        decoded_output = " c"

        if mode == "Compress":
            if not input_text:
                st.warning("Please enter some text.")
                check_point = 1
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

            elif compression_algorithm == 'LZW':
                compressor = lzw.LZW_TEXT()
                encoding = compressor.compress(input_text)
                encoding_text = compressor.compress_text(input_text)
                before, after = len(input_text)*8, len(encoding)*8

                
            if selection == 'Enter':
                st.text(f"Encoded output: {encoding}")
                st.text(f"Encoded text: {encoding_text}")

            elif selection == 'Upload':
                name_file_comp = uploaded_file.name.split('.')[0] + "_" + compression_algorithm + "." + uploaded_file.name.split('.')[1] 
                text_path_save = f"CompressedFiles/{name_file_comp}"
                with open(text_path_save, 'w', encoding="utf-8") as file:    
                    file.write(str(encoding_text))


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

            elif compression_algorithm == 'LZW':
                if st.button("Decompress"):
                    compressor = lzw.LZW_TEXT()
                    decoded_output = compressor.decompress_text(input_text)

                    

            if selection == 'Enter':
                st.text(f"Decoded output: {decoded_output}")

            elif selection == 'Upload':
                name_file_comp = uploaded_file.name.split('.')[0] + "_" + compression_algorithm + "." + uploaded_file.name.split('.')[1] 
                text_path_save = f"DecompressedFiles/{name_file_comp}"
                with open(text_path_save, 'w', encoding="utf-8") as file:    
                    file.write(decoded_output)


                    
    if selection == 'Enter':
        input_text = st.text_area("Enter the text to compress:")
        compress(input_text)
    elif selection == 'Upload':
        uploaded_files = st.file_uploader("Choose text", accept_multiple_files=True, type=['txt', 'doc', 'docx'],
                                    key="text")
        
        for uploaded_file in uploaded_files:
            text_path = f"temp_texts/{uploaded_file.name}"
            input_text = uploaded_file.read()  
            with open(text_path, 'w', encoding="utf-8") as file:    
                file.write(input_text.decode())
            input_text = input_text.decode()
            compress(input_text, uploaded_file.name)
            st.text("Done!!!")
            
    if check_point == 1:
        return

def run():
    st.sidebar.title("Text Compression App")
    text_compression()