import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from streamlit_image_comparison import image_comparison
import random

# 1. Set up the web page title and layout
st.set_page_config(page_title="What Blindness Really Looks Like", layout="centered")

st.title("👁️ What Blindness Really Looks Like")
st.write("Inspired by the Perkins School for the Blind. Scroll down to explore how different visual impairments affect sight. Drag the slider on each image to compare it with normal vision.")

uploaded_file = st.file_uploader("Upload your own image to test (or we'll use the default):", type=["jpg", "jpeg", "png"])
st.divider()

# OPTIMIZATION STEP 1: Resize the image before doing any heavy math
def resize_for_performance(img, max_width=800):
    """Resizes the image if it is too large, drastically speeding up processing."""
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        # Resize using a high-quality downsampling filter
        return img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return img

# OPTIMIZATION STEP 2: Add @st.cache_data to memorize processed images
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
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=4))
    yellow_tint = Image.new('RGB', img.size, (255, 240, 200))
    return Image.blend(img_blur, yellow_tint, alpha=0.2)

@st.cache_data
def apply_diabetic_retinopathy(img):
    img_copy = img.copy()
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    
    random.seed(42) 
    for _ in range(12):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(20, min(width, height) // 8)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
        
    mask = mask.filter(ImageFilter.GaussianBlur(radius=15))
    black_img = Image.new('RGB', img.size, (0, 0, 0))
    return Image.composite(black_img, img_copy, mask)

@st.cache_data
def apply_lower_field_loss(img):
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

# Apply our new resizing function here
original_image = resize_for_performance(raw_image)

# 4. Educational Layout & Render

# --- Example 1: Glaucoma ---
st.subheader("1. Glaucoma")
st.markdown("""
* **The Condition:** Glaucoma is a group of eye conditions that damage the optic nerve, which is crucial for good vision. This damage is often caused by an abnormally high pressure in your eye. It typically develops slowly over time, and the first sign is usually the loss of peripheral (side) vision. 
* **What's in the Image:** The code creates a "tunnel vision" effect. The center of the image remains clear, but the outer edges are heavily darkened and blurred out.
""")
image_comparison(original_image, apply_glaucoma(original_image), label1="Normal", label2="Glaucoma", starting_position=50)
st.divider()

# --- Example 2: Macular Degeneration ---
st.subheader("2. Macular Degeneration")
st.markdown("""
* **The Condition:** Occurs when the small central portion of the retina (the macula) deteriorates. Because the disease affects the center of the visual field, it makes reading, driving, and recognizing faces very difficult.
* **What's in the Image:** A dark, blurry "cloud" is applied directly over the center of the image, while peripheral edges remain clear.
""")
image_comparison(original_image, apply_macular_degeneration(original_image), label1="Normal", label2="Macular Degen.", starting_position=50)
st.divider()

# --- Example 3: Cataracts ---
st.subheader("3. Cataracts")
st.markdown("""
* **The Condition:** A cataract is a clouding of the normally clear lens of the eye. For people who have cataracts, seeing through cloudy lenses is a bit like looking through a frosty or fogged-up window. As it progresses, it can also add a brownish or yellowish tint to vision.
* **What's in the Image:** The entire image is slightly blurred to simulate the cloudy lens, and a warm, yellow-brown tint is blended in to demonstrate the color distortion.
""")
image_comparison(original_image, apply_cataracts(original_image), label1="Normal", label2="Cataracts", starting_position=50)
st.divider()

# --- Example 4: Diabetic Retinopathy ---
st.subheader("4. Diabetic Retinopathy")
st.markdown("""
* **The Condition:** A diabetes complication that affects eyes. It's caused by damage to the blood vessels of the light-sensitive tissue at the back of the eye (retina). It can cause dark spots or "floaters" to appear in the person's vision.
* **What's in the Image:** The code generates random, blurry, dark splotches across the field of view, simulating the patchy vision loss caused by internal bleeding and damaged tissue.
""")
image_comparison(original_image, apply_diabetic_retinopathy(original_image), label1="Normal", label2="Diabetic Retin.", starting_position=50)
st.divider()

# --- Example 5: Low Vision ---
st.subheader("5. Low Vision")
st.markdown("""
* **The Condition:** A broad term for significant visual impairment that cannot be fully corrected. It often results in a severe loss of visual acuity (sharpness).
* **What's in the Image:** A heavy, uniform blur is applied across the entire image and brightness is reduced, simulating a hazy, unfocused world.
""")
image_comparison(original_image, apply_low_vision(original_image), label1="Normal", label2="Low Vision", starting_position=50)
st.divider()


# =========================================================
# DEDICATED CVI SECTION
# =========================================================
st.header("🧠 Cortical/Cerebral Visual Impairment (CVI)")
st.markdown("""
**Understanding CVI:** Unlike the eye conditions listed above, CVI is a **brain-based** visual impairment. The eyes themselves might function perfectly and capture light, but the visual processing centers in the brain cannot properly interpret the signals. 

CVI often manifests uniquely in each person. Common traits include needing movement to see an object, intense preference for a specific color, difficulty processing visual complexity (like a crowded room), or ignoring specific sections of the visual field.
""")

st.subheader("Example A: Lower Field Loss")
st.markdown("""
* **The Condition:** The brain entirely ignores visual data coming from a specific portion of the visual field (commonly the lower half). 
* **What's in the Image:** The code simulates a complete blackout of the lower field. This demonstrates why a person with this specific type of CVI might frequently trip over objects on the floor or struggle with stairs, even if their eyes are technically healthy. Try uploading a picture of a cluttered floor or a sidewalk to see how this impacts navigation!
""")
image_comparison(original_image, apply_lower_field_loss(original_image), label1="Normal", label2="Field Loss", starting_position=50)
