import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load models from pickle files
def load_model(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

models = {
    'Linear Regression': load_model('linear_regression_model.pkl'),
    'Random Forest Regressor': load_model('random_forest_model.pkl')
}

# Mock dataset for demonstration purposes
data = pd.DataFrame({
    'age': np.random.randint(18, 81, 500),
    'bmi': np.random.uniform(12, 80, 500),
    'gender': np.random.choice(['male', 'female'], 500),
    'children': np.random.choice([0, 1, 2, 3], 500),
    'smoker': np.random.choice(['yes', 'no'], 500),
    'region': np.random.choice(['northeast', 'southeast', 'northwest', 'southwest'], 500),
    'charges': np.random.uniform(1000, 50000, 500),
})

# Preprocessing
X = pd.get_dummies(data.drop(columns=['charges']), drop_first=True)
y = data['charges']

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
        'gender_male': [1 if gender == "male" else 0],
        'children': [int(children[0]) if children != "3+" else 3],
        'smoker_yes': [1 if smoker == "yes" else 0],
        'region_northwest': [1 if region == "northwest" else 0],
        'region_southeast': [1 if region == "southeast" else 0],
        'region_southwest': [1 if region == "southwest" else 0],
    })
    
    # Align with model input
    input_data = input_data.reindex(columns=X.columns, fill_value=0)

    # Make prediction
    prediction = selected_model.predict(input_data)[0]

    # Display results
    st.subheader(f"Predicted Charges: ${prediction:,.2f}")
