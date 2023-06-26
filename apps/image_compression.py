import streamlit as st
from PIL import Image

from apps.algorithms import adaptive_huffman

def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


def image_compression():
    st.title("Image Compression")

    st.markdown("**Upload up to 20 images**")
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'],
                                      key="image")

    compression_options = ['Adaptive Huffman', 'LWZ']
    compression_algorithm = st.selectbox("Select compression algorithm", compression_options)

    output_path = "compressed_image.bin"

    if st.button("Compress"):
        if not uploaded_files:
            st.warning("Please upload at least one image.")
            return

        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_path = f"temp_images/{uploaded_file.name}"
            image.save(image_path)

            if compression_algorithm == 'Adaptive Huffman':
                ah = adaptive_huffman.AdaptiveHuffman()
                encoded_data = ah.encode_image(image_path)


                with open(output_path, "wb") as file:
                    for bit_string in encoded_data:
                        num_bytes = len(bit_string) // 8
                        bit_string_padded = bit_string.ljust(num_bytes * 8, "0")

                        for i in range(0, len(bit_string_padded), 8):
                            byte = int(bit_string_padded[i:i + 8], 2)
                            file.write(bytes([byte]))

            elif compression_algorithm == 'LWZ':
                pass

            st.image(image)
            st.markdown("----")


def run():
    st.sidebar.title("Image Compression App")
    image_compression()
