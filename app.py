import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. SETUP - Replace with your key from Google AI Studio
API_KEY = "AIzaSyBOw7hs_Vb65ILCD-LD7B2K5Egf1HEWzOQ"
genai.configure(api_key=API_KEY)
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
            # This prompt forces Gemini to follow your specific document structure
            full_prompt = f"""
            Create a detailed Daily Lesson Plan (DLP) for {topic}, Grade {grade_level}, Quarter {quarter}.
            Use the following EXACT format and headers based on the provided template:

            1. HEADER: Subject Area, Grade Level, Quarter, Date.
            2. CURRICULUM CONTENT: Content Standard, Performance Standard, Learning Competencies/Objectives.
            3. CONTENT: The specific topic title.
            4. INTEGRATION: Within (e.g., Math concepts) and Across (e.g., Science/Real-life).
            5. LEARNING RESOURCES: Teacher Guide, Learner Materials, Textbooks.
            6. TEACHING AND LEARNING PROCEDURE:
               - Activating Prior Knowledge (Minds and Moods)
               - Establishing Lesson Purpose (Aims/Unlocking Vocabulary)
               - Developing Understanding (Tasks and Thought/Explicitation)
               - Lesson Activity (Group work)
            7. MAKING GENERALIZATION: Abstract and Learner's Takeaways.
            8. EVALUATING LEARNING: A brief Assessment table/test.
            9. ASSIGNMENT: Real-life application task.
            10. REMARKS & REFLECTION: (Gains/Teacher's notes).
            11. SIGNATORIES: Prepared by: [Your Name], Checked by: [Name].
            """
            
            response = model.generate_content(full_prompt)
            lesson_text = response.text
            
            st.markdown("### Preview")
            st.write(lesson_text)

            # 3. CONVERT TO PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            
            # Clean text to avoid PDF errors with special characters
            clean_text = lesson_text.encode('latin-1', 'ignore').decode('latin-1')
            
            # Add content to PDF
            pdf.multi_cell(0, 8, clean_text)
            
            pdf_filename = f"Lesson_Plan_{topic.replace(' ', '_')}.pdf"
            pdf.output(pdf_filename)

            with open(pdf_filename, "rb") as file:
                st.download_button(
                    label="💾 Download as PDF",
                    data=file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
