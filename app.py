import streamlit as st
import numpy as np
from scipy.interpolate import interp1d
import urllib.parse

def is_unacceptable(score, total_q=180):
    max_score = total_q * 4
    min_score = -total_q
    
    if score > max_score or score < min_score:
        return "<unacceptable marks>"
    
    # Check if a valid combination of Correct (C) and Incorrect (I) exists
    # S = 4C - I  AND  C + I <= total_q
    for c in range(total_q + 1):
        i = 4 * c - score
        if i >= 0 and (c + i) <= total_q:
            return "<valid>"
            
    return "<unacceptable marks>"

# 1. Page Configuration
st.set_page_config(page_title="NEET 2026 Predictor", page_icon="🎓")

# 2. Data
marks = np.array([720, 716, 715, 712, 711, 710, 708, 707, 700, 690, 680, 675, 670, 665, 660, 655, 650, 640, 630, 620, 610, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50, 25, 10, 0])
ranks = np.array([1, 1, 7, 21, 26, 40, 56, 62, 216, 602, 1275, 1795, 2323, 2987, 3706, 4719, 5798, 8453, 11934, 16231, 21331, 27168, 66068, 121824, 192401, 277517, 378839, 497613, 636462, 806734, 1037373, 1396438, 1811969, 2019734, 2144394, 2227500])

log_ranks = np.log(ranks)
f_interp = interp1d(marks, log_ranks, kind='linear', fill_value="extrapolate")

# 3. UI Elements
st.title("🎓 NEET 2026 Rank Predictor")
st.write("Please provide the reactants (name) & reaction conditions (marks) to get the distillate (rank)!")

name = st.text_input("What your teachers call you?")
score = st.number_input("As per keys available, your marks in NEET exam (0-720):", min_value=0, max_value=720, step=1)

# 4. Logic Block (Everything indented exactly 4 spaces under the 'if')
if st.button("Predict Rank"):
    if not name:
        st.warning("Please enter a name first!")
    else:
        # Calculation logic
        if score >= 716:
            result = "1 - 11"
        elif score == 715:
            result = "7 - 17"
        else:
            pred_rank = int(np.exp(f_interp(score)))
            lower = max(1, int(pred_rank * 0.95))
            upper = int(pred_rank * 1.05)
            result = f"{lower} - {upper}"

        # Display result (This line should have 8 spaces in front)
        st.success(f"Projected Rank for {name}: {result}")
