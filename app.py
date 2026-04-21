import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import random
import base64
from io import BytesIO
import os

# 1. Page Configuration
st.set_page_config(page_title="What Blindness Really Looks Like", layout="wide")

# ==========================================
# ADVANCED CSS: MOBILE OPTIMIZATION & BRANDING
# ==========================================
st.markdown("""
<style>
/* Smooth scrolling and offset for the sticky nav bar */
html {
    scroll-behavior: smooth;
    scroll-padding-top: 80px; 
}

/* Responsive main container with increased top breathing room */
.block-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding-top: 5rem !important; 
    padding-bottom: 5rem !important;
}

/* MOBILE OPTIMIZATION */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        padding-top: 3rem !important; 
    }
}

/* Sticky Navigation Bar - PERKINS BRANDING */
.nav-bar {
    display: flex;
    justify-content: center;
    flex-wrap: wrap; 
    gap: 20px;
    background-color: #1d4f91; 
    padding: 15px 10px;
    border-bottom: 4px solid #00A3E0; 
    position: -webkit-sticky; 
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.nav-bar a {
    text-decoration: none;
    color: #ffffff;
    font-weight: bold;
    font-size: 1.1em;
    letter-spacing: 0.5px;
    transition: color 0.2s ease-in-out;
}
.nav-bar a:hover {
    color: #00A3E0;
}

/* LIGHT MODE: Default Headers & Logo */
h1, h2, h3, h4 {
    text-align: center !important;
    margin-bottom: 0.2rem !important; 
    color: #1d4f91 !important; 
}

.logo-light {
    display: block;
    margin: 0 auto 15px auto;
    width: 250px !important; /* Forces exact pixel width for SVG */
    max-width: 100%; /* Ensures responsiveness on very small screens */
    height: auto;
}
.logo-dark {
    display: none; 
    margin: 0 auto 15px auto;
    width: 250px !important; /* Forces exact pixel width for SVG */
    max-width: 100%; /* Ensures responsiveness on very small screens */
    height: auto;
}

/* DARK MODE OVERRIDES */
@media (prefers-color-scheme: dark) {
    h1, h2, h3, h4 {
        color: #00A3E0 !important; 
    }
    .logo-light {
        display: none !important; 
    }
    .logo-dark {
        display: block !important; 
    }
}

/* Hide Streamlit's default file uploader size text */
div[data-testid="stFileUploader"] small {
    display: none !important;
}

.desc-wrapper {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 5px; 
    margin-bottom: 2rem;
}

.detailed-desc {
    font-size: 1.05em;
    line-height: 1.5;
    text-align: left; 
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Navigation Bar 
st.markdown("""
<div class='nav-bar'>
    <a href='#try-it-with-your-own-photo'>Uploader</a>
    <a href='#medical-eye-conditions'>Eye Conditions</a>
</div>
""", unsafe_allow_html=True)

# ==========================================
# HEADER WITH SMART LOGO SWAPPING
# ==========================================
def get_svg_base64(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        return None

logo_light_base64 = get_svg_base64("Perkins_Trademark_Color.svg")
logo_dark_base64 = get_svg_base64("Perkins_Trademark_White.svg")

if logo_light_base64 and logo_dark_base64:
    logo_html = f"""<img src='data:image/svg+xml;base64,{logo_light_base64}' alt='Perkins Logo' class='logo-light'>
<img src='data:image/svg+xml;base64,{logo_dark_base64}' alt='Perkins Logo' class='logo-dark'>"""
elif logo_light_base64:
    logo_html = f"<img src='data:image/svg+xml;base64,{logo_light_base64}' alt='Perkins Logo' style='display: block; margin: 0 auto 15px auto; width: 250px; max-width: 100%; height: auto;'>"
elif logo_dark_base64:
    logo_html = f"<img src='data:image/svg+xml;base64,{logo_dark_base64}' alt='Perkins Logo' style='display: block; margin: 0 auto 15px auto; width: 250px; max-width: 100%; height: auto;'>"
else:
    logo_html = "<p style='color:red; font-weight:bold; text-align:center;'>⚠️ Could not find logo files. Please ensure they are uploaded.</p>"

st.markdown(f"""
<div style='text-align: center; padding-top: 30px; padding-bottom: 10px;'>
<a href='https://www.perkins.org/' target='_blank'>
{logo_html}
</a>
<h1 style='font-size: 2.8em; margin-bottom: 10px;'>What Blindness Really Looks Like</h1>
<p style='font-size: 1.15em; max-width: 800px; margin: 0 auto; line-height: 1.6;'>
An interactive vision simulator inspired by the advocacy and resources of <a href='https://www.perkins.org/what-blindness-really-looks-like/' target='_blank' style='color: #00A3E0; font-weight: bold; text-decoration: none;'>Perkins School for the Blind</a>.<br>
<span style='font-size: 0.85em; opacity: 0.8;'>📸 Photo Credit: <a href='https://www.pexels.com/@ganajp/' target='_blank' style='color: #00A3E0; text-decoration: none;'>Petr Ganaj</a></span>
</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# UPLOADER SECTION
# ==========================================
st.header("📸 Try It With Your Own Photo!")
_, uploader_center, _ = st.columns([1, 2, 1])

with uploader_center:
    st.markdown("<p style='text-align: center;'>Upload a photo to see the simulations applied to your own environment.</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"], label_visibility="collapsed")

st.divider()

# ==========================================
# EFFECT FUNCTIONS
# ==========================================
@st.cache_data
def apply_glaucoma(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    w, h = img.size
    radius = min(w, h) // 3
    draw.ellipse((w//2 - radius, h//2 - radius, w//2 + radius, h//2 + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    return Image.composite(img, Image.new('RGB', img.size, (0,0,0)), mask)

@st.cache_data
def apply_macular(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    w, h = img.size
    radius = min(w, h) // 4
    draw.ellipse((w//2 - radius, h//2 - radius, w//2 + radius, h//2 + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=25))
    return Image.composite(Image.new('RGB', img.size, (0,0,0)), img, mask)

@st.cache_data
def apply_cataracts(img):
    base = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    random.seed(10)
    for _ in range(12):
        x, y = random.randint(0, img.width), random.randint(0, img.height)
        r = random.randint(img.width//15, img.width//6)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=240)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=15))
    return Image.composite(Image.new('RGB', img.size, (255,255,255)), base, mask)

@st.cache_data
def apply_retinopathy(img):
    base = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    random.seed(42)
    for _ in range(35):
        x, y = random.randint(0, img.width), random.randint(0, img.height)
        r = random.randint(10, min(img.size)//8)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8))
    return Image.composite(Image.new('RGB', img.size, (0,0,0)), base, mask)

@st.cache_data
def apply_low_vision(img):
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    return ImageEnhance.Brightness(img).enhance(0.6)

# ==========================================
# CUSTOM OVERLAY SLIDER
# ==========================================
def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=80) 
    return base64.b64encode(buffered.getvalue()).decode()

def custom_overlay_slider(img_normal, img_simulated, condition_name, height):
    img_normal_b64 = img_to_base64(img_normal)
    img_simulated_b64 = img_to_base64(img_simulated)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; font-family: sans-serif; }}
        .slider-container {{
            position: relative;
            width: 100%;
            height: {height}px; 
            background-color: transparent;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .img-layer {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover; 
            pointer-events: none;
        }}
        #img-normal {{
            clip-path: inset(0 50% 0 0); 
            z-index: 2;
        }}
        #img-simulated {{
            z-index: 1;
        }}
        .handle-line {{
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 4px;
            background-color: white;
            transform: translateX(-50%);
            z-index: 3;
            pointer-events: none;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }}
        .handle-circle {{
            width: 36px;
            height: 36px;
            background-color: white;
            border-radius: 50%;
            box-shadow: 0 2px 6px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #00A3E0; 
        }}
        .handle-circle::before, .handle-circle::after {{
            content: '';
            display: block;
            border-top: 6px solid transparent;
            border-bottom: 6px solid transparent;
        }}
        .handle-circle::before {{ border-right: 8px solid #1d4f91; margin-right: 3px; }} 
        .handle-circle::after {{ border-left: 8px solid #1d4f91; margin-left: 3px; }} 
        
        .invisible-slider {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: ew-resize;
            z-index: 4;
            margin: 0;
        }}
        .labels {{
            position: absolute;
            top: 10px;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 15px;
            box-sizing: border-box;
            z-index: 3;
            pointer-events: none;
        }}
        .label-tag {{
            background: rgba(29, 79, 145, 0.85); 
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 0.5px;
            border: 1px solid #00A3E0; 
        }}
    </style>
    </head>
    <body>
        <div class="slider-container">
            <img src="data:image/jpeg;base64,{img_simulated_b64}" class="img-layer" id="img-simulated">
            <img src="data:image/jpeg;base64,{img_normal_b64}" class="img-layer" id="img-normal">
            
            <div class="handle-line" id="handle">
                <div class="handle-circle"></div>
            </div>
            
            <div class="labels">
                <span class="label-tag">Normal</span>
                <span class="label-tag">{condition_name}</span>
            </div>

            <input type="range" min="0" max="100" value="50" class="invisible-slider" oninput="updateSlider(this.value)">
        </div>

        <script>
            function updateSlider(val) {{
                document.getElementById('img-normal').style.clipPath = `inset(0 ${{100 - val}}% 0 0)`;
                document.getElementById('handle').style.left = val + '%';
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

# ==========================================
# SIMULATION GRID
# ==========================================
st.header("Medical Eye Conditions")
st.markdown("<p style='text-align: center;'>Drag the sliders below to see the difference.</p><br>", unsafe_allow_html=True)

if uploaded_file:
    if uploaded_file.size > 10485760:
        st.error("⚠️ The uploaded file is larger than the 10MB limit. Please upload a smaller image.")
        st.stop()
    else:
        img = Image.open(uploaded_file).convert("RGB")
else:
    try:
        img = Image.open("sample_image.jpg").convert("RGB")
    except:
        # FAILSAFE: If no image is found, create a blank colorful canvas so the app doesn't crash
        img = Image.new('RGB', (800, 600), color='#1d4f91')

# Use a safe resize method that works across all versions of Python/Pillow
try:
    img.thumbnail((600, 600), Image.Resampling.LANCZOS)
except AttributeError:
    img.thumbnail((600, 600), Image.ANTIALIAS)

aspect_ratio = img.height / img.width
dynamic_container_height = int(350 * aspect_ratio)

# Expanded condition descriptions
descriptions = {
    "Glaucoma": "<b>The Condition:</b> Damage to the optic nerve, often linked to high eye pressure. It slowly steals peripheral (side) vision over time.<br><br><b>What's in the Image:</b> This creates a 'tunnel vision' effect, where the outer edges become dark and the world shrinks to a small central circle of sight.",
    "Macular Degeneration": "<b>The Condition:</b> Deterioration of the central portion of the retina, making reading, driving, and recognizing faces highly difficult.<br><br><b>What's in the Image:</b> A dark, blurred or empty spot is placed right in the center of the vision, while peripheral
