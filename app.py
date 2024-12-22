import streamlit as st
import pandas as pd
import requests

st.title("Diabetes Prediction App")

st.write("Enter the patient's details to predict the likelihood of diabetes:")

age = st.number_input("Age", min_value=0, max_value=120, value=30)
hypertension = st.selectbox("Hypertension", options=[0, 1], help="0 = No, 1 = Yes")
heart_disease = st.selectbox("Heart Disease", options=[0, 1], help="0 = No, 1 = Yes")
bmi = st.number_input("BMI", min_value=0.0, max_value=50.0, value=25.0)
HbA1c_level = st.number_input("HbA1c Level", min_value=0.0, max_value=15.0, value=5.5)
blood_glucose_level = st.number_input("Blood Glucose Level", min_value=50, max_value=300, value=120)

gender_encoded = st.selectbox("Gender (Encoded)", options=[0, 1], help="0 = Female, 1 = Male")
smoking_encoded = st.selectbox("Smoking History (Encoded)", options=[0, 1, 2, 3, 4, 5],  help="0 = No Info, 1 = Never, 2 = Former, 3 = Current, 4 = Not Current, 5 = Ever")

gender_name_Male = st.selectbox("Gender Name Male", options=[0, 1], help="0 = Female, 1 = Male")
smoking_status_former = st.selectbox("Smoking Status Former", options=[0, 1], help="0 = No, 1 = Yes")
smoking_status_never = st.selectbox("Smoking Status Never", options=[0, 1], help="0 = No, 1 = Yes")
smoking_status_unknown = st.selectbox("Smoking Status Unknown", options=[0, 1], help="0 = No, 1 = Yes")

input_data = {
    "age": age,
    "hypertension": hypertension,
    "heart_disease": heart_disease,
    "bmi": bmi,
    "HbA1c_level": HbA1c_level,
    "blood_glucose_level": blood_glucose_level,
    "gender_encoded": gender_encoded,
    "smoking_encoded": smoking_encoded,
    "gender_name_Male": gender_name_Male,
    "smoking_status_former": smoking_status_former,
    "smoking_status_never": smoking_status_never,
    "smoking_status_unknown": smoking_status_unknown
}

if st.button("Predict"):
    endpoint = "https://diabetesprediction.up.railway.app/predict" 
    
    try:
        response = requests.post(endpoint, json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Prediction: {prediction['diabetes']} (0 = No Diabetes, 1 = Diabetes)")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
