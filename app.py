import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# 1. LOGIC & UTILITIES
def is_unacceptable(score, total_q=180):
    max_score = total_q * 4
    min_score = -total_q
    if score > max_score or score < min_score:
        return True
    
    # If no combination of Correct (C) and Incorrect (I) fits the score
    for c in range(total_q + 1):
        i = 4 * c - score
        if i >= 0 and (c + i) <= total_q:
            return False # It is acceptable
    return True # It is unacceptable

# 2. DATA & INTERPOLATION
marks = np.array([720, 716, 715, 712, 711, 710, 708, 707, 700, 690, 680, 675, 670, 665, 660, 655, 650, 640, 630, 620, 610, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50, 25, 10, 0])
ranks = np.array([1, 1, 7, 21, 26, 40, 56, 62, 216, 602, 1275, 1795, 2323, 2987, 3706, 4719, 5798, 8453, 11934, 16231, 21331, 27168, 66068, 121824, 192401, 277517, 378839, 497613, 636462, 806734, 1037373, 1396438, 1811969, 2019734, 2144394, 2227500])

log_ranks = np.log(ranks)
f_interp = interp1d(marks, log_ranks, kind='linear', fill_value="extrapolate")

# 3. PAGE CONFIG & UI
st.set_page_config(page_title="NEET 2026 Predictor", page_icon="🎓")
st.title("🎓 NEET 2026 Rank Predictor")

name = st.text_input("What your teachers call you?")
score = st.number_input("Your marks (0-720):", min_value=0, max_value=720, step=1)

# 4. PREDICTION LOGIC
if st.button("Predict Rank"):
    if not name:
        st.warning("Please enter a name first!")
    elif is_unacceptable(score):
        # CUSTOM ERROR MESSAGE
        st.error(f"⚠️ **{score} is an impossible score.**")
        st.info("""
            **Why?** In NEET, you get **+4** for correct and **-1** for incorrect. 
            Because every wrong answer drops your potential score by **5 points** (4 marks not gained + 1 mark deducted), 
            scores like **719, 718, 717, and 714** cannot be achieved mathematically.
        """)
    else:
        # Rank range calculation
        if score >= 716:
            result = "1 - 11"
        elif score == 715:
            result = "7 - 17"
        else:
            pred_rank = int(np.exp(f_interp(score)))
            lower = max(1, int(pred_rank * 0.95))
            upper = int(pred_rank * 1.05)
            result = f"{lower:,} - {upper:,}"

        st.success(f"Projected Rank for {name}: {result}")
