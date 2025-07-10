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
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            padding: 2.5rem;
            margin: 2rem auto;
            max-width: 700px;
            transition: all 0.3s ease;
        }
        
        .glass-container:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
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
            background: #f8fafc;
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
def convert_volume(value, unit_from, unit_to, density=1.0):
    # Conversion factors to milliliters (base unit)
    volume_units = {
        "Liter": 1000.0,
        "Milliliter": 1.0,
        "Cubic Meter": 1000000.0,
        "Gallon (US)": 3785.41,
        "Gallon (UK)": 4546.09,
        "Cubic Foot": 28316.8,
        "Cup": 240.0,
        "Tablespoon": 15.0,
        "Teaspoon": 5.0,
        "Fluid Ounce": 30.0
    }
    
    try:
        value = float(value)
        if value < 0:
            return "Value must be non-negative"
        if unit_from == unit_to:
            return value
        if unit_from in ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]:
            # Convert measurement to mass (grams) using density
            volume_ml = value * volume_units[unit_from]
            mass_g = volume_ml * density
            # Convert mass to target volume (mL) using density, then to target unit
            target_volume_ml = mass_g / density
            converted_value = target_volume_ml / volume_units[unit_to]
        else:
            # Convert source volume to milliliters
            volume_ml = value * volume_units[unit_from]
            if unit_to in ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]:
                # Convert to mass (grams) using density
                mass_g = volume_ml * density
                # Convert mass to target volume (mL) using density
                target_volume_ml = mass_g / density
                converted_value = target_volume_ml / volume_units[unit_to]
            else:
                # Standard volume-to-volume conversion
                converted_value = volume_ml / volume_units[unit_to]
        return round(converted_value, 4)
    except (ValueError, KeyError):
        return "Invalid input"

# Main content
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("<h1>UnitSwap: Instant Converter</h1>", unsafe_allow_html=True)
st.write("Instantly swap metric volumes to culinary measurements with this user-friendly tool. Select a substance for precise conversions based on density! 🚀")

# Unit converter UI
st.subheader("Metric Volume to Measurement Converter")
substances = {
    "Water": 1.0,
    "All-Purpose Flour": 0.53,
    "Granulated Sugar": 0.85,
    "Olive Oil": 0.92,
    "Milk": 1.03,
    "Custom": None
}
substance = st.selectbox("Select Substance for Accurate Conversion", list(substances.keys()))
density = substances[substance]
if substance == "Custom":
    density = st.number_input("Enter Density (g/mL)", min_value=0.0, value=1.0, step=0.01)

volume_units = ["Liter", "Milliliter", "Cubic Meter"]
measurement_units = ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]
all_units = volume_units + measurement_units
value = st.text_input("Enter Volume Value", "0")
unit_from = st.selectbox("From Metric Unit", all_units)
unit_to = st.selectbox("To Unit", all_units)
if st.button("Convert"):
    result = convert_volume(value, unit_from, unit_to, density)
    if isinstance(result, str):
        st.error(result)
    else:
        st.success(f"{value} {unit_from} = {result} {unit_to} (for {substance})")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made with ❤️ using Streamlit</div>", unsafe_allow_html=True)
