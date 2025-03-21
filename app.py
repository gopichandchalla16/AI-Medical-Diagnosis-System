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

# Add background image with low fade and improve text visibility via custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/medical-healthcare-background-with-heart-beat-pulse_1017-26089.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Semi-transparent overlay to make text readable */
    .main-content {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .stTextInput>div>input {
        background-color: rgba(255, 255, 255, 0.9);
        color: #333333;
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #2E7D32;
        font-weight: bold;
    }
    /* Ensure all text is dark and readable */
    p, div, span, label {
        color: #333333 !important;
        font-weight: 500;
    }
    .stSuccess, .stError {
        color: #333333 !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "AI Disease Prediction",
        ["Diabetes Prediction", "Heart Disease Prediction", "Parkinson's Prediction", "Lung Cancer Prediction", "Hypo-Thyroid Prediction"],
        icons=['capsule', 'heart', 'person', 'lungs', 'shield'],
        menu_icon="hospital",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "#4CAF50", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )

# Main content wrapped in a div for better visibility
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.title("AI-Powered Medical Diagnosis System")
st.write("Select a disease from the sidebar to input symptoms and get a prediction.")

if not models:
    st.error("No models loaded. Please check the error messages above.")
else:
    if selected == "Diabetes Prediction":
        st.header("Diabetes Prediction")
        col1, col2 = st.columns(2)
        with col1:
            preg = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
            gluc = st.number_input("Glucose", min_value=0, max_value=200, value=0)
            bp = st.number_input("Blood Pressure", min_value=0, max_value=150, value=0)
            skin = st.number_input("Skin Thickness", min_value=0, max_value=100, value=0)
        with col2:
            ins = st.number_input("Insulin", min_value=0, max_value=900, value=0)
            bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=0.0)
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.0)
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
        
        if st.button("Predict Diabetes"):
            input_data = np.array([[preg, gluc, bp, skin, ins, bmi, dpf, age]])
            prediction = models['diabetes'].predict(input_data)
            result = "Positive (Diabetic)" if prediction[0] == 1 else "Negative (Non-Diabetic)"
            st.success(f"Prediction: {result}")

    elif selected == "Heart Disease Prediction":
        st.header("Heart Disease Prediction")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
            sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
            cp = st.number_input("Chest Pain Type (0-3)", min_value=0, max_value=3, value=0)
            trestbps = st.number_input("Resting Blood Pressure", min_value=0, max_value=200, value=0)
            chol = st.number_input("Cholesterol", min_value=0, max_value=600, value=0)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            restecg = st.number_input("Resting ECG (0-2)", min_value=0, max_value=2, value=0)
        with col2:
            thalach = st.number_input("Max Heart Rate", min_value=0, max_value=220, value=0)
            exang = st.selectbox("Exercise Induced Angina", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=0.0)
            slope = st.number_input("Slope of Peak Exercise ST (0-2)", min_value=0, max_value=2, value=0)
            ca = st.number_input("Major Vessels (0-3)", min_value=0, max_value=3, value=0)
            thal = st.number_input("Thalassemia (0-3)", min_value=0, max_value=3, value=0)
        
        if st.button("Predict Heart Disease"):
            input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            prediction = models['heart'].predict(input_data)
            result = "Positive (Heart Disease)" if prediction[0] == 1 else "Negative (No Heart Disease)"
            st.success(f"Prediction: {result}")

    elif selected == "Parkinson's Prediction":
        st.header("Parkinson's Disease Prediction")
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input("MDVP:Fo(Hz)", min_value=0.0, max_value=300.0, value=0.0)
            fhi = st.number_input("MDVP:Fhi(Hz)", min_value=0.0, max_value=600.0, value=0.0)
            flo = st.number_input("MDVP:Flo(Hz)", min_value=0.0, max_value=300.0, value=0.0)
            jitter = st.number_input("Jitter(%)", min_value=0.0, max_value=1.0, value=0.0)
            shimmer = st.number_input("Shimmer", min_value=0.0, max_value=1.0, value=0.0)
        with col2:
            nhr = st.number_input("NHR", min_value=0.0, max_value=1.0, value=0.0)
            hnr = st.number_input("HNR", min_value=0.0, max_value=50.0, value=0.0)
            rpde = st.number_input("RPDE", min_value=0.0, max_value=1.0, value=0.0)
            dfa = st.number_input("DFA", min_value=0.0, max_value=1.0, value=0.0)
            spread1 = st.number_input("spread1", min_value=-10.0, max_value=0.0, value=0.0)
        
        if st.button("Predict Parkinson's"):
            input_data = np.array([[fo, fhi, flo, jitter, shimmer, nhr, hnr, rpde, dfa, spread1]])
            prediction = models['parkinsons'].predict(input_data)
            result = "Positive (Parkinson's)" if prediction[0] == 1 else "Negative (No Parkinson's)"
            st.success(f"Prediction: {result}")

    elif selected == "Lung Cancer Prediction":
        st.header("Lung Cancer Prediction")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
            smoking = st.selectbox("Smoking", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            yellow_fingers = st.selectbox("Yellow Fingers", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            anxiety = st.selectbox("Anxiety", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        with col2:
            chronic_disease = st.selectbox("Chronic Disease", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            fatigue = st.selectbox("Fatigue", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            wheezing = st.selectbox("Wheezing", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            coughing = st.selectbox("Coughing", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        
        if st.button("Predict Lung Cancer"):
            input_data = np.array([[age, smoking, yellow_fingers, anxiety, chronic_disease, fatigue, wheezing, coughing]])
            prediction = models['lungs'].predict(input_data)
            result = "Positive (Lung Cancer)" if prediction[0] == 1 else "Negative (No Lung Cancer)"
            st.success(f"Prediction: {result}")

    elif selected == "Hypo-Thyroid Prediction":
        st.header("Hypo-Thyroid Prediction")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
            tsh = st.number_input("TSH", min_value=0.0, max_value=100.0, value=0.0)
            t3 = st.number_input("T3", min_value=0.0, max_value=10.0, value=0.0)
            tt4 = st.number_input("TT4", min_value=0.0, max_value=300.0, value=0.0)
        with col2:
            t4u = st.number_input("T4U", min_value=0.0, max_value=3.0, value=0.0)
            fti = st.number_input("FTI", min_value=0.0, max_value=300.0, value=0.0)
            tbg = st.number_input("TBG", min_value=0.0, max_value=100.0, value=0.0)
        
        if st.button("Predict Hypo-Thyroid"):
            input_data = np.array([[age, tsh, t3, tt4, t4u, fti, tbg]])
            prediction = models['thyroid'].predict(input_data)
            result = "Positive (Hypo-Thyroid)" if prediction[0] == 1 else "Negative (No Hypo-Thyroid)"
            st.success(f"Prediction: {result}")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("Developed by Gopichand | Powered by Streamlit")
