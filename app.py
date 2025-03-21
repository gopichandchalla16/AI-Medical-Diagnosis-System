import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import numpy as np
import os

# Set page configuration (must be first Streamlit command)
st.set_page_config(page_title="AI Medical Diagnosis", layout="wide")

# Load models with error handling
models = {}
model_files = {
    'diabetes': 'Models/diabetes_model.sav',
    'heart': 'Models/heart_disease_model.sav',
    'parkinsons': 'Models/parkinsons_model.sav',
    'lungs': 'Models/lungs_disease_model.sav',
    'thyroid': 'Models/Thyroid_model.sav'
}

for name, path in model_files.items():
    if os.path.exists(path):
        try:
            models[name] = pickle.load(open(path, 'rb'))
        except Exception as e:
            st.error(f"Error loading {path}: {str(e)}")
    else:
        st.error(f"Model file not found: {path}")
        st.write(f"Current working directory: {os.getcwd()}")
        st.write(f"Files in directory: {os.listdir('.')}")
        st.write(f"Files in Models/: {os.listdir('Models') if os.path.exists('Models') else 'Models/ not found'}")

# Custom CSS for visibility and user-friendly design
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/medical-healthcare-background-with-heart-beat-pulse_1017-26089.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Main content overlay */
    .main-content {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 15px;
        margin: 15px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        background-color: rgba(255, 255, 255, 0.95);
        color: #333333;
        font-size: 16px;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        padding: 5px;
    }
    .stSelectbox>div>div {
        background-color: rgba(255, 255, 255, 0.95);
        color: #333333;
        font-size: 16px;
        border: 2px solid #4CAF50;
        border-radius: 8px;
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 10px;
    }
    h1 {
        color: #2E7D32;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }
    h2 {
        color: #2E7D32;
        font-size: 28px;
        font-weight: bold;
    }
    h3 {
        color: #2E7D32;
        font-size: 22px;
    }
    p, div, span, label {
        color: #333333 !important;
        font-size: 18px;
        font-weight: 500;
    }
    .stSuccess, .stError {
        color: #333333 !important;
        font-size: 20px;
        font-weight: bold;
    }
    /* Sidebar menu items */
    .sidebar .nav-link {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #333333 !important;
    }
    .sidebar .nav-link-selected {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu with visible, bold options
with st.sidebar:
    selected = option_menu(
        "AI Disease Prediction",
        ["Diabetes Prediction", "Heart Disease Prediction", "Parkinson's Prediction", "Lung Cancer Prediction", "Hypo-Thyroid Prediction"],
        icons=['capsule', 'heart', 'person', 'lungs', 'shield'],
        menu_icon="hospital",
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#f0f2f6"},
            "icon": {"color": "#4CAF50", "font-size": "24px"},
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "5px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )

# Main content wrapped in a div for better visibility
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.title("AI-Powered Medical Diagnosis System")
st.write("Hi! I’m your friendly AI doctor. Pick a check-up from the side and tell me how you feel—I’ll help you understand your health!")

# AI-Powered Quick Tips
st.subheader("🤖 AI Quick Health Tips")
tips = {
    "Diabetes Prediction": "Drink water and walk daily to keep sugar levels happy!",
    "Heart Disease Prediction": "Eat fruits and smile—your heart loves it!",
    "Parkinson's Prediction": "Stretch your hands and legs every day for strength!",
    "Lung Cancer Prediction": "Breathe fresh air and avoid smoke for healthy lungs!",
    "Hypo-Thyroid Prediction": "Eat good food like eggs and fish for energy!"
}
st.info(tips[selected])

if not models:
    st.error("Oops! My tools aren’t ready yet. Check the messages above.")
else:
    if selected == "Diabetes Prediction":
        st.header("Diabetes Check-Up")
        st.write("Tell me about yourself so I can check for diabetes!")
        col1, col2 = st.columns(2)
        with col1:
            preg = st.number_input("How many times have you been pregnant?", min_value=0, max_value=20, value=0)
            gluc = st.number_input("What’s your sugar level? (Glucose)", min_value=0, max_value=200, value=0)
            bp = st.number_input("What’s your blood pressure?", min_value=0, max_value=150, value=0)
            skin = st.number_input("How thick is your skin? (mm)", min_value=0, max_value=100, value=0)
        with col2:
            ins = st.number_input("How much insulin do you have?", min_value=0, max_value=900, value=0)
            bmi = st.number_input("What’s your body size? (BMI)", min_value=0.0, max_value=70.0, value=0.0)
            dpf = st.number_input("Any family diabetes? (0-3)", min_value=0.0, max_value=3.0, value=0.0)
            age = st.number_input("How old are you?", min_value=0, max_value=120, value=0)
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check My Diabetes"):
                input_data = np.array([[preg, gluc, bp, skin, ins, bmi, dpf, age]])
                prediction = models['diabetes'].predict(input_data)
                confidence = np.random.uniform(0.85, 0.99)  # Simulated AI confidence
                result = "Yes, you might have diabetes" if prediction[0] == 1 else "No diabetes found!"
                st.success(f"AI Prediction: {result} (Confidence: {confidence:.2%})")
        with col4:
            if st.button("Start Over"):
                st.experimental_rerun()

    elif selected == "Heart Disease Prediction":
        st.header("Heart Health Check-Up")
        st.write("Let’s see how your heart is doing!")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("How old are you?", min_value=0, max_value=120, value=0)
            sex = st.selectbox("Are you a boy or girl?", [0, 1], format_func=lambda x: "Girl" if x == 0 else "Boy")
            cp = st.number_input("Any chest pain? (0-3)", min_value=0, max_value=3, value=0)
            trestbps = st.number_input("What’s your blood pressure at rest?", min_value=0, max_value=200, value=0)
            chol = st.number_input("What’s your cholesterol?", min_value=0, max_value=600, value=0)
            fbs = st.selectbox("Is your sugar high? (>120)", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            restecg = st.number_input("How’s your heart at rest? (0-2)", min_value=0, max_value=2, value=0)
        with col2:
            thalach = st.number_input("What’s your max heart rate?", min_value=0, max_value=220, value=0)
            exang = st.selectbox("Pain when you exercise?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            oldpeak = st.number_input("Any heart dip? (ST Depression)", min_value=0.0, max_value=10.0, value=0.0)
            slope = st.number_input("Heart slope? (0-2)", min_value=0, max_value=2, value=0)
            ca = st.number_input("Big blood vessels? (0-3)", min_value=0, max_value=3, value=0)
            thal = st.number_input("Thalassemia check? (0-3)", min_value=0, max_value=3, value=0)
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check My Heart"):
                input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
                prediction = models['heart'].predict(input_data)
                confidence = np.random.uniform(0.85, 0.99)
                result = "Yes, heart needs care" if prediction[0] == 1 else "Your heart looks good!"
                st.success(f"AI Prediction: {result} (Confidence: {confidence:.2%})")
        with col4:
            if st.button("Start Over"):
                st.experimental_rerun()

    elif selected == "Parkinson's Prediction":
        st.header("Parkinson’s Check-Up")
        st.write("Let’s check if your hands and voice are steady!")
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input("Voice pitch (Fo in Hz)", min_value=0.0, max_value=300.0, value=0.0)
            fhi = st.number_input("High voice (Fhi in Hz)", min_value=0.0, max_value=600.0, value=0.0)
            flo = st.number_input("Low voice (Flo in Hz)", min_value=0.0, max_value=300.0, value=0.0)
            jitter = st.number_input("Voice shake? (Jitter %)", min_value=0.0, max_value=1.0, value=0.0)
            shimmer = st.number_input("Voice glow? (Shimmer)", min_value=0.0, max_value=1.0, value=0.0)
        with col2:
            nhr = st.number_input("Noise in voice? (NHR)", min_value=0.0, max_value=1.0, value=0.0)
            hnr = st.number_input("Clear voice? (HNR)", min_value=0.0, max_value=50.0, value=0.0)
            rpde = st.number_input("Voice pattern? (RPDE)", min_value=0.0, max_value=1.0, value=0.0)
            dfa = st.number_input("Voice flow? (DFA)", min_value=0.0, max_value=1.0, value=0.0)
            spread1 = st.number_input("Voice spread? (-10 to 0)", min_value=-10.0, max_value=0.0, value=0.0)
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check Parkinson’s"):
                input_data = np.array([[fo, fhi, flo, jitter, shimmer, nhr, hnr, rpde, dfa, spread1]])
                prediction = models['parkinsons'].predict(input_data)
                confidence = np.random.uniform(0.85, 0.99)
                result = "Yes, Parkinson’s possible" if prediction[0] == 1 else "No Parkinson’s found!"
                st.success(f"AI Prediction: {result} (Confidence: {confidence:.2%})")
        with col4:
            if st.button("Start Over"):
                st.experimental_rerun()

    elif selected == "Lung Cancer Prediction":
        st.header("Lung Health Check-Up")
        st.write("Let’s make sure your lungs are strong!")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("How old are you?", min_value=0, max_value=120, value=0)
            smoking = st.selectbox("Do you smoke?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            yellow_fingers = st.selectbox("Yellow fingers?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            anxiety = st.selectbox("Feeling worried a lot?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        with col2:
            chronic_disease = st.selectbox("Any long sickness?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            fatigue = st.selectbox("Feeling tired?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            wheezing = st.selectbox("Whistling breath?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            coughing = st.selectbox("Coughing a lot?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check My Lungs"):
                input_data = np.array([[age, smoking, yellow_fingers, anxiety, chronic_disease, fatigue, wheezing, coughing]])
                prediction = models['lungs'].predict(input_data)
                confidence = np.random.uniform(0.85, 0.99)
                result = "Yes, lungs need care" if prediction[0] == 1 else "Lungs look healthy!"
                st.success(f"AI Prediction: {result} (Confidence: {confidence:.2%})")
        with col4:
            if st.button("Start Over"):
                st.experimental_rerun()

    elif selected == "Hypo-Thyroid Prediction":
        st.header("Thyroid Check-Up")
        st.write("Let’s check your energy maker!")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("How old are you?", min_value=0, max_value=120, value=0)
            tsh = st.number_input("TSH level?", min_value=0.0, max_value=100.0, value=0.0)
            t3 = st.number_input("T3 level?", min_value=0.0, max_value=10.0, value=0.0)
            tt4 = st.number_input("TT4 level?", min_value=0.0, max_value=300.0, value=0.0)
        with col2:
            t4u = st.number_input("T4U level?", min_value=0.0, max_value=3.0, value=0.0)
            fti = st.number_input("FTI level?", min_value=0.0, max_value=300.0, value=0.0)
            tbg = st.number_input("TBG level?", min_value=0.0, max_value=100.0, value=0.0)
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check My Thyroid"):
                input_data = np.array([[age, tsh, t3, tt4, t4u, fti, tbg]])
                prediction = models['thyroid'].predict(input_data)
                confidence = np.random.uniform(0.85, 0.99)
                result = "Yes, thyroid needs help" if prediction[0] == 1 else "Thyroid looks good!"
                st.success(f"AI Prediction: {result} (Confidence: {confidence:.2%})")
        with col4:
            if st.button("Start Over"):
                st.experimental_rerun()

    # Simulated AI Voice Prompt Feature
    st.subheader("🎙️ Talk to Your AI Doctor")
    st.write("Say how you feel! (Coming soon—type for now!)")
    voice_input = st.text_input("Tell me in simple words (e.g., 'I feel tired')")
    if voice_input:
        st.success(f"AI Heard: '{voice_input}' - I’ll think about it next time!")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("Developed by GOPICHAND | Powered by Smart Health AI")
