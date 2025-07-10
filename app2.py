import streamlit as st

def apply_glass_style():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Roboto', 'Inter', sans-serif;
            background: linear-gradient(135deg, #d6eaff 0%, #f0e7ff 100%);
            color: #1e293b;
            margin: 0;
            padding: 0;
        }
        
        .glass-container {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 2.5rem;
            margin: 2rem auto;
            max-width: 700px;
            transition: all 0.3s ease;
        }
        
        .glass-container:hover {
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
            transform: translateY(-3px);
        }
        
        h1 {
            color: #1e40af;
            font-weight: 700;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }
        
        h2, h3 {
            color: #1e40af;
            font-weight: 600;
            text-align: center;
        }
        
        .stButton>button {
            background: #3b82f6;
            color: white;
            border-radius: 10px;
            padding: 0.8rem 1.8rem;
            border: none;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
            box-sizing: border-box;
        }
        
        .stButton>button:hover {
            background: #2563eb;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
            transform: translateY(-1px);
        }
        
        .stTextInput>div>input, .stSelectbox>div>select {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            padding: 0.8rem;
            font-size: 1rem;
            color: #1e293b;
        }
        
        .stTextInput>label, .stSelectbox>label {
            color: #1e40af;
            font-weight: 500;
            font-size: 1.1rem;
        }
        
        .footer {
            text-align: center;
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="UnitSwap",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Apply custom styles
apply_glass_style()

# Conversion logic for volume units
def convert_volume(value, unit_from, unit_to):
    # Conversion factors to liters (base unit)
    volume_units = {
        "Liter": 1.0,
        "Milliliter": 0.001,
        "Gallon (US)": 3.78541,
        "Gallon (UK)": 4.54609,
        "Cubic Meter": 1000.0,
        "Cubic Foot": 28.3168
    }
    
    try:
        value = float(value)
        if unit_from == unit_to:
            return value
        # Convert from source unit to liters, then to target unit
        value_in_liters = value * volume_units[unit_from]
        converted_value = value_in_liters / volume_units[unit_to]
        return round(converted_value, 4)
    except (ValueError, KeyError):
        return "Invalid input"

# Main content
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("<h1>UnitSwap: Instant Converter</h1>", unsafe_allow_html=True)
st.write("Convert volume units instantly with ease. Enter a value, select units, and get results in real-time! 🚀")

# Unit converter UI
st.subheader("Volume Converter")
volume_units = ["Liter", "Milliliter", "Gallon (US)", "Gallon (UK)", "Cubic Meter", "Cubic Foot"]
value = st.text_input("Enter Value", "0")
unit_from = st.selectbox("From Unit", volume_units)
unit_to = st.selectbox("To Unit", volume_units)
if st.button("Convert"):
    result = convert_volume(value, unit_from, unit_to)
    if isinstance(result, str):
        st.error(result)
    else:
        st.success(f"{value} {unit_from} = {result} {unit_to}")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made By Jalen Claytor</div>", unsafe_allow_html=True)
