import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Exam Anxiety Detector",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
        /* Hide the Streamlit header and deploy button */
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        [data-testid="stToolbar"] {display: none;}
        
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .main-title {
            text-align: center;
            color: #2E86C1;
        }
        .tip-box {
            padding: 15px;
            border-radius: 8px;
            background-color: #f0f2f6;
            margin-top: 10px;
            color: #1f2937; /* Dark gray color for visibility */
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🧠 AI-Based Exam Anxiety Detector</h1>', unsafe_allow_html=True)
st.write("""
Welcome! This intelligent mental-wellness support system identifies exam-related anxiety based on your reflections or pre-exam thoughts.
*Note: This system is designed as a supportive and non-diagnostic tool to help you manage pre-exam stress. All data is processed anonymously.*
""")

text_input = st.text_area("How are you feeling about your upcoming exam?", height=150, placeholder="Express your thoughts here...")

if st.button("Evaluate Anxiety Level"):
    if text_input.strip():
        with st.spinner("Analyzing your thoughts..."):
            try:
                # Call FastAPI backend (uses environment variable for production)
                api_url = os.getenv("API_URL", "http://localhost:8000")
                response = requests.post(f"{api_url}/predict", json={"text": text_input})
                
                if response.status_code == 200:
                    result = response.json()
                    anxiety_level = result["anxiety_level"]
                    
                    st.subheader("Analysis Result")
                    
                    if anxiety_level == "Low":
                        st.success(f"**Anxiety Level:** {anxiety_level} 🟢")
                        st.markdown("""
                        <div class='tip-box'>
                            <b>Tips for maintaining focus:</b>
                            <ul>
                                <li>Keep up your current study routine!</li>
                                <li>Ensure you get a good night's sleep before the exam.</li>
                                <li>Stay hydrated and eat a healthy meal before your test.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    elif anxiety_level == "Moderate":
                        st.warning(f"**Anxiety Level:** {anxiety_level} 🟡")
                        st.markdown("""
                        <div class='tip-box'>
                            <b>Tips for managing moderate anxiety:</b>
                            <ul>
                                <li>Take short, frequent breaks during studying (e.g., Pomodoro technique).</li>
                                <li>Practice deep breathing exercises (inhale 4s, hold 4s, exhale 4s).</li>
                                <li>Visualize yourself feeling calm and doing well in the exam.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    elif anxiety_level == "High":
                        st.error(f"**Anxiety Level:** {anxiety_level} 🔴")
                        st.markdown("""
                        <div class='tip-box'>
                            <b>Immediate calming tips:</b>
                            <ul>
                                <li><b>Breathe:</b> Try the 4-7-8 breathing technique down-regulate your nervous system.</li>
                                <li><b>Reach out:</b> Talk to a friend, counselor, or teacher about how you feel.</li>
                                <li><b>Ground yourself:</b> Name 5 things you can see, 4 you can touch, 3 you can hear.</li>
                                <li>Remember, your worth is not defined by a single exam. Reach out to campus support services if you feel overwhelmed.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(f"**Anxiety Level:** {anxiety_level}")
                        
                else:
                    st.error(f"Error from server: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter your thoughts before evaluating.")
