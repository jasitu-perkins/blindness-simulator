import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from streamlit_image_comparison import image_comparison

# 1. Set up the web page title and layout
st.set_page_config(page_title="What Blindness Really Looks Like", layout="centered")

st.title("👁️ What Blindness Really Looks Like")
st.write("Inspired by the Perkins School for the Blind. Scroll down to explore how different visual impairments affect sight. Drag the slider on each image to compare it with normal vision.")
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

# 4. Create the educational layout for multiple examples

# --- Example 1: Glaucoma ---
st.subheader("1. Glaucoma")
st.markdown("""
* **The Condition:** Glaucoma is a group of eye conditions that damage the optic nerve, which is crucial for good vision. This damage is often caused by an abnormally high pressure in your eye. It typically develops slowly over time, and the first sign is usually the loss of peripheral (side) vision. 
* **What's in the Image:** The code creates a "tunnel vision" effect. The center of the image remains clear, but the outer edges are heavily darkened and blurred out. This shows how someone might be able to read a book right in front of them but completely miss a person walking past them on the side.
""")
image_comparison(
    img1=original_image,
    img2=apply_glaucoma(original_image),
    label1="Normal Vision",
    label2="Glaucoma",
    starting_position=50
)
st.divider()

# --- Example 2: Macular Degeneration ---
st.subheader("2. Macular Degeneration")
st.markdown("""
* **The Condition:** This condition occurs when the small central portion of the retina, known as the macula, deteriorates. The retina is the light-sensing nerve tissue at the back of the eye. Because the disease affects the center of the visual field, it makes reading, driving, and recognizing faces very difficult.
* **What's in the Image:** The code applies a dark, blurry "cloud" directly over the center of the image. Unlike Glaucoma, the peripheral edges of the image remain completely clear. This demonstrates how a person might be able to navigate a room using their side vision but struggle to focus on the face of someone standing directly in front of them.
""")
image_comparison(
    img1=original_image,
    img2=apply_macular_degeneration(original_image),
    label1="Normal Vision",
    label2="Macular Degeneration",
    starting_position=50
)
st.divider()

# --- Example 3: Achromatopsia ---
st.subheader("3. Achromatopsia")
st.markdown("""
* **The Condition:** Achromatopsia is a rare, inherited vision disorder where a person has a partial or total absence of color vision. People with complete achromatopsia lack functioning cone cells (the cells in the eye responsible for color) and must rely entirely on rod cells, which only process black, white, and shades of gray.
* **What's in the Image:** The code strips away all color data and converts the image to grayscale. This leaves a purely black-and-white image, allowing the user to experience what a scene looks like when the eyes cannot detect any color wavelengths.
""")
image_comparison(
    img1=original_image,
    img2=apply_achromatopsia(original_image),
    label1="Normal Vision",
    label2="Achromatopsia",
    starting_position=50
)
st.divider()

# --- Example 4: Low Vision ---
st.subheader("4. Low Vision")
st.markdown("""
* **The Condition:** "Low vision" is a broad term used to describe a significant visual impairment that cannot be fully corrected with standard glasses, contact lenses, medication, or surgery. It can be caused by various eye diseases or injuries and often results in a severe loss of visual acuity (sharpness).
* **What's in the Image:** The code applies a heavy, uniform blur across the entire image and significantly reduces the brightness. This simulates the hazy, dim, and unfocused world that many individuals with low vision experience on a daily basis.
""")
image_comparison(
    img1=original_image,
    img2=apply_low_vision(original_image),
    label1="Normal Vision",
    label2="Low Vision",
    starting_position=50
)
st.divider()

# --- Example 5: Cortical/Cerebral Visual Impairment (CVI) ---
st.subheader("5. Cortical/Cerebral Visual Impairment (Lower Field Loss)")
st.markdown("""
* **The Condition:** Unlike the other conditions, CVI is a brain-based visual impairment. The eyes themselves might function perfectly, but the visual processing centers in the brain cannot properly interpret the signals. CVI can manifest in many different ways, but one common presentation is "field loss," where the brain entirely ignores a specific portion of the visual field. 
* **What's in the Image:** The code simulates a complete lower visual field loss. The top half of the image remains visible, but the entire bottom half is blacked out. This demonstrates why a person with this specific type of CVI might frequently trip over objects on the floor or struggle to walk down a flight of stairs, even if their eyes are technically healthy.
""")
image_comparison(
    img1=original_image,
    img2=apply_lower_field_loss(original_image),
    label1="Normal Vision",
    label2="Lower Field Loss",
    starting_position=50
)
