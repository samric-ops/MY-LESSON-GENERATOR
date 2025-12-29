import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. SETUP 
# We use st.secrets for security. I will show you how to set this up below.
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Fallback for local testing if secrets aren't set
    API_KEY = "AIzaSyC1UcmdhtoPqY2MIkFhncP07qDuocn5Db4" 

genai.configure(api_key=API_KEY)

# Change from 'gemini-1.5-flash' to 'gemini-1.5-flash-latest'
model = genai.GenerativeModel('gemini-1.5-flash-latest') 
# just in case the model isn't responding.
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
                Use the following EXACT format and headers:

                1. HEADER: Subject Area, Grade Level, Quarter, Date.
                2. CURRICULUM CONTENT: Content Standard, Performance Standard, Learning Competencies/Objectives.
                3. CONTENT: The specific topic title.
                4. INTEGRATION: Within and Across.
                5. LEARNING RESOURCES: Teacher Guide, Learner Materials.
                6. TEACHING AND LEARNING PROCEDURE:
                   - Activating Prior Knowledge
                   - Establishing Lesson Purpose
                   - Developing Understanding
                   - Lesson Activity
                7. MAKING GENERALIZATION.
                8. EVALUATING LEARNING.
                9. ASSIGNMENT.
                10. REMARKS & REFLECTION.
                11. SIGNATORIES.
                """
                
                response = model.generate_content(full_prompt)
                lesson_text = response.text
                
                st.markdown("### Preview")
                st.info("Lesson generated successfully!")
                st.write(lesson_text)

                # 3. CONVERT TO PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                
                # Clean text: remove characters that FPDF doesn't support
                clean_text = lesson_text.encode('latin-1', 'ignore').decode('latin-1')
                
                # Add content to PDF
                pdf.multi_cell(0, 8, clean_text)
                
                pdf_filename = f"Lesson_Plan_{topic.replace(' ', '_')}.pdf"
                pdf_output = pdf.output(dest='S').encode('latin-1') # Stream to memory

                st.download_button(
                    label="💾 Download as PDF",
                    data=pdf_output,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Try checking if your API Key is active in Google AI Studio.")
