# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import re
from dotenv import load_dotenv
from pathlib import Path
import cohere

# Load environment variables from project root
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path, override=False)

st.set_page_config(layout="wide", page_icon="🏋️", page_title="Personalized Diet & Fitness")

if 'page' not in st.session_state:
    st.session_state.page = 'input'

cohere_api_key = os.getenv('COHERE_API_KEY')
if not cohere_api_key:
    st.error("Cohere API key not found. Please set the COHERE_API_KEY environment variable.")
    st.stop()

co = cohere.Client(cohere_api_key)

def generate_recommendations(user_data):
    prompt = f"""
    Diet and Exercise Recommendation System:
    - Suggest 6 types of home workouts with concise but clear instructions.
    - Suggest 6 breakfast ideas and 5 dinner options, each with brief nutritional information and estimated calories per serving amd their recipe too with total protein they will get after eating that meal  .
    - For each food, include calories and a short note on its health benefits or suitability for the user's profile.
    - For gym workout plans, provide a summarized weekly plan (6 days), listing the main focus and key exercises for each day ad include how to do that exercise properly.
    - Do NOT include disclaimers or generic advice.
    Full Name: {user_data['full_name']}
    Age: {user_data['age_group']}
    Gender: {user_data['gender_identity']}
    Weight: {user_data['body_weight']}
    Height: {user_data['height_in_cm']}
    Diet Preference: {user_data['diet_preference']}
    Allergic Reactions: {user_data['allergic_reactions']}
    """

    supported_models = [
        "command-r",
        "command-r-08-2024",
        "command-r-plus-08-2024",
    ]

    last_error = None
    for model_name in supported_models:
        try:
            response = co.chat(
                model=model_name,
                preamble="You are a professional AI health and fitness assistant.",
                message=prompt,
                temperature=0.7,
                max_tokens=3500
            )
            return response.text
        except Exception as e:
            last_error = e
            continue

    st.error(f"Error generating recommendations: {last_error}")
    return f"Unable to generate recommendations at this time. Error: {last_error}"

def set_css():
    st.markdown("""
        <style>
            #myVideo {
                     position: fixed;
                     top: 0;
                     left: 0;
                     width: 99.3%;
                     height: 100%;
                     object-fit: fill;
                     z-index: 0;
                   }
            .content {
                     width: 99.3%;
                      height: -webkit-fill-available;
                      position: fixed;
                      top: 0;
                      left: 0;
                      right: 0;
                      bottom: 0;
                      overflow-y: auto;
                      background: rgba(0, 0, 0, 0.7);
                      color: #f1f1f1;
                      padding: 30px;
                      box-sizing: border-box;
                      z-index: 0;
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
            body_weight = st.text_input("⚖️ Weight (kg)")
            height_in_cm = st.text_input("📏 Height (cm)")
            diet_preference = st.selectbox("🍴 Diet Preference", ['Veg', 'Non-Veg'])
        allergic_reactions = st.text_input("⛔ Allergic Reactions (Optional)", help="Enter any allergic reactions you have, separated by commas")
        submit_button = st.form_submit_button(label="🔔 Get Recommendations")
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        # Input validation
        errors = []
        if not full_name.strip():
            errors.append("Full Name is required.")
        try:
            age = int(age_group)
            if not (1 <= age <= 122):
                errors.append("Please enter a valid age between 1 and 122.")
        except Exception:
            errors.append("Please enter a valid numeric age.")
        try:
            weight = float(body_weight)
            if not (2 <= weight <= 635):
                errors.append("Please enter a valid weight between 2 and 635 kg.")
        except Exception:
            errors.append("Please enter a valid numeric weight.")
        try:
            height = float(height_in_cm)
            if not (30 <= height <= 272):
                errors.append("Please enter a valid height between 30 and 272 cm.")
        except Exception:
            errors.append("Please enter a valid numeric height.")
        if not diet_preference:
            errors.append("Diet Preference is required.")
        if not gender_identity:
            errors.append("Gender is required.")

        if errors:
            for error in errors:
                st.error(error)
        else:
            user_data = {
                'full_name': full_name,
                'age_group': age,
                'gender_identity': gender_identity,
                'body_weight': weight,
                'height_in_cm': height,
                'diet_preference': diet_preference,
                'allergic_reactions': allergic_reactions
            }
            with st.spinner("Generating your personalized recommendations..."):
                recommendations = generate_recommendations(user_data)
            st.session_state.recommendations = recommendations
            st.session_state.page = "output"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def clean_recommendations_text(recommendations_text):
    cleaned_text = re.sub(r'[*_]', '', recommendations_text)
    cleaned_text = ''.join(c if ord(c) < 128 else ' ' for c in cleaned_text)
    return cleaned_text

def generate_pdf(recommendations_text):
    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)
    pdf_file_path = os.path.join(output_dir, "recommendations.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Personalized Recommendation PDF", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    cleaned_text = clean_recommendations_text(recommendations_text)
    try:
        pdf.multi_cell(0, 10, cleaned_text)
    except Exception:
        cleaned_text = ''.join(c for c in cleaned_text if ord(c) < 128)
        pdf.multi_cell(0, 10, cleaned_text)
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
        try:
            pdf_file_path = generate_pdf(st.session_state.recommendations)
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="recommendations.pdf"><button class="stButton">📥 Download Recommendations (PDF)</button></a>'
                st.markdown(href, unsafe_allow_html=True)
        except Exception:
            st.error("Could not generate PDF. Please try again or contact support.")
            st.info("You can still view your recommendations in the Overview section above.")
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
