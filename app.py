import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import random
from streamlit_image_comparison import image_comparison

# 1. Set up the web page title and layout
st.set_page_config(page_title="What Blindness Really Looks Like", layout="wide")

st.markdown("<h1 style='text-align: center;'>👁️ What Blindness Really Looks Like</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Inspired by the Perkins School for the Blind. Drag the sliders below to compare normal vision with different visual impairments.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your own image to test (or we'll use the default):", type=["jpg", "jpeg", "png"])
st.divider()

# OPTIMIZATION & SIZING: Resize the image to be 50% smaller (max 400px wide)
def resize_for_performance(img, max_width=400):
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
    # Reduced blur from 50 to 20 to keep the center completely solid and dark
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

# ==========================================
# FILTER FUNCTIONS (CVI Profiles)
# ==========================================
@st.cache_data
def apply_cvi_tina(img):
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=15))
    offset_img = Image.new("RGB", img.size)
    offset_img.paste(img_blur, (15, 0)) 
    return Image.blend(img_blur, offset_img, alpha=0.5).convert("RGB")

@st.cache_data
def apply_cvi_dagbjort(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 10 
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=15))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask).convert("RGB")

@st.cache_data
def apply_cvi_omer(img):
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=30))
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 3
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=40))
    
    return Image.composite(img_blur, img, mask).convert("RGB")

@st.cache_data
def apply_cvi_krish(img):
    mask = Image.new('L', img.size, 255)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    draw.rectangle((0, height // 2, width, height), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask).convert("RGB")

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
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("<h3 style='text-align: center;'>1. Glaucoma</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_glaucoma(original_image), label1="Normal", label2="Glaucoma")
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; padding-top: 10px;'>
        <b>The Condition:</b> Damages the optic nerve, often caused by abnormally high eye pressure. It typically develops slowly, with the first sign usually being the loss of peripheral vision.<br><br>
        <b>What's in the Image:</b> Creates a "tunnel vision" effect. The center remains clear, but the outer edges are heavily darkened and blurred.
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("<h3 style='text-align: center;'>2. Macular Degeneration</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_macular_degeneration(original_image), label1="Normal", label2="Macular Degen.")
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; padding-top: 10px;'>
        <b>The Condition:</b> Deterioration of the central portion of the retina. Because it affects the center of the visual field, reading and recognizing faces becomes very difficult.<br><br>
        <b>What's in the Image:</b> A dark, solid blurry "cloud" is applied directly over the center of the image, while peripheral edges remain clear.
    </div>
    """, unsafe_allow_html=True)

with row1_col3:
    st.markdown("<h3 style='text-align: center;'>3. Achromatopsia</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_achromatopsia(original_image), label1="Normal", label2="Achromatopsia")
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; padding-top: 10px;'>
        <b>The Condition:</b> A rare, inherited vision disorder where a person has a partial or total absence of color vision, relying entirely on rod cells.<br><br>
        <b>What's in the Image:</b> The code strips away all color data and converts the image to grayscale, showing a purely black-and-white scene.
    </div>
    """, unsafe_allow_html=True)

st.write("<br><br>", unsafe_allow_html=True) # Spacing between rows

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("<h3 style='text-align: center;'>4. Cataracts</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_cataracts(original_image), label1="Normal", label2="Cataracts")
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; padding-top: 10px;'>
        <b>The Condition:</b> A clouding of the normally clear lens of the eye, comparable to looking through a frosted window. It can also add a yellowish tint.<br><br>
        <b>What's in the Image:</b> The image is blurred, a warm yellow-brown tint is blended in, and cloudy white spots obscure the view.
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown("<h3 style='text-align: center;'>5. Diabetic Retinopathy</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_diabetic_retinopathy(original_image), label1="Normal", label2="Diabetic Retin.")
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; padding-top: 10px;'>
        <b>The Condition:</b> A diabetes complication caused by damage to the blood vessels in the retina. It causes dark spots or "floaters" to appear in vision.<br><br>
        <b>What's in the Image:</b> The code generates random, prominent dark splotches across the field of view, simulating patchy vision loss.
    </div>
    """, unsafe_allow_html=True)

with row2_col3:
    st.markdown("<h3 style='text-align: center;'>6. Low Vision</h3>", unsafe_allow_html=True)
    image_comparison(original_image, apply_low_vision(original_image), label1="Normal", label2="Low Vision")
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; padding-top: 10px;'>
        <b>The Condition:</b> A broad term for significant visual impairment that cannot be fully corrected, resulting in a severe loss of visual sharpness.<br><br>
        <b>What's in the Image:</b> A heavy blur is applied across the entire image and brightness is reduced, simulating a hazy, unfocused world.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================
# RENDER GRID: 1x4 CVI Profiles
# ==========================================
st.markdown("<h2 style='text-align: center;'>🧠 Cortical/Cerebral Visual Impairment (CVI)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>CVI is a neurological impairment where the eyes capture light, but the brain struggles to process the signals. Every individual's experience is unique.</p><br>", unsafe_allow_html=True)

cvi_col1, cvi_col2, cvi_col3, cvi_col4 = st.columns(4)

with cvi_col1:
    st.markdown("<h4 style='text-align: center;'>Profile: Tina</h4>", unsafe_allow_html=True)
    image_comparison(original_image, apply_cvi_tina(original_image), label1="Normal", label2="Tina's CVI")
    st.markdown("""
    <div style='text-align: center; font-size: 0.85em; padding-top: 10px;'>
        <b>The Condition:</b> Tina has 20/100 vision, optic nerve atrophy, and nystagmus (involuntary eye shaking).<br><br>
        <b>What's in the Image:</b> Heavy blur limits sharpness, while a duplicated offset simulates visual instability.
    </div>
    """, unsafe_allow_html=True)

with cvi_col2:
    st.markdown("<h4 style='text-align: center;'>Profile: Dagbjört</h4>", unsafe_allow_html=True)
    image_comparison(original_image, apply_cvi_dagbjort(original_image), label1="Normal", label2="Dagbjört's CVI")
    st.markdown("""
    <div style='text-align: center; font-size: 0.85em; padding-top: 10px;'>
        <b>The Condition:</b> When fatigued, her brain restricts how much visual data it takes in to conserve energy.<br><br>
        <b>What's in the Image:</b> An extreme "pinhole" effect shrinks her field of view down to the size of a straw.
    </div>
    """, unsafe_allow_html=True)

with cvi_col3:
    st.markdown("<h4 style='text-align: center;'>Profile: Omer</h4>", unsafe_allow_html=True)
    image_comparison(original_image, apply_cvi_omer(original_image), label1="Normal", label2="Omer's CVI")
    st.markdown("""
    <div style='text-align: center; font-size: 0.85em; padding-top: 10px;'>
        <b>The Condition:</b> Omer struggles with focal details, meaning he cannot easily process the central subject, especially faces.<br><br>
        <b>What's in the Image:</b> The focal center is heavily scrambled, forcing reliance on peripheral context.
    </div>
    """, unsafe_allow_html=True)

with cvi_col4:
    st.markdown("<h4 style='text-align: center;'>Profile: Krish</h4>", unsafe_allow_html=True)
    image_comparison(original_image, apply_cvi_krish(original_image), label1="Normal", label2="Krish's CVI")
    st.markdown("""
    <div style='text-align: center; font-size: 0.85em; padding-top: 10px;'>
        <b>The Condition:</b> Krish has a specific visual field loss where his brain ignores data from the lower half of his vision.<br><br>
        <b>What's in the Image:</b> The lower half is completely blacked out, simulating struggles with tripping hazards.
    </div>
    """, unsafe_allow_html=True)
