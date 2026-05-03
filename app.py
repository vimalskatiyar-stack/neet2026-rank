import streamlit as st

st.set_page_config(
    page_title="NEET 2026 Predictor",
    page_icon="🎓", # Can be an emoji or an image URL
    layout="centered"
)
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://drive.google.com/file/d/1yxBJ1RG_nZIcyV886FssI-QaVpN7DfZd/view?usp=sharing");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
[theme]
primaryColor = "#007bff"     # The color of your buttons
backgroundColor = "#ffffff"  # Main background color (if no image)
secondaryBackgroundColor = "#f0f2f6" # Color of the input boxes
textColor = "#31333F"        # Main text color
font = "sans serif"
add_bg_from_url()
import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# Data
marks = np.array([720, 716, 715, 712, 711, 710, 708, 707, 700, 690, 680, 675, 670, 665, 660, 655, 650, 640, 630, 620, 610, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50, 25, 10, 0])
ranks = np.array([1, 1, 7, 21, 26, 40, 56, 62, 216, 602, 1275, 1795, 2323, 2987, 3706, 4719, 5798, 8453, 11934, 16231, 21331, 27168, 66068, 121824, 192401, 277517, 378839, 497613, 636462, 806734, 1037373, 1396438, 1811969, 2019734, 2144394, 2227500])

log_ranks = np.log(ranks)
f_interp = interp1d(marks, log_ranks, kind='linear', fill_value="extrapolate")

st.title("--- NEET 2026 Rank Predictor ---")

name = st.text_input("Enter candidate's name:")
score = st.number_input("Enter your NEET marks (0-720):", min_value=0, max_value=720, step=1)

if st.button("Predict Rank"):
    if score >= 716:
        result = "1 - 11"
    elif score == 715:
        result = "7 - 17"
    else:
        pred_rank = int(np.exp(f_interp(score)))
        result = f"{max(1, int(pred_rank * 0.95))} - {int(pred_rank * 1.05)}"

    st.success(f"Projected Rank for {name}: {result}")
    
    # WhatsApp Share Link
    share_text = f"{name}'s projected NEET 2026 Rank for {score} marks is {result}."
    st.link_button("Share on WhatsApp", f"https://wa.me{share_text}")
