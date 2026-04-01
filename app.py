import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import random
from streamlit_image_comparison import image_comparison

# 1. Set up the web page title and layout
st.set_page_config(page_title="What Blindness Really Looks Like", layout="wide")

st.title("👁️ What Blindness Really Looks Like")
st.write("Inspired by the Perkins School for the Blind. Drag the sliders below to compare normal vision with different visual impairments.")

uploaded_file = st.file_uploader("Upload your own image to test (or we'll use the default):", type=["jpg", "jpeg", "png"])
st.divider()

# OPTIMIZATION: Resize the image before doing any heavy math
def resize_for_performance(img, max_width=800):
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
    return Image.composite(img, black_img, mask)

@st.cache_data
def apply_macular_degeneration(img):
    img_copy = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 4
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=50))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(black_img, img_copy, mask)

@st.cache_data
def apply_achromatopsia(img):
    return img.convert('L').convert('RGB')

@st.cache_data
def apply_low_vision(img):
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=10))
    enhancer = ImageEnhance.Brightness(img_blur)
    return enhancer.enhance(0.5)

@st.cache_data
def apply_cataracts(img):
    # Overall blur and yellow/brown tint
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=4))
    yellow_tint = Image.new('RGB', img.size, (255, 235, 190))
    blended = Image.blend(img_blur, yellow_tint, alpha=0.3)
    
    # Add noticeable white cloudy spots
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
    
    return Image.composite(white_img, blended, cloud_mask)

@st.cache_data
def apply_diabetic_retinopathy(img):
    img_copy = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    
    # Add many large, noticeable dark spots
    random.seed(42) 
    for _ in range(30): 
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(20, min(width, height) // 4) 
        draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
        
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8)) # Less blur = darker, sharper spots
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(black_img, img_copy, mask)

# ==========================================
# FILTER FUNCTIONS (CVI Profiles)
# ==========================================
@st.cache_data
def apply_cvi_tina(img):
    """Tina: 20/100 vision, nystagmus, and optic nerve atrophy."""
    # Heavy blur for 20/100 and atrophy
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=15))
    # Slight optical offset blended in to simulate nystagmus (shaking eyes)
    offset_img = Image.new("RGB", img.size)
    offset_img.paste(img_blur, (15, 0)) 
    return Image.blend(img_blur, offset_img, alpha=0.5)

@st.cache_data
def apply_cvi_dagbjort(img):
    """Dagbjört: Fatigue creates a view like looking through a straw."""
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 10 # Extreme pinhole effect
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=15))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask)

@st.cache_data
def apply_cvi_omer(img):
    """Omer: Cannot process faces or focal details."""
    # Scramble/heavily blur the focal points (center of the image)
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=30))
    
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 3
    center_x, center_y = width // 2, height // 2
    
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=40))
    
    return Image.composite(img_blur, img, mask)

@st.cache_data
def apply_cvi_krish(img):
    """Krish: Cannot see below eye level."""
    mask = Image.new('L', img.size, 255)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    
    draw.rectangle((0, height // 2, width, height), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask)

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
st.header("Medical Eye Conditions")
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("**1. Glaucoma**")
    st.caption("Optic nerve damage resulting in 'tunnel vision'.")
    image_comparison(original_image, apply_glaucoma(original_image), label1="Normal Vision", label2="Glaucoma")

with row1_col2:
    st.markdown("**2. Macular Degeneration**")
    st.caption("Deteriorates the retina's center, creating a blind spot.")
    image_comparison(original_image, apply_macular_degeneration(original_image), label1="Normal Vision", label2="Macular Degeneration")

with row1_col3:
    st.markdown("**3. Achromatopsia**")
    st.caption("A partial or total absence of all color vision.")
    image_comparison(original_image, apply_achromatopsia(original_image), label1="Normal Vision", label2="Achromatopsia")

st.write("") # Spacing between rows

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("**4. Cataracts**")
    st.caption("Clouding and yellowing of the eye's natural lens.")
    image_comparison(original_image, apply_cataracts(original_image), label1="Normal Vision", label2="Cataracts")

with row2_col2:
    st.markdown("**5. Diabetic Retinopathy**")
    st.caption("Damaged blood vessels create dark floaters and blind spots.")
    image_comparison(original_image, apply_diabetic_retinopathy(original_image), label1="Normal Vision", label2="Diabetic Retinopathy")

with row2_col3:
    st.markdown("**6. Low Vision**")
    st.caption("Severe, uncorrectable blurriness and dimness.")
    image_comparison(original_image, apply_low_vision(original_image), label1="Normal Vision", label2="Low Vision")

st.divider()

# ==========================================
# RENDER GRID: 1x4 CVI Profiles
# ==========================================
st.header("🧠 Cortical/Cerebral Visual Impairment (CVI)")
st.write("CVI is a neurological impairment where the eyes capture light, but the brain struggles to process the signals. Every individual's experience is unique. Below are profiles inspired by real students at the Perkins School for the Blind.")

cvi_col1, cvi_col2, cvi_col3, cvi_col4 = st.columns(4)

with cvi_col1:
    st.markdown("**Profile: Tina**")
    st.caption("Experiences 20/100 vision, optic nerve atrophy, and the shakiness of nystagmus.")
    image_comparison(original_image, apply_cvi_tina(original_image), label1="Normal Vision", label2="Tina's CVI")

with cvi_col2:
    st.markdown("**Profile: Dagbjört**")
    st.caption("When fatigued, her vision shrinks down to a view comparable to looking through a straw.")
    image_comparison(original_image, apply_cvi_dagbjort(original_image), label1="Normal Vision", label2="Dagbjört's CVI")

with cvi_col3:
    st.markdown("**Profile: Omer**")
    st.caption("Struggles to process faces or focal details, relying on voices and context instead.")
    image_comparison(original_image, apply_cvi_omer(original_image), label1="Normal Vision", label2="Omer's CVI")

with cvi_col4:
    st.markdown("**Profile: Krish**")
    st.caption("Experiences a specific visual field loss where he cannot process information below eye level.")
    image_comparison(original_image, apply_cvi_krish(original_image), label1="Normal Vision", label2="Krish's CVI")
