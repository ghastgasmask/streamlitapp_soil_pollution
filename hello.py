import streamlit as st
import pickle
import numpy as np

st.set_page_config(layout="wide")

# loading model
with open('personalprojectmodel.pkl', 'rb') as f:
    lr2 = pickle.load(f)

# sidebar
st.sidebar.header('Soil Features')

def get_user_input():
    temp = st.sidebar.number_input('Input temperature of the soil (°C)', min_value=10.0, max_value=50.0, step=0.1, value=25.0)
    rainfall = st.sidebar.number_input('Input rainfall in that area (mm)', min_value=10.0, max_value=400.0, step=0.1, value=100.0)
    humidity = st.sidebar.number_input('Input humidity of the soil (%)', min_value=0.0, max_value=100.0, step=0.1, value=50.0)
    pHLevel = st.sidebar.number_input('Input pH level of the soil', min_value=4.00, max_value=14.00, step=0.01, value=7.00)
    soilTexture = st.sidebar.selectbox('Input soil texture', ['Loamy', 'Silty', 'Clay', 'Sandy'])

    user_data = {
        'pHLevel_No': pHLevel,
        'Temperature_No': temp,
        'Humidity_No': humidity,
        'Rainfall_No': rainfall,
        'SoilTexture': soilTexture 
    }
    return user_data

# title
st.markdown("<h1 style='text-align: center;'>Soil Pollution Prediction Web App</h1>", unsafe_allow_html=True)

# geti nput
user_data = get_user_input()

# input preparationlelelele
def prepare_input(data, feature_list):
    soil_texture_map = {'Loamy': 1, 'Silty': 2, 'Clay': 3, 'Sandy': 4}
    soil_texture_numerical = soil_texture_map.get(data.get('SoilTexture', None), 0)

    input_data = {
        'Soil_pH': data.get('pHLevel_No', 0),
        'Temperature_C': data.get('Temperature_No', 0),
        'Humidity_%': data.get('Humidity_No', 0),
        'Rainfall_mm': data.get('Rainfall_No', 0),
        'Soil_Texture': soil_texture_numerical
    }

    input_array = np.array([list(input_data.values())])
    return input_array

features = ['Soil_pH', 'Temperature_C', 'Humidity_%', 'Rainfall_mm', 'Soil_Texture']

# predict
if st.button("Predict"):
    input_array = prepare_input(user_data, features)
    st.write("What you have inputted (how the computer perceives this):", input_array)  # THIS LINE OF CODE is made to compare the input 
    #data with what the ML model received, and see if tehre are mistakes (DEBUG) 
    prediction = lr2.predict(input_array)
    st.subheader("Predicted Pollution Level")
    st.write("0 = Low, 3 = Medium, 5+ = High")
    st.success(f"Predicted value: {prediction[0]:.2f}")
