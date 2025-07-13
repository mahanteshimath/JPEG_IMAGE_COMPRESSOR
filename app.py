import io
import zipfile
import streamlit as st
from tools.tools_img import (
    compress_img,
    formated_name_img,
    get_filename_without_extension,
    manipulate_img,
    open_img,
    quality_img,
    scale_img,
)

# Page config and styling
st.set_page_config(page_title="JPEG Image Compressor", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #2B1B3D;
        text-align: center;
        padding: 1rem;
        border: solid #2B1B3D;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #2B1B3D;
        color: white;
        width: 100%;
    }
    .stDownloadButton>button {
        background-color: #28a745;
        color: white;
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1>JPEG Image Compressor</h1>", unsafe_allow_html=True)

st.write("""
👋 Welcome to JPEG Image Compressor! 
Your one-stop solution for optimizing images for the web.
Compress single or multiple images with just a few clicks!
""")

st.write("---")

# Initialize session state
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0

# File upload section
st.write("## 📂 Upload Images")
uploaded_files = st.file_uploader("Choose image files", 
                                ["jpg", "jpeg", "png", "webp"], 
                                accept_multiple_files=True)

if uploaded_files:
    # Create three columns for layout
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.write("### Preview")
        current_img = open_img(uploaded_files[st.session_state.current_image])
        st.image(current_img, use_container_width=True)
        st.write(f"Image {st.session_state.current_image + 1}/{len(uploaded_files)}")

    with col2:
        st.write("### Settings")
        # Batch processing option
        batch_process = st.checkbox("Process all images at once", 
                                  help="Apply same settings to all images")
        
        # Image settings
        name = st.text_input("Output filename", 
                           get_filename_without_extension(
                               uploaded_files[st.session_state.current_image].name))
        
        format_type = st.selectbox("Output format", 
                                 ["JPEG", "PNG", "WEBP"], 
                                 index=0)
        
        quality = st.select_slider("Quality", 
                                 ["Poor", "Low", "Medium", "Good", "High"], 
                                 value="Medium")
        
        scale = st.slider("Scale (%)", 1, 100, 100)

    with col3:
        st.write("### Actions")
        # Navigation buttons (if not batch processing)
        if not batch_process and len(uploaded_files) > 1:
            cols = st.columns(2)
            with cols[0]:
                if st.button("Previous", use_container_width=True) and st.session_state.current_image > 0:
                    st.session_state.current_image -= 1
            with cols[1]:
                if st.button("Next", use_container_width=True) and st.session_state.current_image < len(uploaded_files) - 1:
                    st.session_state.current_image += 1

        # Compression settings
        user_settings = {
            "img_converted_name": name,
            "img_converted_extension": format_type,
            "img_converted_quality": quality,
            "img_converted_scale": scale
        }

        if batch_process:
            if st.button("Compress All", use_container_width=True):
                compressed_files = []
                progress_bar = st.progress(0)
                
                for idx, file in enumerate(uploaded_files):
                    compressed_data = manipulate_img(file, user_settings)
                    compressed_files.append({
                        "name": f"{name}_{idx+1}.{format_type.lower()}",
                        "data": compressed_data
                    })
                    progress_bar.progress((idx + 1) / len(uploaded_files))

                # Create ZIP file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file in compressed_files:
                        zip_file.writestr(file["name"], file["data"])
                
                st.download_button(
                    "Download All (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="compressed_images.zip",
                    use_container_width=True
                )
        else:
            if st.button("Compress", use_container_width=True):
                compressed = manipulate_img(
                    uploaded_files[st.session_state.current_image], 
                    user_settings
                )
                st.download_button(
                    "Download",
                    data=compressed,
                    file_name=formated_name_img(user_settings),
                    mime=f"image/{format_type.lower()}",
                    use_container_width=True
                )

        # Display image info
        current_img = open_img(uploaded_files[st.session_state.current_image])
        preview_compressed = compress_img(current_img, user_settings)
        
        st.write("### Image Info")
        st.write(f"""
        - **Original size:** {current_img.size[0]}x{current_img.size[1]}px
        - **New size:** {int(current_img.size[0]*scale/100)}x{int(current_img.size[1]*scale/100)}px
        - **Format:** {format_type}
        - **Quality:** {quality}
        """)
else:
    st.info("👆 Upload some images to get started!")
