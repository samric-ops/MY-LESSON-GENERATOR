import streamlit as st
import google.generativeai as genai

st.title("🔑 API Key & Model Tester")

# 1. SETUP - Replace this with your NEW Key
# Do NOT use the old key that you posted earlier. It is likely blocked.
MY_API_KEY = "AIzaSyC1UcmdhtoPqY2MIkFhncP07qDuocn5Db4"

genai.configure(api_key=MY_API_KEY)

if st.button("Test My API Key"):
    try:
        st.write(f"Using Library Version: {genai.__version__}")
        st.write("Attempting to connect to Google...")
        
        # This asks Google: "What models can I use?"
        models = genai.list_models()
        
        found_any = False
        st.write("### ✅ Success! Here are the models your Key can access:")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name) # This will print the EXACT name you need to use
                found_any = True
        
        if not found_any:
            st.error("Connection successful, but no models found. Your project might have restrictions.")
            
    except Exception as e:
        st.error("❌ CONNECTION FAILED")
        st.error(f"Error details: {e}")
        st.warning("If you see a 404 or 403 error above, your API Key is invalid.")
