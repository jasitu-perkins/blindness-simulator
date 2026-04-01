import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from streamlit_image_comparison import image_comparison

# 1. Set up the web page title and layout
st.set_page_config(page_title="What Blindness Really Looks Like", layout="centered")

st.title("👁️ What Blindness Really Looks Like")
st.write("Inspired by the Perkins School for the Blind. Use the swipe slider below to compare normal vision with different visual impairments.")

# 2. Define our image processing functions based on the Perkins reference
def apply_glaucoma(img):
    """Glaucoma: Creates a pinhole view with darkened/blurred surroundings."""
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 3
    center_x, center_y = width // 2, height // 2
    
    # Draw the clear central area
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    # Blur the edges heavily
    mask = mask.filter(ImageFilter.GaussianBlur(radius=80))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask)

def apply_macular_degeneration(img):
    """Macular Degeneration: Creates a dark cloud obscuring the middle of the scene."""
    img_copy = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    radius = min(width, height) // 4
    center_x, center_y = width // 2, height // 2
    
    # Draw the central blind spot
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    # Blur the spot so it looks like a cloud
    mask = mask.filter(ImageFilter.GaussianBlur(radius=50))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    # Composite the black image OVER the original image using the mask
    return Image.composite(black_img, img_copy, mask)

def apply_achromatopsia(img):
    """Achromatopsia: Complete absence of color vision (black and white)."""
    # Convert to grayscale, then back to RGB so it plays nicely with the comparison tool
    return img.convert('L').convert('RGB')

def apply_low_vision(img):
    """Low Vision: A dim and blurry scene."""
    # First, blur the image
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=10))
    # Then, reduce the brightness
    enhancer = ImageEnhance.Brightness(img_blur)
    return enhancer.enhance(0.5)

def apply_lower_field_loss(img):
    """CVI (Field Loss): Cannot see below eye level."""
    mask = Image.new('L', img.size, 255)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    
    # Draw a black rectangle over the bottom half
    draw.rectangle((0, height // 2, width, height), fill=0)
    # Soften the horizontal line slightly
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(img, black_img, mask)

# 3. Load the original image
try:
    original_image = Image.open("sample_image.jpg")
except FileNotFoundError:
    st.error("Please place an image named 'sample_image.jpg' in the same folder as this script!")
    st.stop()

# 4. User Interface Control
condition = st.selectbox(
    "Select an eye condition to simulate (Based on Perkins School examples):",
    ("Glaucoma", "Macular Degeneration", "Achromatopsia", "Low Vision", "Lower Field Loss (CVI)")
)

# 5. Apply the chosen effect
if condition == "Glaucoma":
    processed_image = apply_glaucoma(original_image)
elif condition == "Macular Degeneration":
    processed_image = apply_macular_degeneration(original_image)
elif condition == "Achromatopsia":
    processed_image = apply_achromatopsia(original_image)
elif condition == "Low Vision":
    processed_image = apply_low_vision(original_image)
elif condition == "Lower Field Loss (CVI)":
    processed_image = apply_lower_field_loss(original_image)

# 6. Display the interactive swipe comparison
st.write("---")
st.write("**Drag the slider left and right to compare:**")
image_comparison(
    img1=original_image,
    img2=processed_image,
    label1="Normal Vision",
    label2=condition,
    starting_position=50, # Starts the slider exactly in the middle
    make_responsive=True
)