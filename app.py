# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
import langchain.globals as lcg
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_icon="🏋️", page_title="Personalized Diet & Fitness")

if 'page' not in st.session_state:
    st.session_state.page = 'input'

lcg.set_verbose(True)
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBGKnyD4gAXmoeXT61bikW-wkQ4SRr3yU4'

config = {"temperature": 0.6, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
ai_model = GoogleGenerativeAI(model="gemini-pro", generation_config=config)

diet_prompt_template = PromptTemplate(
    input_variables=[
        'full_name', 'age_group', 'gender_identity', 'body_weight',
        'height_in_cm', 'diet_preference', 'allergic_reactions'
    ],
    template="""
    Diet and Exercise Recommendation System:
    Suggest 6 types of home workouts with detailed instructions,
    6 breakfast ideas with nutritional information,
    5 dinner options with nutritional information, 
    and 6 gym workout plans for each day of the week.
    Full Name: {full_name}
    Age: {age_group}
    Gender: {gender_identity}
    Weight: {body_weight}
    Height: {height_in_cm}
    Diet Preference: {diet_preference}
    Allergic Reactions: {allergic_reactions}
    """
)

recommendation_chain = RunnableLambda(lambda inputs: diet_prompt_template.format(**inputs)) | ai_model

def set_css():
    st.markdown("""
        <style>
            #myVideo {
                position: fixed;
                top: 50%;
                left: 33%;
                min-width: 100%;
                min-height: 100%;
                width: auto;
                height: auto;
                z-index: 0;
                transform: translate(-50%, -30%);
                background-size: cover;
            }
            .content {
                top: 0;
                left: -2px;
                height: -webkit-fill-available;
                width: 101.9%;
                position: fixed;
                background: rgba(0, 0, 0, 0.7);
                color: #f1f1f1;
                padding: 0;
                border-radius: 8px;
                margin: -30px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
            }
            #recommendation_box {
                width: 90%;
                margin: 5% auto;
                animation: fadeIn 1.5s ease-in-out;
                text-align: center;
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
                    height: 100%;
                    width: 100%;
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
    st.title("🏋️ Personalized Diet & Fitness Recommendation")
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
        allergic_reactions = st.text_input("⛔ Allergic Reactions")
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
                recommendations = recommendation_chain.invoke(user_data)
            st.session_state.recommendations = recommendations
            st.session_state.page = "output"
            st.rerun()
        else:
            st.error("Please fill in all required fields!")
    st.markdown('</div>', unsafe_allow_html=True)

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

        recommendations_text = st.session_state.recommendations
        b64 = base64.b64encode(recommendations_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="recommendations.txt"><button class="stButton">📥 Download Recommendations</button></a>'
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