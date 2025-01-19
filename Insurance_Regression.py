import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
from io import BytesIO
import joblib

# Load models from pickle files
def load_model(model_type):
    file_path = "https://github.com/puneet786/BIA_streamlit/blob/c23d9021c55fe2b582cffdb988727f7fe471d183/lr_model.pkl"
    # with open(file_path, 'rb') as file:
    return joblib.load(BytesIO(requests.get(file_path).content))

models = {
    'Linear Regression': load_model('linear_regression_model'),
    # 'Random Forest Regressor': load_model('random_forest_model.pkl')
}

# Streamlit app
st.title("Insurance Charges Prediction App")

# Sidebar for model selection
st.sidebar.title("Select Model")
selected_model_name = st.sidebar.selectbox("Choose a regression model:", list(models.keys()))
selected_model = models[selected_model_name]

# Form for user inputs
with st.form("input_form"):
    age = st.slider("Age", 18, 80, 30)
    bmi = st.slider("BMI", 12.0, 80.0, 25.0)
    gender = st.selectbox("Gender", ["male", "female"])
    children = st.selectbox("Children", ["0", "1", "2", "3+"])
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["northeast", "southeast", "northwest", "southwest"])
    submit_button = st.form_submit_button("Predict")

if submit_button:
    # Convert inputs to model-compatible format
    input_data = pd.DataFrame({
        'age': [age],
        'bmi': [bmi],
        'sex': [gender],
        'children': [str(children[0]) if children != "3+" else "GTE_3"],
        'smoker': [smoker],
        'region': [region],
    })

    # Make prediction
    prediction = selected_model.predict(input_data)[0]

    # Display results
    st.subheader(f"Predicted Charges: ${prediction:,.2f}")
