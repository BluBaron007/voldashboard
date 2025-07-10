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
        culinary_units = ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]
        if unit_from in culinary_units or unit_to in culinary_units:
            # Density-based conversion for culinary units
            volume_ml = value * volume_units[unit_from]
            if unit_from in culinary_units:
                # Convert measurement to mass (grams) using density
                mass_g = volume_ml * density
                # Convert mass to target volume (mL) using density
                target_volume_ml = mass_g / density
                converted_value = target_volume_ml / volume_units[unit_to]
            else:
                # Convert source volume to mass (grams) using density
                mass_g = volume_ml * density
                # Convert mass to target volume (mL) using density
                target_volume_ml = mass_g / density
                converted_value = target_volume_ml / volume_units[unit_to]
        else:
            # Standard volume-to-volume conversion (no density needed)
            converted_value = (value * volume_units[unit_from]) / volume_units[unit_to]
        return round(converted_value, 4)
    except (ValueError, KeyError):
        return "Invalid input"

# Main content
st.markdown("<h1>UnitSwap: Instant Volume Converter</h1>", unsafe_allow_html=True)
st.write("Instantly swap metric and other volume units to measurements with this user-friendly tool. Enter density for precise culinary conversions! 🚀")

# Unit converter UI
st.subheader("Volume to Measurement Converter")
density = st.number_input("Enter Density (g/mL)", min_value=0.0, value=1.0, step=0.01, help="Enter the density of the substance (e.g., 1.0 for water, 0.53 for flour)")

all_units = ["Liter", "Milliliter", "Cubic Meter", "Gallon (US)", "Gallon (UK)", "Cubic Foot", "Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]
value = st.text_input("Enter Volume Value", "0", help="Enter a volume (e.g., 1 for 1 Liter)")
unit_from = st.selectbox("From Volume Unit", all_units, help="Select the source unit (e.g., Liter, Cup)")
unit_to = st.selectbox("To Volume Unit", all_units, help="Select the target unit (e.g., Cup, Milliliter)")
if st.button("Convert Now"):
    result = convert_volume(value, unit_from, unit_to, density)
    if isinstance(result, str):
        st.error(result)
    else:
        density_note = f" (using density {density} g/mL)" if unit_from in ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"] or unit_to in ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"] else ""
        st.success(f"{value} {unit_from} = {result} {unit_to}{density_note}")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made By Jalen Claytor<div>", unsafe_allow_html=True)
