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
st.set_page_config(
    page_title="JPEG Image Compressor",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/compress.png", width=100)
    st.title("📚 Guide")
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    - Multiple image formats (JPEG, PNG, WebP)
    - Batch processing
    - Quality control
    - Image resizing
    - Format conversion
    """)
    
    st.markdown("### 🔧 How to Use")
    st.markdown("""
    1. **Upload Images**
       - Click 'Browse files' or drag & drop
       - Supports JPG, PNG, and WebP
    
    2. **Adjust Settings**
       - Choose output format
       - Set quality level
       - Adjust image scale
       - Rename output files
    
    3. **Process Images**
       - Single image: Click 'Compress'
       - Multiple images: Enable 'Process all' and click 'Compress All'
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - **For Web Images**: Use JPEG with 'Medium' quality
    - **For Photos**: Use JPEG with 'High' quality
    - **For Graphics**: Use PNG for best quality
    - **For Modern Web**: Try WebP format
    - **Batch Processing**: Enable for multiple images
    """)
    
    st.markdown("### 📊 Quality Guide")
    st.markdown("""
    - **High**: Best quality, larger file size
    - **Good**: Great quality, optimized size
    - **Medium**: Balanced quality/size
    - **Low**: Small size, visible loss
    - **Poor**: Smallest size, significant loss
    """)
    
    st.divider()
    st.markdown("### 🔗 Links")
    st.markdown("""
    - [GitHub Repository](https://github.com/mahanteshimath/JPEG_IMAGE_COMPRESSOR)
    - [Report an Issue](https://github.com/mahanteshimath/JPEG_IMAGE_COMPRESSOR/issues)
    """)
    
    st.divider()
    st.markdown("Made with ❤️ by [mahanteshimath](https://github.com/mahanteshimath)")


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

                # Calculate total compression statistics
                total_original_size = sum(len(file.getvalue()) for file in uploaded_files)
                total_compressed_size = sum(len(file["data"]) for file in compressed_files)
                total_ratio = (1 - total_compressed_size / total_original_size) * 100
                
                # Show batch compression results (simple markdown)
                st.success(f"✅ Successfully compressed {len(uploaded_files)} images!")
                st.markdown(f"""
**📊 Batch Compression Results**

- 📥 Total Original Size: {total_original_size/1024:.1f} KB
- 📤 Total Compressed Size: {total_compressed_size/1024:.1f} KB
- 📈 Average Compression Ratio: {total_ratio:.1f}%
- 🖼️ Images Processed: {len(compressed_files)}
                """)
                
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
                
                # Calculate sizes and compression ratio
                original_size = len(uploaded_files[st.session_state.current_image].getvalue())
                compressed_size = len(compressed)
                ratio = (1 - compressed_size / original_size) * 100
                
                # Show compression results (simple markdown)
                st.success("✅ Image compressed successfully!")
                st.markdown(f"""
**📊 Compression Results**

- 📥 Original Size: {original_size/1024:.1f} KB
- 📤 Compressed Size: {compressed_size/1024:.1f} KB
- 📈 Compression Ratio: {ratio:.1f}%
                """)
                
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
