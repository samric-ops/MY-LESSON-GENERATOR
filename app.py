import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- DIAGNOSTIC ---
# This confirms you are on the correct version (should be 0.8.6+)
st.write(f"🔍 Diagnostic: Google GenAI Version: {genai.__version__}")

# 1. SETUP
# ---------------------------------------------------------
# IMPORTANT: PASTE YOUR NEW API KEY BELOW inside the quotes
# ---------------------------------------------------------
try:
    # Try loading from secrets first
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # PASTE YOUR NEW KEY HERE REPLACE THE OLD ONE
    API_KEY = "AIzaSyC1UcmdhtoPqY2MIkFhncP07qDuocn5Db4" 

genai.configure(api_key=API_KEY)

# Now that you have library version 0.8.6, we use the specific modern model
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="DLL/DLP Generator", page_icon="📋")
st.title("📋 Daily Lesson Plan (DLP) Generator")
st.write("Generate a lesson plan following the exact format of your Demo Daily Lesson Plan.")

# 2. USER INPUT
topic = st.text_input("Enter the Subject Topic:", placeholder="e.g., Polynomial Equations")
grade_level = st.text_input("Grade Level:", value="10")
quarter = st.selectbox("Quarter:", ["1", "2", "3", "4"])

if st.button("Generate Lesson Plan"):
    if not topic:
        st.error("Please enter a topic first.")
    else:
        with st.spinner("Writing your lesson plan..."):
            try:
                full_prompt = f"""
                Create a detailed Daily Lesson Plan (DLP) for {topic}, Grade {grade_level}, Quarter {quarter}.
                Use the following EXACT format:
                1. HEADER: Subject Area, Grade Level, Quarter, Date.
                2. CURRICULUM CONTENT.
                3. CONTENT.
                4. INTEGRATION.
                5. LEARNING RESOURCES.
                6. TEACHING AND LEARNING PROCEDURE.
                7. MAKING GENERALIZATION.
                8. EVALUATING LEARNING.
                9. ASSIGNMENT.
                10. REMARKS & REFLECTION.
                11. SIGNATORIES.
                """
                
                response = model.generate_content(full_prompt)
                lesson_text = response.text
                
                st.markdown("### Preview")
                st.write(lesson_text)

                # 3. CONVERT TO PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                # Clean text to prevent crashes
                clean_text = lesson_text.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 8, clean_text)
                
                # Output to memory string (S) for Streamlit download
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="💾 Download as PDF",
                    data=pdf_output,
                    file_name="Lesson_Plan.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Double check that you replaced the API Key in the code with a NEW one from Google AI Studio.")
