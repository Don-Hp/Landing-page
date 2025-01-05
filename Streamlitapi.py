import streamlit as st
import pickle
import requests
import numpy as np
from sklearn.preprocessing import LabelEncoder

# URL for the pickle file
url = 'https://raw.githubusercontent.com/Templearikpo/Diabetes-Prediction-App/main/diabetes_prediction_dataset.pkl'

# Fetch the file content from the URL
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

    # Save the pickle content to a temporary file and load it
    with open("diabetes_model.pkl", "wb") as f:
        f.write(response.content)

    with open("diabetes_model.pkl", "rb") as f:
        model = pickle.load(f)

    print("Model loaded successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error fetching the file from URL: {e}")
    model = None
except pickle.UnpicklingError as e:
    print(f"Error unpickling the file: {e}")
    model = None

# Streamlit app
def main():
    if model is None:
        st.error("The prediction model could not be loaded. Please check the source file.")
        return

    # App title and description
    st.set_page_config(page_title="Diabetes Prediction System", page_icon="🩺", layout="centered")

    st.markdown(
        """
        <style>
         body {
            background-color: #f4f9f4; /* Soft green background for health theme */
            background-image: url('https://images.unsplash.com/photo-1565376987447-22a3a490b809?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080'); 
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .title-container {
            background: white;
            border: 3px solid #2E8B57;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        .title-container h1 {
            font-size: 36px;
            color: #2E8B57;
            margin: 0;
        }
        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            left: 0;
            background-color: #f4f4f4;
            padding: 10px;
            text-align: center;
            font-size: 14px;
            color: #555;
            border-top: 1px solid #ddd;
        }
        .result {
            font-size: 24px;
            color: green;
            font-weight: bold;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="title-container"><h1>🩺 Diabetes Prediction System</h1></div>', unsafe_allow_html=True)

    # Layout for user input
    st.header("Enter Patient Data")

    # Input fields for patient data
    gender = st.selectbox("Gender", ["Male", "Female", "Others"])
    age = st.text_input("Age", "0")
    hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    heart_disease = st.selectbox("Heart Disease", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    bmi = st.text_input("Body Mass Index (BMI)", "0.0")
    HbA1c_level = st.text_input("HbA1c Level", "0.0")
    blood_glucose_level = st.text_input("Blood Glucose Level", "0.0")
    smoking_history = st.selectbox(
        "Smoking History",
        ["No Info", "Current", "Ever", "Former", "Never", "Not Current"]
    )

    # Convert inputs to numeric
    try:
        age = int(age)
        bmi = float(bmi)
        HbA1c_level = float(HbA1c_level)
        blood_glucose_level = float(blood_glucose_level)
    except ValueError:
        st.error("Please enter valid numeric values for age, BMI, HbA1c, and blood glucose.")
        return

    # Encode Gender
    le = LabelEncoder()
    gender_encoded = le.fit_transform(["Male", "Female", "Others"])
    gender = le.transform([gender])[0]

    # One-Hot Encoding for Smoking History
    smoking_history_encoded = [0] * 6
    smoking_categories = ["No Info", "Current", "Ever", "Former", "Never", "Not Current"]
    smoking_history_encoded[smoking_categories.index(smoking_history)] = 1

    # Prepare the input features
    inputs = [
        gender,
        age,
        hypertension,
        heart_disease,
        bmi,
        HbA1c_level,
        blood_glucose_level,
        *smoking_history_encoded
    ]
    inputs = np.array(inputs).reshape(1, -1)

    st.subheader("Patient Data Summary")
    st.write(f"**Gender:** {gender}")
    st.write(f"**Age:** {age}")
    st.write(f"**Hypertension:** {'Yes' if hypertension == 1 else 'No'}")
    st.write(f"**Heart Disease:** {'Yes' if heart_disease == 1 else 'No'}")
    st.write(f"**BMI:** {bmi}")
    st.write(f"**HbA1c Level:** {HbA1c_level}")
    st.write(f"**Blood Glucose Level:** {blood_glucose_level}")
    st.write(f"**Smoking History:** {smoking_history}")

    # Make prediction
    if st.button("Predict"):
        try:
            prediction = model.predict(inputs)
            if prediction[0] == 1:
                result = "This patient is AT RISK of diabetes. Please, consult a medical professional."
            else:
                result = "This patient is NOT AT RISK of diabetes. Continue a healthy lifestyle with a balanced diet and regular exercise."
            
            st.markdown(f'<div class="result">{result}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error during prediction: {e}")

    # Footer
    st.markdown(
        """
        <div class="footer">
            Powered by <b>Predictive Wellness Partners (PWP)</b>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Run the app
if __name__ == "__main__":
    main()
