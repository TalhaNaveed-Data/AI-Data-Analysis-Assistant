import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="AI Data Analyst", page_icon="📊")

st.title("📊 AI Data Analysis Assistant")
st.markdown("Upload your Excel/CSV file - AI will analyze it for you!")

with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Apni Gemini API Key:", type="password")
    st.markdown("[Yahan se key lo](https://aistudio.google.com/app/apikey)")

uploaded_file = st.file_uploader("📁 Apni Excel/CSV file upload karo", type=["xlsx", "csv"])

if uploaded_file and api_key:
    # File read karo
    if uploaded_file.name.endswith('csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())
    
    # File ki information
    st.info(f"Rows: {len(df)} | Columns: {len(df.columns)}")
    
    # AI se analysis
    if st.button("🤖 AI Se Analysis Karwao"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Mera data analysis karo. Meri file mein {len(df)} rows aur {len(df.columns)} columns hain.
        Columns ye hain: {list(df.columns)}
        
        Mujhe batao:
        1. Is data mein kya trends hain?
        2. Kya koi interesting patterns hain?
        3. 3 practical insights do jo business ke liye useful ho
        
        Simple language mein batao.
        """
        
        with st.spinner("AI analysis kar raha hai..."):
            response = model.generate_content(prompt)
            st.subheader("🤖 AI Insights")
            st.write(response.text)

elif uploaded_file and not api_key:
    st.error("❌ Pehle sidebar mein API key dalo")

else:
    st.info("👈 Sidebar mein API key dalo aur file upload karo")