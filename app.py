import streamlit as st
import requests

st.set_page_config(page_title="EthioSoil-AI Dashboard", page_icon="🌱", layout="centered")

st.title("🌱 EthioSoil-AI Advisory Dashboard")
st.markdown("Hyper-Localized Nutrient Optimization and Dual Fertilizer Recommendation System.")

language_choice = st.sidebar.selectbox("Select Language / ቋንቋ / Afaan", ["en", "am", "om"], index=0)
st.sidebar.info("Backend Status: Connected (Live ML Model + PostGIS Logging)")

with st.form("soil_form"):
    st.subheader("1. Farm & Location Details")
    kebele_name = st.text_input("Kebele / Location Name", "Ginchi Highland Plot 4")
    farm_size = st.number_input("Farm Size (Hectares)", min_value=0.1, max_value=50.0, value=1.5)
    
    st.subheader("2. GPS Coordinates (Optional)")
    col_lat, col_lon = st.columns(2)
    with col_lat:
        latitude = st.number_input("Latitude", value=9.00, format="%.4f")
    with col_lon:
        longitude = st.number_input("Longitude", value=38.50, format="%.4f")

    st.subheader("3. Soil Test Parameters")
    col1, col2 = st.columns(2)
    with col1:
        soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=4.8)
        nitrogen = st.number_input("Nitrogen (N) mg/kg", min_value=0.0, value=35.0)
    with col2:
        phosphorus = st.number_input("Phosphorus (P) mg/kg", min_value=0.0, value=12.0)
        potassium = st.number_input("Potassium (K) mg/kg", min_value=0.0, value=110.0)
        
    rainfall = st.number_input("Expected Seasonal Rainfall (mm)", min_value=0.0, value=1150.0)
    
    submitted = st.form_submit_button("Generate AI Recommendation")

if submitted:
    payload = {
        "kebele_name": kebele_name,
        "farm_size_hectares": farm_size,
        "latitude": latitude,
        "longitude": longitude,
        "soil_ph": soil_ph,
        "nitrogen_n": nitrogen,
        "phosphorus_p": phosphorus,
        "potassium_k": potassium,
        "rainfall": rainfall,
        "language": language_choice
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/recommend", json=payload)
        if response.status_code == 200:
            result = response.json()["data"]
            
            st.success("Recommendation Generated Successfully & Logged to DB!")
            
            st.markdown(f"### 📍 Location: {result.get('kebele')}")
            st.markdown(f"🌾 **Crop Recommendation:** {result.get('recommended_crop')}")
            
            # Display Model Performance Metrics in Streamlit Metric Widgets
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Model Confidence", result.get('confidence'))
            col_m2.metric("Model Accuracy", result.get('accuracy'))
            col_m3.metric("Model Precision", result.get('precision'))
            
            st.markdown("---")
            st.markdown(f"🧪 **Soil Acidity Status:** {result.get('acidity_status')}")
            st.markdown(f"💊 **Chemical Prescription:** {result.get('chemical_recommendation')}")
            st.markdown(f"🌿 **Home-Made Organic Recipe:** {result.get('organic_recommendation')}")
        else:
            st.error(f"Server Error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend.")