import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from streamlit_image_comparison import image_comparison

# 1. Set up the web page title and layout (Changed to "wide")
st.set_page_config(page_title="What Blindness Really Looks Like", layout="wide")

st.title("👁️ What Blindness Really Looks Like")
st.write("Inspired by the Perkins School for the Blind. Drag the slider on each image below to compare different visual impairments with normal vision.")
st.divider()

# 2. Define our image processing functions
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

def apply_achromatopsia(img):
    return img.convert('L').convert('RGB')

def apply_low_vision(img):
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=10))
    enhancer = ImageEnhance.Brightness(img_blur)
    return enhancer.enhance(0.5)

def apply_lower_field_loss(img):
    mask = Image.new('L', img.size, 255)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    
    draw.rectangle((0, height // 2, width, height), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask)

# 3. Load the original image
try:
    original_image = Image.open("sample_image.jpg")
except FileNotFoundError:
    st.error("Please place an image named 'sample_image.jpg' in the same folder as this script!")
    st.stop()

# 4. Create a 5-column layout to fit everything on one screen
col1, col2, col3, col4, col5 = st.columns(5)

# --- Example 1: Glaucoma ---
with col1:
    st.markdown("**1. Glaucoma**")
    st.caption("Damages the optic nerve, resulting in 'tunnel vision' and loss of peripheral sight.")
    image_comparison(
        img1=original_image,
        img2=apply_glaucoma(original_image),
        label1="Normal",
        label2="Glaucoma",
        starting_position=50
    )

# --- Example 2: Macular Degeneration ---
with col2:
    st.markdown("**2. Macular Degen.**")
    st.caption("Deteriorates the retina's center, creating a dark, blurry blind spot in the middle.")
    image_comparison(
        img1=original_image,
        img2=apply_macular_degeneration(original_image),
        label1="Normal",
        label2="Macular",
        starting_position=50
    )

# --- Example 3: Achromatopsia ---
with col3:
    st.markdown("**3. Achromatopsia**")
    st.caption("A rare condition causing a partial or total absence of all color vision.")
    image_comparison(
        img1=original_image,
        img2=apply_achromatopsia(original_image),
        label1="Normal",
        label2="Achromatopsia",
        starting_position=50
    )

# --- Example 4: Low Vision ---
with col4:
    st.markdown("**4. Low Vision**")
    st.caption("Severe loss of sharpness causing a heavily blurred and dimmed view.")
    image_comparison(
        img1=original_image,
        img2=apply_low_vision(original_image),
        label1="Normal",
        label2="Low Vision",
        starting_position=50
    )

# --- Example 5: Cortical/Cerebral Visual Impairment (CVI) ---
with col5:
    st.markdown("**5. Lower Field Loss**")
    st.caption("A brain-based impairment where the lower half of the visual field is ignored.")
    image_comparison(
        img1=original_image,
        img2=apply_lower_field_loss(original_image),
        label1="Normal",
        label2="CVI",
        starting_position=50
    )
