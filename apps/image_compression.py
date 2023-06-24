import streamlit as st
from PIL import Image


def get_file_size(file_path):
    with open(file_path, 'rb') as file:
        return len(file.read())


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


def run():
    st.sidebar.title("Image Compression App")
    image_compression()
