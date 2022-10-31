import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
import json

drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", )
)
stroke_width = st.sidebar.slider("Stroke width: ", 1, 50, 3)
input_path = st.text_input('input_path', value=None)
output_path = st.text_input('output_path', value=None)
input_mask = Image.open(input_path) if input_path != 'None' else None

if input_mask is not None:
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1.)",
        stroke_width=stroke_width,
        height = input_mask.size[1],
        width = input_mask.size[0],
        background_image = input_mask,
        drawing_mode=drawing_mode,
        key="canvas",
    )

save_mask_state = st.sidebar.button("save")

if save_mask_state:
    mask = np.array(Image.fromarray(canvas_result.image_data[:,:,-1]))
    original_mask = np.array(input_mask)
    mask = 255 - np.array(mask)
    mask = original_mask * (mask / 255)
    mask[mask != 0] = 255
    Image.fromarray(mask.astype(np.uint8)).save(output_path)
    save_mask_state = None
