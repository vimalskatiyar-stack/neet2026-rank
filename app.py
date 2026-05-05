import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# 1. LOGIC & UTILITIES
def is_unacceptable(score, total_q=180):
    max_score, min_score = total_q * 4, -total_q
    if score > max_score or score < min_score:
        return True
    for c in range(total_q + 1):
        i = 4 * c - score
        if i >= 0 and (c + i) <= total_q:
            return False
    return True

# 2. DATA (Ensure arrays are populated with your rank data)
marks = np.array([720, 716, 715, 710, 700, 650, 600, 500, 400, 300, 200, 100, 0])
ranks = np.array([1, 1, 7, 40, 216, 5798, 27168, 121824, 277517, 497613, 806734, 1396438, 2227500])

f_interp = interp1d(marks, np.log(ranks), kind='linear', fill_value="extrapolate")

# 3. UI CONFIG
st.set_page_config(page_title="NEET 2026 Predictor", page_icon="🎓")
st.title("🎓 NEET 2026 Rank Predictor")

name = st.text_input("What your teachers call you?")
score = st.number_input("Your marks (0-720):", min_value=0, max_value=720, step=1)

# 4. PREDICTION & DOWNLOAD
if st.button("Predict Rank"):
    if not name:
        st.warning("Please enter a name first!")
    elif is_unacceptable(score):
        st.error(f"⚠️ **{score} is an impossible score. You must re-check your calculations. Use calculator if needed, and come back here again to proceed. Thanks.**")
        st.info("In NEET (+4/-1), scores like 719, 718, 717, and 714 cannot be achieved.")
    else:
        # Rank Logic
        if score >= 716: result = "1 - 11"
        elif score == 715: result = "7 - 17"
        else:
            pred_rank = int(np.exp(f_interp(score)))
            result = f"{int(pred_rank * 0.95):,} - {int(pred_rank * 1.05):,}"

        # Display Result
        st.success(f"Projected Rank for {name}: {result}")

        # GENERATE DOWNLOADABLE TEXT
        report_text = f"NEET 2026 Rank Prediction\n--------------------------\nName: {name}\nMarks: {score}\nPredicted Rank: {result}"
        
        st.download_button(
            label="💾 Download Result as Text",
            data=report_text,
            file_name=f"{name}_NEET_Prediction.txt",
            mime="text/plain"
        )
