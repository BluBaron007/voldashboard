import streamlit as st
import logging

# Configure logging for debugging (especially for Streamlit Cloud)
logging.basicConfig(filename='converter_errors.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

# Conversion logic
def convert_units(value, unit_from, unit_to, density=1.0):
    # Conversion factors
    mass_units = {
        "Milligram": 0.001,  # to grams
        "Gram": 1.0,
        "Kilogram": 1000.0
    }
    volume_units = {
        "Liter": 1000.0,  # to milliliters
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
            logging.error(f"Negative value input: {value}")
            return "Value must be non-negative"
        if unit_from == unit_to:
            return value
        if density <= 0 and (unit_from in ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"] or 
                             unit_to in ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"] or 
                             unit_from in mass_units or unit_to in mass_units):
            logging.error(f"Invalid density: {density} for units {unit_from} to {unit_to}")
            return "Density must be greater than zero for culinary or mass-volume conversions"
            
        culinary_units = ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]
        mass_to_mass = unit_from in mass_units and unit_to in mass_units
        volume_to_volume = unit_from in volume_units and unit_to in volume_units
        mass_to_volume = unit_from in mass_units and unit_to in volume_units
        volume_to_mass = unit_from in volume_units and unit_to in mass_units
        
        if mass_to_mass:
            # Direct mass-to-mass conversion
            converted_value = (value * mass_units[unit_from]) / mass_units[unit_to]
        elif volume_to_volume and unit_from not in culinary_units and unit_to not in culinary_units:
            # Direct volume-to-volume conversion (non-culinary)
            converted_value = (value * volume_units[unit_from]) / volume_units[unit_to]
        elif mass_to_volume:
            # Mass to volume/culinary conversion
            mass_g = value * mass_units[unit_from]
            volume_ml = mass_g / density
            converted_value = volume_ml / volume_units[unit_to]
        elif volume_to_mass:
            # Volume/culinary to mass conversion
            volume_ml = value * volume_units[unit_from]
            mass_g = volume_ml * density
            converted_value = mass_g / mass_units[unit_to]
        else:
            # Culinary to culinary or volume to culinary or culinary to volume
            volume_ml = value * volume_units[unit_from]
            mass_g = volume_ml * density
            target_volume_ml = mass_g / density
            converted_value = target_volume_ml / volume_units[unit_to]
            
        return round(converted_value, 4)
    except (ValueError, KeyError) as e:
        logging.error(f"Conversion error: {str(e)}, Input: {value}, From: {unit_from}, To: {unit_to}, Density: {density}")
        return f"Invalid input: {str(e)}"

# Main content
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("<h1>UnitSwap: Instant Converter</h1>", unsafe_allow_html=True)
st.write("Instantly swap metric mass and volume units to measurements with this user-friendly tool. Enter density for precise culinary conversions! 🚀")

# Unit converter UI
st.subheader("Mass and Volume Converter")
value = st.text_input("Enter Value", "0", help="Enter a mass or volume (e.g., 1 for 1 Liter or 1 Gram)")
all_units = ["Milligram", "Gram", "Kilogram", "Liter", "Milliliter", "Cubic Meter", 
             "Gallon (US)", "Gallon (UK)", "Cubic Foot", "Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]
unit_from = st.selectbox("From Unit", all_units, help="Select the source unit (e.g., Gram, Liter, Cup)")
unit_to = st.selectbox("To Unit", all_units, help="Select the target unit (e.g., Cup, Kilogram, Milliliter)")

# Conditional density input
culinary_units = ["Cup", "Tablespoon", "Teaspoon", "Fluid Ounce"]
mass_units = ["Milligram", "Gram", "Kilogram"]
density = 1.0  # Default density
if (unit_from in culinary_units or unit_to in culinary_units or 
    (unit_from in mass_units and unit_to in volume_units) or 
    (unit_from in volume_units and unit_to in mass_units)):
    density = st.number_input("Enter Density (g/mL)", min_value=0.0, value=1.0, step=0.01, 
                             help="Enter the density of the substance (e.g., 1.0 for water, 0.53 for flour)")

if st.button("Convert Now"):
    result = convert_units(value, unit_from, unit_to, density)
    if isinstance(result, str):
        st.error(result)
    else:
        density_note = f" (using density {density} g/mL)" if (unit_from in culinary_units or 
                                                             unit_to in culinary_units or 
                                                             unit_from in mass_units or 
                                                             unit_to in mass_units) else ""
        st.success(f"{value} {unit_from} = {result} {unit_to}{density_note}")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made with ❤️ using Streamlit</div>", unsafe_allow_html=True)
