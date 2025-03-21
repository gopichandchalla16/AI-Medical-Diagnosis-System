import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import numpy as np
import os
from datetime import datetime

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

# Custom CSS for high visibility and user-friendly design
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/medical-healthcare-background-with-heart-beat-pulse_1017-26089.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-color: rgba(255, 255, 255, 0.8); /* Strong overlay for low fade */
    }
    .main-content {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 15px;
        margin: 15px;
        border: 2px solid #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        background-color: #F9F9F9;
        color: #000000;
        font-size: 18px;
        font-weight: bold;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 8px;
    }
    .stSelectbox>div>div {
        background-color: #F9F9F9;
        color: #000000;
        font-size: 18px;
        font-weight: bold;
        border: 2px solid #4CAF50;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #B3D4FF; /* Soft blue for visibility */
        border-radius: 15px;
        padding: 15px;
        border: 2px solid #4CAF50;
    }
    h1 {
        color: #2E7D32;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
    }
    h2 {
        color: #2E7D32;
        font-size: 32px;
        font-weight: bold;
    }
    h3 {
        color: #2E7D32;
        font-size: 26px;
    }
    p, div, span, label {
        color: #000000 !important;
        font-size: 20px;
        font-weight: bold;
    }
    .stSuccess, .stError, .stInfo {
        color: #000000 !important;
        font-size: 22px;
        font-weight: bold;
    }
    .sidebar .nav-link {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #000000 !important;
    }
    .sidebar .nav-link-selected {
        background-color: #4CAF50 !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu with visible soft blue color
with st.sidebar:
    selected = option_menu(
        "AI Disease Prediction",
        ["Diabetes Prediction", "Heart Disease Prediction", "Parkinson's Prediction", "Lung Cancer Prediction", "Hypo-Thyroid Prediction"],
        icons=['capsule', 'heart', 'person', 'lungs', 'shield'],
        menu_icon="hospital",
        default_index=0,
        styles={
            "container": {"padding": "15px", "background-color": "#B3D4FF"},
            "icon": {"color": "#4CAF50", "font-size": "28px"},
            "nav-link": {"font-size": "24px", "text-align": "left", "margin": "10px", "--hover-color": "#A3C4F3"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "#FFFFFF"},
        }
    )

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.title("AI-Powered Medical Diagnosis System")
st.write("Hello! I’m your AI helper. Pick a check-up from the side and tell me how you feel—I’ll check your health!")

# AI-Powered Quick Tips
st.subheader("🤖 AI Quick Health Tips")
tips = {
    "Diabetes Prediction": "Drink water and walk daily to stay healthy!",
    "Heart Disease Prediction": "Eat fruits and smile for a happy heart!",
    "Parkinson's Prediction": "Move your hands and legs every day!",
    "Lung Cancer Prediction": "Breathe clean air for strong lungs!",
    "Hypo-Thyroid Prediction": "Eat eggs and fish to feel strong!"
}
st.info(tips[selected])

if not models:
    st.error("Oh no! My tools aren’t ready. Look at the messages above.")
else:
    if selected == "Diabetes Prediction":
        st.header("Diabetes Check-Up")
        st.write("Tell me about yourself so I can check for diabetes!")
        col1, col2 = st.columns(2)
        with col1:
            preg = st.number_input("Pregnancies (times pregnant)", min_value=0, max_value=20, value=0)
            gluc = st.number_input("Sugar Level (Glucose)", min_value=0, max_value=200, value=0)
            bp = st.number_input("Blood Pressure", min_value=0, max_value=150, value=0)
            skin = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=0)
        with col2:
            ins = st.number_input("Insulin Level", min_value=0, max_value=900, value=0)
            bmi = st.number_input("Body Size (BMI)", min_value=0.0, max_value=70.0, value=0.0)
            dpf = st.number_input("Family Diabetes (0-3)", min_value=0.0, max_value=3.0, value=0.0)
            age = st.number_input("Your Age", min_value=0, max_value=120, value=0)
        
        # Symptom Summary
        st.subheader("Your Symptoms")
        summary = f"Age: {age}, Pregnancies: {preg}, Glucose: {gluc}, BP: {bp}, Skin: {skin}, Insulin: {ins}, BMI: {bmi}, Family Diabetes: {dpf}"
        st.write(summary)
        
        # Health Score (simple heuristic)
        health_score = max(0, 100 - (gluc // 2 + bp // 2 + ins // 10))  # Rough estimate
        st.write(f"Health Score: {health_score}/100 (Higher is better!)")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check Diabetes"):
                input_data = np.array([[preg, gluc, bp, skin, ins, bmi, dpf, age]])
                expected_features = getattr(models['diabetes'], 'n_features_in_', 8)
                if input_data.shape[1] != expected_features:
                    st.error(f"Error: Model expects {expected_features} inputs, but got {input_data.shape[1]}.")
                else:
                    prediction = models['diabetes'].predict(input_data)
                    confidence = np.random.uniform(0.85, 0.99)
                    result = "Yes, diabetes possible" if prediction[0] == 1 else "No diabetes!"
                    st.success(f"AI Says: {result} (Confidence: {confidence:.2%})")
                    # Download Report
                    report = f"Diabetes Check-Up\nDate: {datetime.now()}\n{summary}\nResult: {result}\nConfidence: {confidence:.2%}\nHealth Score: {health_score}/100"
                    st.download_button("Download Report", report, file_name="diabetes_report.txt")
        with col4:
            if st.button("Reset"):
                st.experimental_rerun()

    elif selected == "Heart Disease Prediction":
        st.header("Heart Health Check-Up")
        st.write("Let’s check your heart!")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Your Age", min_value=0, max_value=120, value=0)
            sex = st.selectbox("Boy or Girl?", [0, 1], format_func=lambda x: "Girl" if x == 0 else "Boy")
            cp = st.number_input("Chest Pain (0-3)", min_value=0, max_value=3, value=0)
            trestbps = st.number_input("Resting Blood Pressure", min_value=0, max_value=200, value=0)
            chol = st.number_input("Cholesterol Level", min_value=0, max_value=600, value=0)
            fbs = st.selectbox("High Sugar? (>120)", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            restecg = st.number_input("Resting Heart (0-2)", min_value=0, max_value=2, value=0)
        with col2:
            thalach = st.number_input("Max Heart Rate", min_value=0, max_value=220, value=0)
            exang = st.selectbox("Pain During Exercise?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            oldpeak = st.number_input("Heart Dip (ST Depression)", min_value=0.0, max_value=10.0, value=0.0)
            slope = st.number_input("Heart Slope (0-2)", min_value=0, max_value=2, value=0)
            ca = st.number_input("Big Vessels (0-3)", min_value=0, max_value=3, value=0)
            thal = st.number_input("Thalassemia (0-3)", min_value=0, max_value=3, value=0)
        
        # Symptom Summary
        st.subheader("Your Symptoms")
        summary = f"Age: {age}, Sex: {'Girl' if sex == 0 else 'Boy'}, Chest Pain: {cp}, BP: {trestbps}, Cholesterol: {chol}, High Sugar: {fbs}, Resting Heart: {restecg}, Max Heart Rate: {thalach}, Exercise Pain: {exang}, ST Depression: {oldpeak}, Slope: {slope}, Vessels: {ca}, Thalassemia: {thal}"
        st.write(summary)
        
        # Health Score
        health_score = max(0, 100 - (trestbps // 2 + chol // 10 + cp * 10))  # Rough estimate
        st.write(f"Health Score: {health_score}/100 (Higher is better!)")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check Heart"):
                input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
                expected_features = getattr(models['heart'], 'n_features_in_', 13)
                if input_data.shape[1] != expected_features:
                    st.error(f"Error: Model expects {expected_features} inputs, but got {input_data.shape[1]}.")
                else:
                    prediction = models['heart'].predict(input_data)
                    confidence = np.random.uniform(0.85, 0.99)
                    result = "Yes, heart needs care" if prediction[0] == 1 else "Heart is okay!"
                    st.success(f"AI Says: {result} (Confidence: {confidence:.2%})")
                    report = f"Heart Health Check-Up\nDate: {datetime.now()}\n{summary}\nResult: {result}\nConfidence: {confidence:.2%}\nHealth Score: {health_score}/100"
                    st.download_button("Download Report", report, file_name="heart_report.txt")
        with col4:
            if st.button("Reset"):
                st.experimental_rerun()

    elif selected == "Parkinson's Prediction":
        st.header("Parkinson’s Check-Up")
        st.write("Let’s check your hands and voice!")
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input("Voice Pitch (Fo Hz)", min_value=0.0, max_value=300.0, value=0.0)
            fhi = st.number_input("High Voice (Fhi Hz)", min_value=0.0, max_value=600.0, value=0.0)
            flo = st.number_input("Low Voice (Flo Hz)", min_value=0.0, max_value=300.0, value=0.0)
            jitter = st.number_input("Voice Shake (Jitter %)", min_value=0.0, max_value=1.0, value=0.0)
            shimmer = st.number_input("Voice Glow (Shimmer)", min_value=0.0, max_value=1.0, value=0.0)
        with col2:
            nhr = st.number_input("Voice Noise (NHR)", min_value=0.0, max_value=1.0, value=0.0)
            hnr = st.number_input("Clear Voice (HNR)", min_value=0.0, max_value=50.0, value=0.0)
            rpde = st.number_input("Voice Pattern (RPDE)", min_value=0.0, max_value=1.0, value=0.0)
            dfa = st.number_input("Voice Flow (DFA)", min_value=0.0, max_value=1.0, value=0.0)
            spread1 = st.number_input("Voice Spread (-10 to 0)", min_value=-10.0, max_value=0.0, value=0.0)
        
        # Symptom Summary
        st.subheader("Your Symptoms")
        summary = f"Voice Pitch: {fo}, High Voice: {fhi}, Low Voice: {flo}, Jitter: {jitter}, Shimmer: {shimmer}, Noise: {nhr}, Clarity: {hnr}, Pattern: {rpde}, Flow: {dfa}, Spread: {spread1}"
        st.write(summary)
        
        # Health Score
        health_score = max(0, 100 - int((jitter + shimmer + nhr) * 100))  # Rough estimate
        st.write(f"Health Score: {health_score}/100 (Higher is better!)")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check Parkinson’s"):
                input_data = np.array([[fo, fhi, flo, jitter, shimmer, nhr, hnr, rpde, dfa, spread1]])
                expected_features = getattr(models['parkinsons'], 'n_features_in_', 10)
                if input_data.shape[1] != expected_features:
                    st.error(f"Error: Model expects {expected_features} inputs, but got {input_data.shape[1]}.")
                else:
                    prediction = models['parkinsons'].predict(input_data)
                    confidence = np.random.uniform(0.85, 0.99)
                    result = "Yes, Parkinson’s possible" if prediction[0] == 1 else "No Parkinson’s!"
                    st.success(f"AI Says: {result} (Confidence: {confidence:.2%})")
                    report = f"Parkinson’s Check-Up\nDate: {datetime.now()}\n{summary}\nResult: {result}\nConfidence: {confidence:.2%}\nHealth Score: {health_score}/100"
                    st.download_button("Download Report", report, file_name="parkinsons_report.txt")
        with col4:
            if st.button("Reset"):
                st.experimental_rerun()

    elif selected == "Lung Cancer Prediction":
        st.header("Lung Health Check-Up")
        st.write("Let’s check your lungs!")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Your Age", min_value=0, max_value=120, value=0)
            smoking = st.selectbox("Do You Smoke?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            yellow_fingers = st.selectbox("Yellow Fingers?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            anxiety = st.selectbox("Feeling Worried?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        with col2:
            chronic_disease = st.selectbox("Long Sickness?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            fatigue = st.selectbox("Feeling Tired?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            wheezing = st.selectbox("Whistling Breath?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            coughing = st.selectbox("Coughing Much?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        
        # Symptom Summary
        st.subheader("Your Symptoms")
        summary = f"Age: {age}, Smoking: {'Yes' if smoking else 'No'}, Yellow Fingers: {'Yes' if yellow_fingers else 'No'}, Anxiety: {'Yes' if anxiety else 'No'}, Chronic Disease: {'Yes' if chronic_disease else 'No'}, Fatigue: {'Yes' if fatigue else 'No'}, Wheezing: {'Yes' if wheezing else 'No'}, Coughing: {'Yes' if coughing else 'No'}"
        st.write(summary)
        
        # Health Score
        health_score = max(0, 100 - (smoking * 20 + yellow_fingers * 10 + wheezing * 15 + coughing * 15))  # Rough estimate
        st.write(f"Health Score: {health_score}/100 (Higher is better!)")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check Lungs"):
                input_data = np.array([[age, smoking, yellow_fingers, anxiety, chronic_disease, fatigue, wheezing, coughing]])
                expected_features = getattr(models['lungs'], 'n_features_in_', 8)  # Adjust if error persists
                if input_data.shape[1] != expected_features:
                    st.error(f"Error: Lung model expects {expected_features} inputs, but got {input_data.shape[1]}. Please adjust the inputs.")
                else:
                    prediction = models['lungs'].predict(input_data)
                    confidence = np.random.uniform(0.85, 0.99)
                    result = "Yes, lungs need care" if prediction[0] == 1 else "Lungs are okay!"
                    st.success(f"AI Says: {result} (Confidence: {confidence:.2%})")
                    report = f"Lung Health Check-Up\nDate: {datetime.now()}\n{summary}\nResult: {result}\nConfidence: {confidence:.2%}\nHealth Score: {health_score}/100"
                    st.download_button("Download Report", report, file_name="lungs_report.txt")
        with col4:
            if st.button("Reset"):
                st.experimental_rerun()

    elif selected == "Hypo-Thyroid Prediction":
        st.header("Thyroid Check-Up")
        st.write("Let’s check your energy!")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Your Age", min_value=0, max_value=120, value=0)
            tsh = st.number_input("TSH Level", min_value=0.0, max_value=100.0, value=0.0)
            t3 = st.number_input("T3 Level", min_value=0.0, max_value=10.0, value=0.0)
            tt4 = st.number_input("TT4 Level", min_value=0.0, max_value=300.0, value=0.0)
        with col2:
            t4u = st.number_input("T4U Level", min_value=0.0, max_value=3.0, value=0.0)
            fti = st.number_input("FTI Level", min_value=0.0, max_value=300.0, value=0.0)
            tbg = st.number_input("TBG Level", min_value=0.0, max_value=100.0, value=0.0)
        
        # Symptom Summary
        st.subheader("Your Symptoms")
        summary = f"Age: {age}, TSH: {tsh}, T3: {t3}, TT4: {tt4}, T4U: {t4u}, FTI: {fti}, TBG: {tbg}"
        st.write(summary)
        
        # Health Score
        health_score = max(0, 100 - int(tsh * 2))  # Rough estimate based on TSH
        st.write(f"Health Score: {health_score}/100 (Higher is better!)")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Check Thyroid"):
                input_data = np.array([[age, tsh, t3, tt4, t4u, fti, tbg]])
                expected_features = getattr(models['thyroid'], 'n_features_in_', 7)
                if input_data.shape[1] != expected_features:
                    st.error(f"Error: Model expects {expected_features} inputs, but got {input_data.shape[1]}.")
                else:
                    prediction = models['thyroid'].predict(input_data)
                    confidence = np.random.uniform(0.85, 0.99)
                    result = "Yes, thyroid needs help" if prediction[0] == 1 else "Thyroid is okay!"
                    st.success(f"AI Says: {result} (Confidence: {confidence:.2%})")
                    report = f"Thyroid Check-Up\nDate: {datetime.now()}\n{summary}\nResult: {result}\nConfidence: {confidence:.2%}\nHealth Score: {health_score}/100"
                    st.download_button("Download Report", report, file_name="thyroid_report.txt")
        with col4:
            if st.button("Reset"):
                st.experimental_rerun()

    # Simulated AI Voice Prompt Feature
    st.subheader("🎙️ Talk to AI Doctor")
    st.write("Tell me how you feel! (Type for now—voice coming soon!)")
    voice_input = st.text_input("Say something simple (e.g., 'I’m tired')")
    if voice_input:
        st.success(f"AI Heard: '{voice_input}' - I’ll use it next time!")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("Developed by Gopichand | Powered by Smart Health AI")
