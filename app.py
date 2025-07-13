import streamlit as st
from PIL import Image
import io

def compress_image(image, quality):
    img = Image.open(image)


st.write("""
Upload a JPEG image, select the compression quality, and download the compressed image.
""")

uploaded_file = st.file_uploader("Choose a JPEG image", type=["jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Original Image", use_column_width=True)
    quality = st.slider("Select Compression Quality", min_value=1, max_value=100, value=75)
    if st.button("Compress"):
        compressed_image = compress_image(uploaded_file, quality)
        st.success("Image compressed!")
        st.image(compressed_image, caption="Compressed Image", use_column_width=True)
        st.download_button(
            label="Download Compressed Image",
            data=compressed_image,
            file_name="compressed.jpg",
            mime="image/jpeg"
        )
