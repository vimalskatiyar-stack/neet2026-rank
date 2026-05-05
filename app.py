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

# 2. DATA
marks = np.array([720, 716, 715, 710, 700, 650, 600, 500, 400, 300, 200, 100, 0])
ranks = np.array([1, 1, 7, 40, 216, 5798, 27168, 121824, 277517, 497613, 806734, 1396438, 2227500])

f_interp = interp1d(marks, np.log(ranks), kind='linear', fill_value="extrapolate")

# 3. UI CONFIG
st.set_page_config(page_title="NEET 2026 Predictor", page_icon="🎓")
st.title("🎓 NEET 2026 Rank Predictor")
st.write("Please provide the reactants (name) & reaction conditions (marks) to get the distillate (rank)!")

name = st.text_input("What your teachers call you?")
score = st.number_input("Your marks (0-720):", min_value=0, max_value=720, step=1)

# 4. PREDICTION & DOWNLOAD
if st.button("Predict Rank"):
    if not name:
        st.warning("Please enter a name first!")
    elif is_unacceptable(score):
        # CUSTOM ERROR MESSAGE
        st.error(f"⚠️ **{score} is an impossible score. You must re-check your calculations. Use calculator if needed, and come back here again to proceed. Thanks.**")
        st.info("""
            **Why?** In NEET, you get **+4** for correct and **-1** for incorrect. 
            Because every wrong answer drops your potential score by **5 points** (4 marks not gained + 1 mark deducted), 
            scores like **719, 718, 717, and 714** cannot be achieved mathematically.
        """)
    else:

        # Rank Logic
        if score >= 716: 
            result_val = 1
            result = "1 - 11"
        elif score == 715: 
            result_val = 7
            result = "7 - 17"
        else:
            result_val = int(np.exp(f_interp(score)))
            result = f"{int(result_val * 0.95):,} - {int(result_val * 1.05):,}"

        # 1. STYLE: Result Display
        st.success(f"### Projected Rank for {name}: **{result}**")

        # 2. STYLE: Congratulations Logic (NOW PROPERLY INDENTED)
        if result_val <= 50:
            st.balloons()
            st.markdown(f"### 🏆 Elite Achievement, {name}!")
            st.write("You are in the top tier! You ARE going to **AIIMS New Delhi!!**")
        elif result_val <= 1000:
            st.balloons()
            st.markdown(f"### 🎉 Outstanding Rank, {name}!")
            st.write("Strong chance for **MAMC Delhi, VMMC Delhi, JIPMER Pondicherry, or other best rated second generation AIIMS!**")
        elif result_val <= 10000:
            st.balloons()
            st.markdown(f"### 🎉 Wonderful Rank, {name}!")
            st.write("You are likely eligible for **Top-Rated State Medical Colleges**.")
        elif result_val <= 27000:
            st.snow()
            st.markdown(f"### 🎊 Congratulations, {name}!")
            st.write("You are in the range for a **Government Medical College (GMC)** seat via AIQ.")
        elif result_val <= 40000:
            st.write(f"✨ **Well done, {name}!**")
            st.write("Strong chance for Newer Government Colleges or Semi-Gov institutions.")
        elif result_val <= 100000:
            st.write(f"👍 **Good Effort, {name}!**")
            st.write("Eligible for reputed Private Colleges, BDS, or BAMS.")
        else:
            st.write(f"📚 **Keep Pushing, {name}!**")
            st.write("Focus on your next steps. You may qualify for private or allied fields.")

        # 3. GENERATE DOWNLOADABLE TEXT (NOW PROPERLY INDENTED)
        report_text = f"NEET 2026 Rank Prediction\n--------------------------\nName: {name}\nMarks: {score}\nPredicted Rank: {result}"
        
        st.download_button(
            label="💾 Download Result",
            data=report_text,
            file_name=f"{name}_NEET_Prediction.txt",
            mime="text/plain"
        )
