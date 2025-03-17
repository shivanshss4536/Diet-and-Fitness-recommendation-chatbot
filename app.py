# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import google.generativeai as genai
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import re

st.set_page_config(layout="wide", page_icon="🏋️", page_title="Personalized Diet & Fitness")

if 'page' not in st.session_state:
    st.session_state.page = 'input'

os.environ["GOOGLE_API_KEY"] = 'AIzaSyBGKnyD4gAXmoeXT61bikW-wkQ4SRr3yU4'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-pro')

def generate_recommendations(user_data):
    prompt = f""" 
    Diet and Exercise Recommendation System:
    Suggest 6 types of home workouts with detailed instructions,
    6 breakfast ideas with nutritional information,
    5 dinner options with nutritional information, 
    and 6 gym workout plans for each day of the week.
    Full Name: {user_data['full_name']}
    Age: {user_data['age_group']}
    Gender: {user_data['gender_identity']}
    Weight: {user_data['body_weight']}
    Height: {user_data['height_in_cm']}
    Diet Preference: {user_data['diet_preference']}
    Allergic Reactions: {user_data['allergic_reactions']}
    """
    response = model.generate_content(prompt)
    return response.text

def set_css():
    st.markdown("""
        <style>
            #myVideo {
                     position: fixed;       /* Fixed to the viewport */
                     top: 0;                /* Align at the top */
                     left: 0;               /* Align at the left */
                     width: 99.3%;           /* Full viewport width */
                     height: 100%;          /* Full viewport height */
                     object-fit: fill;     /* Cover the container without distortion */
                     z-index: 0;            /* Keep the video behind your content */
                   }
            
            .content {
                     width: 99.3%;
                      height: -webkit-fill-available;
                      position: fixed;
                      top: 0;
                      left: 0;
                      right: 0;
                      bottom: 0;          /* Cover the entire viewport */
                      overflow-y: auto;   /* Allow scrolling if content overflows */
                      background: rgba(0, 0, 0, 0.7);  /* Semi-transparent overlay */
                      color: #f1f1f1;
                      padding: 30px;      /* Adjust as needed */
                      box-sizing: border-box;  /* Ensure padding is included in the width/height */
                      z-index: 0;         /* Place content above the video */
              }
            #recommendation_box {
                width: 90%;
                margin: 5% auto;
                animation: fadeIn 1.5s ease-in-out;
                text-align: center;
                background-color: #F0A04B;
            }
            #recommendation_box .stButton>button {
                
                margin: 0 auto;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            ::-webkit-scrollbar {
                width: 18px;
                height: 18px;
                z_index: 1;
            }
            ::-webkit-scrollbar-track {
                background: #222; 
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #f39c12, #e67e22);
                border-radius: 10px;
                border: 2px solid #222;
            }
            * {
                z_index: -1;
                scrollbar-width: thin;
                scrollbar-color: #f39c12 #222;
            }
            h1, h2, h3 {
                color: #f39c12;
                text-align: center;
            }
            .stButton>button {
                background-color: #f39c12 !important;
                color: white !important;
                border-radius: 8px;
                font-size: 1.1rem;
                padding: 10px 20px;
                transition: background-color 0.3s ease;
            }
                .st-emotion-cache-sh2krr p {
                      word-break: break-word;
                     margin-bottom: 0px;
                      font-size: 18px;
                 }
            .stButton>button:hover {
                background-color: #e67e22 !important;
            }
            .stTextInput>div>div>input, .stSelectbox>div>div>select {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 8px;
                border: 1px solid #f39c12;
                padding: 10px;
                font-size: 1rem;
            }
            .stTextInput>div>div>input::placeholder {
                color: #ddd;
            }
            @media (max-width: 768px) {
                .content { 
                    top: 0;
                    left: 0;
                    height: -webkit-fill-available;
                    width: -webkit-fill-available;
                    position: fixed;
                    background: rgba(0, 0, 0, 0.7);
                    color: #f1f1f1;
                    border-radius: 8px;
                    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
                    overflow-y: scroll !important;
                }
            }
            .card {
            
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid #f39c12;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: scale(1.02);
            }
                 .stExpander>div {
                background-color: #222;
                border: 1px solid #f39c12;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 1rem;
                color: white;
                transition: background-color 0.3s ease;
            }
            .stExpander>div:hover {
                background-color: #f39c12;
            }

            .stExpander>div>details>summary {
                font-weight: bold;
                font-size: 1.1rem;
                color: #f39c12;
            }

            .stExpander>div>details[open]>summary {
                color: #e67e22;
            }

            .card {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid #f39c12;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                transition: transform 0.3s ease;
            }

            .card:hover {
                transform: scale(1.02);
            }
            


        </style>
    """, unsafe_allow_html=True)

def embed_video():
    video_path = "background.mp4"
    if os.path.exists(video_path):
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            encoded_video = base64.b64encode(video_bytes).decode()
            st.markdown(f"""
                <video autoplay muted loop playsinline id="myVideo">
                    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
                </video>
            """, unsafe_allow_html=True)
    else:
        st.error("Background video file not found.")

def input_page():
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.title("🏋️ Personalized Diet & Fitness Recommendation Chatbot")
    st.markdown('<div id="recommendation_box">', unsafe_allow_html=True)
    with st.form(key='user_profile_form', clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("👤 Full Name")
            age_group = st.text_input("📅 Age")
            gender_identity = st.selectbox("⚥ Gender", ['Male', 'Female'])
        with col2:
            body_weight = st.text_input("⚖️ Weight (kg)"  )
            height_in_cm = st.text_input("📏 Height (cm)")
            diet_preference = st.selectbox("🍴 Diet Preference", ['Veg', 'Non-Veg'])
        allergic_reactions = st.text_input("⛔ Allergic Reactions (Optional)", help="Enter any allergic reactions you have, separated by commas")
        submit_button = st.form_submit_button(label="🔔 Get Recommendations")
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if all([full_name, age_group, gender_identity, body_weight, height_in_cm, diet_preference]):
            user_data = {
                'full_name': full_name,
                'age_group': age_group,
                'gender_identity': gender_identity,
                'body_weight': body_weight,
                'height_in_cm': height_in_cm,
                'diet_preference': diet_preference,
                'allergic_reactions': allergic_reactions
            }
            with st.spinner("Generating your personalized recommendations..."):
                recommendations = generate_recommendations(user_data)
            st.session_state.recommendations = recommendations
            st.session_state.page = "output"
            st.rerun()
        else:
            st.error("Please fill in all required fields!")
    st.markdown('</div>', unsafe_allow_html=True)

def clean_recommendations_text(recommendations_text):
    # Remove markdown symbols and clean up text for the PDF
    cleaned_text = re.sub(r'[*_]', '', recommendations_text)  # Remove asterisks and underscores
    return cleaned_text

def generate_pdf(recommendations_text):
    # Ensure the directory exists
    output_dir = "generated_pdfs"  # or another directory within your app's folder
    os.makedirs(output_dir, exist_ok=True)
    pdf_file_path = os.path.join(output_dir, "recommendations.pdf") 
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Set the title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Personalized Recommendation PDF", ln=True, align='C')
    
    # Set the body content
    pdf.ln(10)  # line break
    pdf.set_font("Arial", '', 12)
    
    # Clean and add recommendations content
    cleaned_text = clean_recommendations_text(recommendations_text)
    pdf.multi_cell(0, 10, cleaned_text)
    
    # Save the PDF
    pdf_file_path = os.path.join(output_dir, "recommendations.pdf")
    pdf.output(pdf_file_path)
    return pdf_file_path

def output_page():
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.title("📊 Your Personalized Recommendations")

    if 'recommendations' in st.session_state:
        st.markdown("### 🎉 Overview")
        with st.expander("View Recommendations"):
            st.markdown(f"<div class='card'>{st.session_state.recommendations}</div>", unsafe_allow_html=True)

        st.markdown("### 📊 Weekly Activity Overview")
        data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Calories Burned": [300, 450, 500, 600, 550, 700, 400]
        })
        fig = px.bar(data, x="Day", y="Calories Burned", color="Day", color_discrete_sequence=px.colors.sequential.YlOrRd)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)

        # Generate and provide a PDF download
        pdf_file_path = generate_pdf(st.session_state.recommendations)
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="recommendations.pdf"><button class="stButton">📥 Download Recommendations (PDF)</button></a>'
            st.markdown(href, unsafe_allow_html=True)

        if st.button("🔙 Back to Input Page"):
            st.session_state.page = "input"
            st.rerun()
    else:
        st.warning("No recommendations found.")
        if st.button("🔙 Back to Input Page"):
            st.session_state.page = "input"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    set_css()
    embed_video()
    if st.session_state.page == "input":
        input_page()
    elif st.session_state.page == "output":
        output_page()

if __name__ == "__main__":
    main()
