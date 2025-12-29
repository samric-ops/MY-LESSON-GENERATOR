import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="DLL/DLP Generator", page_icon="📋")

# ******************************************************
# PASTE YOUR NEW API KEY BELOW (Inside the quotes)
# ******************************************************
DIRECT_API_KEY = "AIzaSyC1UcmdhtoPqY2MIkFhncP07qDuocn5Db4"

# This forces the app to use YOUR pasted key, ignoring any old Secrets
genai.configure(api_key=DIRECT_API_KEY)

# We use the flash model because you have the new library (0.8.6)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. APP INTERFACE ---
st.title("📋 Daily Lesson Plan Generator")
st.write("Generate a lesson plan following the exact format of your Demo Daily Lesson Plan.")

topic = st.text_input("Enter the Subject Topic:", placeholder="e.g., Polynomial Equations")
grade_level = st.text_input("Grade Level:", value="10")
quarter = st.selectbox("Quarter:", ["1", "2", "3", "4"])

if st.button("Generate Lesson Plan"):
    if not topic:
        st.error("Please enter a topic first.")
    elif DIRECT_API_KEY == "PASTE_YOUR_NEW_KEY_HERE":
        st.error("🚨 You forgot to paste your new API Key in the code!")
    else:
        with st.spinner("Generating lesson plan..."):
            try:
                # 3. GENERATE CONTENT
                full_prompt = f"""
                Create a detailed Daily Lesson Plan (DLP) for {topic}, Grade {grade_level}, Quarter {quarter}.
                Use this EXACT format:
                I. OBJECTIVES
                II. CONTENT
                III. LEARNING RESOURCES
                IV. PROCEDURES
                V. REMARKS
                VI. REFLECTION
                """
                
                response = model.generate_content(full_prompt)
                lesson_text = response.text
                
                # Show Preview
                st.markdown("### Preview")
                st.write(lesson_text)

                # 4. CREATE PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                # Fix for special characters to prevent errors
                clean_text = lesson_text.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 6, clean_text)
                
                # Download Button
                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.download_button(
                    label="💾 Download PDF",
                    data=pdf_output,
                    file_name="Lesson_Plan.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error("❌ Error encountered")
                st.error(f"Details: {e}")
                st.info("If this says '404', your new API Key might not be active yet. Wait 2 minutes and try again.")
