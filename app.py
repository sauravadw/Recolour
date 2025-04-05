import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import io

st.set_page_config(page_title="Pandora Sprayer Recolor Tool", layout="centered")

st.title("Pandora Sprayer Recolor Tool")

uploaded_file = st.file_uploader("Upload an image of the sprayer", type=["jpg", "jpeg", "png"])

body_color = st.color_picker("Select Body Color", "#7ac6c3")
cap_color = st.color_picker("Select Cap & Base Color", "#fe3f0b")

def replace_color(image, mask_range, new_color):
    img = image.convert("RGBA")
    data = np.array(img)

    r, g, b = data[..., 0], data[..., 1], data[..., 2]

    # Create a simple mask (based on value ranges, can be improved with real masking)
    mask = (
        (r > mask_range[0][0]) & (r < mask_range[1][0]) &
        (g > mask_range[0][1]) & (g < mask_range[1][1]) &
        (b > mask_range[0][2]) & (b < mask_range[1][2])
    )

    data[..., :3][mask] = new_color  # Replace only masked region

    return Image.fromarray(data)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    st.image(image, caption="Original Image", use_column_width=True)

    # Define ranges manually (ideally replace this with a real mask if possible)
    # First range is for body, second for caps & base
    body_range = [(60, 60, 60), (180, 180, 180)]
    cap_range = [(10, 10, 10), (80, 80, 80)]

    new_body = tuple(int(body_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    new_cap = tuple(int(cap_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    recolored = replace_color(image, body_range, new_body)
    recolored = replace_color(recolored, cap_range, new_cap)

    st.image(recolored, caption="Recolored Image", use_column_width=True)

    # Download
    img_bytes = io.BytesIO()
    recolored.save(img_bytes, format="PNG")
    st.download_button("Download Recolored Image", data=img_bytes.getvalue(), file_name="recolored_sprayer.png", mime="image/png")
