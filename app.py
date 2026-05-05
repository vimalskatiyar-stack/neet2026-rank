# 4. PREDICTION & DOWNLOAD
if st.button("Predict Rank"):
    if not name:
        st.warning("Please enter a name first!")
    elif is_unacceptable(score):
        st.error(f"⚠️ **{score} is an impossible score.**")
        st.info("In NEET (+4/-1), scores like 719, 718, 717, and 714 cannot be achieved.")
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

        # 2. STYLE: Congratulations Logic
        if result_val < 25000:
            st.balloons()  # Adds a fun animation
            st.markdown(f"### 🎉 Congratulations, {name}!")
            st.write("You are currently in the range for a **Government Medical College (GMC)** seat. Keep up the momentum!")
        elif result_val < 50000:
            st.write("✨ **Great effort!** You have a strong chance for Semi-Government or top Private colleges.")

        # 3. GENERATE DOWNLOADABLE TEXT
        report_text = f"NEET 2026 Rank Prediction\n--------------------------\nName: {name}\nMarks: {score}\nPredicted Rank: {result}"
        
        st.download_button(
            label="💾 Download Result",
            data=report_text,
            file_name=f"{name}_NEET_Prediction.txt",
            mime="text/plain"
        )
