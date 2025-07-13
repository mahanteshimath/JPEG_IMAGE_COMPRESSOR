from PIL import Image
import io

def open_img(uploaded_file):
    return Image.open(uploaded_file)

def get_filename_without_extension(filename):
    return filename.rsplit('.', 1)[0]

def formated_name_img(user_data):
    return f"{user_data['img_converted_name']}.{user_data['img_converted_extension'].lower()}"

def scale_img(img, user_data):
    width, height = img.size
    new_width = int(width * (user_data['img_converted_scale'] / 100))
    new_height = int(height * (user_data['img_converted_scale'] / 100))
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def quality_img(quality_setting):
    quality_map = {
        "Poor": 10,
        "Low": 30,
        "Medium": 60,
        "Good": 80,
        "High": 95
    }
    return quality_map.get(quality_setting, 60)

def compress_img(img, user_data):
    buf = io.BytesIO()
    img.save(buf, format=user_data['img_converted_extension'], 
             quality=quality_img(user_data['img_converted_quality']))
    buf.seek(0)
    return buf

def manipulate_img(uploaded_file, user_data):
    img = open_img(uploaded_file)
    img = scale_img(img, user_data)
    return compress_img(img, user_data).getvalue()
