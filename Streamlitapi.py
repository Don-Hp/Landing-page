import streamlit as st
import pickle
import requests
import numpy as np

# Check for scikit-learn dependency
try:
    from sklearn.preprocessing import LabelEncoder
except ImportError:
    st.error(
        "The 'scikit-learn' library is not installed. Please install it using 'pip install scikit-learn' and try again."
    )
    raise

# URL for the pickle file
url = 'https://raw.githubusercontent.com/Templearikpo/Diabetes-Prediction-App/main/diabetes_prediction_dataset.pkl'

# Fetch the file content from the URL
try:
    response = requests.get(url)
    response.raise_for_status()

    # Save the pickle content to a temporary file and load it
    with open("diabetes_model.pkl", "wb") as f:
        f.write(response.content)

    with open("diabetes_model.pkl", "rb") as f:
        model = pickle.load(f)

    print("Model loaded successfully!")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching the model file from the URL: {e}")
    model = None
except pickle.UnpicklingError as e:
    st.error(f"Error loading the model file: {e}")
    model = None

# Streamlit app
def main():
    if model is None:
        st.error("The prediction model could not be loaded. Please check the source file.")
        return

    st.title("🩺 Diabetes Prediction System")
    st.header("Enter Patient Data")

    # User input
    gender = st.selectbox("Gender", ["Male", "Female", "Others"])
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    heart_disease = st.selectbox("Heart Disease", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    bmi = st.number_input("Body Mass Index (BMI)", min_value=0.0, max_value=100.0, value=22.5)
    HbA1c_level = st.number_input("HbA1c Level", min_value=0.0, max_value=20.0, value=5.5)
    blood_glucose_level = st.number_input("Blood Glucose Level", min_value=0.0, max_value=500.0, value=110.0)
    smoking_history = st.selectbox(
        "Smoking History",
        ["No Info", "Current", "Ever", "Former", "Never", "Not Current"]
    )

    # Encode Gender
    le = LabelEncoder()
    gender_encoded = le.fit_transform(["Male", "Female", "Others"])
    gender = le.transform([gender])[0]

    # One-Hot Encoding for Smoking History
    smoking_history_encoded = [0] * 6
    smoking_categories = ["No Info", "Current", "Ever", "Former", "Never", "Not Current"]
    smoking_history_encoded[smoking_categories.index(smoking_history)] = 1

    # Prepare input features
    inputs = np.array([
        gender,
        age,
        hypertension,
        heart_disease,
        bmi,
        HbA1c_level,
        blood_glucose_level,
        *smoking_history_encoded
    ]).reshape(1, -1)

    if st.button("Predict"):
        try:
            prediction = model.predict(inputs)
            if prediction[0] == 1:
                st.error("This patient is AT RISK of diabetes. Please consult a medical professional.")
            else:
                st.success("This patient is NOT AT RISK of diabetes. Continue maintaining a healthy lifestyle!")
        except Exception as e:
            st.error(f"Error during prediction: {e}")

if __name__ == "__main__":
    main()
