import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import random
from streamlit_image_comparison import image_comparison

# 1. Set up the web page title and layout
st.set_page_config(page_title="What Blindness Really Looks Like", layout="wide")

st.markdown("<h1 style='text-align: center;'>👁️ What Blindness Really Looks Like</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Inspired by the Perkins School for the Blind. Drag the sliders below to compare normal vision with different visual impairments.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your own image to test (or we'll use the default):", type=["jpg", "jpeg", "png"])
st.divider()

# OPTIMIZATION & SIZING: Resize the image to be 30% larger than the previous step (max 260px wide)
def resize_for_performance(img, max_width=260):
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        return img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return img

# ==========================================
# FILTER FUNCTIONS (Standard Conditions)
# ==========================================
@st.cache_data
def apply_glaucoma(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 3
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=80))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask).convert("RGB")

@st.cache_data
def apply_macular_degeneration(img):
    img_copy = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 4
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20)) 
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(black_img, img_copy, mask).convert("RGB")

@st.cache_data
def apply_achromatopsia(img):
    return img.convert('L').convert('RGB')

@st.cache_data
def apply_low_vision(img):
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=10))
    enhancer = ImageEnhance.Brightness(img_blur)
    return enhancer.enhance(0.5).convert("RGB")

@st.cache_data
def apply_cataracts(img):
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=4))
    yellow_tint = Image.new('RGB', img.size, (255, 235, 190))
    blended = Image.blend(img_blur, yellow_tint, alpha=0.3)
    
    cloud_mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(cloud_mask)
    width, height = img.size
    
    random.seed(10)
    for _ in range(8): 
        x, y = random.randint(0, width), random.randint(0, height)
        r = random.randint(width // 8, width // 4)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=200) 
        
    cloud_mask = cloud_mask.filter(ImageFilter.GaussianBlur(radius=20))
    white_img = Image.new('RGB', img.size, (255, 255, 255))
    
    return Image.composite(white_img, blended, cloud_mask).convert("RGB")

@st.cache_data
def apply_diabetic_retinopathy(img):
    img_copy = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    
    random.seed(42) 
    for _ in range(30): 
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(20, min(width, height) // 4) 
        draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
        
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8))
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(black_img, img_copy, mask).convert("RGB")

# 3. Load AND Optimize the image
if uploaded_file is not None:
    raw_image = Image.open(uploaded_file).convert("RGB")
else:
    try:
        raw_image = Image.open("sample_image.jpg").convert("RGB")
    except FileNotFoundError:
        st.error("Please place an image named 'sample_image.jpg' in the same folder, or upload an image above!")
        st.stop()

original_image = resize_for_performance(raw_image)

# ==========================================
# RENDER GRID: 3x2 Standard Conditions
# ==========================================
st.markdown("<h2 style='text-align: center;'>Medical Eye Conditions</h2><br>", unsafe_allow_html=True)

# ROW 1 - Using spacer columns on the left and right to center the grid and leave white space
spacer_left_1, col1, col2, col3, spacer_right_1 = st.columns([1, 3, 3, 3, 1])

with col1:
    st.markdown("<h3 style='text-align: center;'>1. Glaucoma</h3>", unsafe_allow_html=True)
    # Replaced hardcoded width with parameter alignment for the new size
    image_comparison(original_image, apply_glaucoma(original_image), label1="Normal", label2="Glaucoma", width=260)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: -15px;'>
        <b>The Condition:</b> Damages the optic nerve, often caused by abnormally high eye pressure. It typically develops slowly, with the first sign usually being the loss of peripheral vision.<br><br>
        <b>What's in the Image:</b> Creates a "tunnel vision" effect. The center remains clear, but the outer edges are heavily darkened and blurred.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='text-align: center;'>2. Macular Degeneration</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_macular_degeneration(original_image), label1="Normal", label2="Macular Degen.", width=260)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: -15px;'>
        <b>The Condition:</b> Deterioration of the central portion of the retina. Because it affects the center of the visual field, reading and recognizing faces becomes very difficult.<br><br>
        <b>What's in the Image:</b> A dark, solid blurry "cloud" is applied directly over the center of the image, while peripheral edges remain clear.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("<h3 style='text-align: center;'>3. Achromatopsia</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_achromatopsia(original_image), label1="Normal", label2="Achromatopsia", width=260)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: -15px;'>
        <b>The Condition:</b> A rare, inherited vision disorder where a person has a partial or total absence of color vision, relying entirely on rod cells.<br><br>
        <b>What's in the Image:</b> The code strips away all color data and converts the image to grayscale, showing a purely black-and-white scene.
    </div>
    """, unsafe_allow_html=True)

st.write("<br><br>", unsafe_allow_html=True) # Spacing between rows

# ROW 2 - Using identical spacer columns
spacer_left_2, col4, col5, col6, spacer_right_2 = st.columns([1, 3, 3, 3, 1])

with col4:
    st.markdown("<h3 style='text-align: center;'>4. Cataracts</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_cataracts(original_image), label1="Normal", label2="Cataracts", width=260)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: -15px;'>
        <b>The Condition:</b> A clouding of the normally clear lens of the eye, comparable to looking through a frosted window. It can also add a yellowish tint.<br><br>
        <b>What's in the Image:</b> The image is blurred, a warm yellow-brown tint is blended in, and cloudy white spots obscure the view.
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("<h3 style='text-align: center;'>5. Diabetic Retinopathy</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_diabetic_retinopathy(original_image), label1="Normal", label2="Diabetic Retin.", width=260)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: -15px;'>
        <b>The Condition:</b> A diabetes complication caused by damage to the blood vessels in the retina. It causes dark spots or "floaters" to appear in vision.<br><br>
        <b>What's in the Image:</b> The code generates random, prominent dark splotches across the field of view, simulating patchy vision loss.
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("<h3 style='text-align: center;'>6. Low Vision</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_low_vision(original_image), label1="Normal", label2="Low Vision", width=260)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: -15px;'>
        <b>The Condition:</b> A broad term for significant visual impairment that cannot be fully corrected, resulting in a severe loss of visual sharpness.<br><br>
        <b>What's in the Image:</b> A heavy blur is applied across the entire image and brightness is reduced, simulating a hazy, unfocused world.
    </div>
    """, unsafe_allow_html=True)
