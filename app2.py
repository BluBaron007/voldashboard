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
    page_title="UnitSwap: Instant Converter",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Apply custom styles
apply_glass_style()

# Main content
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("<h1>UnitSwap: Instant Converter</h1>", unsafe_allow_html=True)
st.write("Convert units instantly with ease. Select a category, enter a value, and get results in real-time! 🚀")

# Sample unit converter UI
category = st.selectbox("Unit Category", ["Length", "Weight", "Temperature", "Volume"])
value = st.text_input("Enter Value", "0")
unit_from = st.selectbox("From Unit", ["Meter", "Kilometer", "Mile"] if category == "Length" else ["Kilogram", "Pound"])
unit_to = st.selectbox("To Unit", ["Meter", "Kilometer", "Mile"] if category == "Length" else ["Kilogram", "Pound"])
if st.button("Convert"):
    st.write(f"Result: {value} {unit_from} = [Converted Value] {unit_to}")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made with ❤️ using Streamlit</div>", unsafe_allow_html=True)
# --- Conversion Dictionaries ---
VOLUME_CONVERSIONS = {
    'mL': 1.0, 'L': 1000.0, 'µL': 0.001, 'dL': 100.0, 'fl oz': 29.5735,
    'cup': 236.588, 'pint': 473.176, 'quart': 946.353, 'gallon': 3785.41,
    'tsp': 4.92892, 'tbsp': 14.7868, 'drop': 0.05
}

VOLUME_TO_MASS_EXAMPLES = {
    'water': 1.0, 'oil': 0.9, 'alcohol': 0.8, 'honey': 1.4,
    'milk': 1.03, 'blood': 1.06, 'mercury': 13.6, 'gasoline': 0.75
}

MASS_CONVERSIONS = {
    'µg': 1.0, 'mg': 1000.0, 'g': 1000000.0, 'kg': 1e9,
    'oz': 28349523.125, 'lb': 453592370.0, 'grain': 64798.91
}

CONCENTRATION_CONVERSIONS = {
    'µg/mL': 1.0, 'mg/mL': 1000.0, 'g/mL': 1e6, 'kg/mL': 1e9,
    'µg/L': 0.001, 'mg/L': 1.0, 'g/L': 1000.0, 'kg/L': 1e6,
    'ppm': 1.0, 'ppb': 0.001, '%': 10000.0, 'M': 'molar', 'mM': 'millimolar'
}

DENSITY_CONVERSIONS = {
    'g/mL': 1.0, 'g/cm³': 1.0, 'kg/L': 1.0, 'kg/m³': 0.001,
    'g/L': 0.001, 'lb/ft³': 0.0160185, 'lb/gal': 0.119826
}

# --- Conversion Functions ---
def convert_volume(value, from_unit, to_unit):
    ml_value = value * VOLUME_CONVERSIONS[from_unit]
    return ml_value / VOLUME_CONVERSIONS[to_unit]

def convert_mass(value, from_unit, to_unit):
    ug_value = value * MASS_CONVERSIONS[from_unit]
    return ug_value / MASS_CONVERSIONS[to_unit]

def convert_concentration(value, from_unit, to_unit, molecular_weight=None):
    if 'M' in from_unit or 'M' in to_unit:
        if not molecular_weight:
            return None
        if from_unit == 'M':
            ug_ml = value * molecular_weight * 1000
        elif from_unit == 'mM':
            ug_ml = value * molecular_weight
        else:
            ug_ml = value * CONCENTRATION_CONVERSIONS[from_unit]
        if to_unit == 'M':
            return ug_ml / (molecular_weight * 1000)
        elif to_unit == 'mM':
            return ug_ml / molecular_weight
        else:
            return ug_ml / CONCENTRATION_CONVERSIONS[to_unit]
    ug_ml = value * CONCENTRATION_CONVERSIONS[from_unit]
    return ug_ml / CONCENTRATION_CONVERSIONS[to_unit]

def convert_density(value, from_unit, to_unit):
    g_ml = value * DENSITY_CONVERSIONS[from_unit]
    return g_ml / DENSITY_CONVERSIONS[to_unit]

def convert_volume_to_mass(volume_value, volume_unit, density_value, density_unit, target_mass_unit):
    volume_ml = volume_value * VOLUME_CONVERSIONS[volume_unit]
    density_g_ml = density_value * DENSITY_CONVERSIONS[density_unit]
    mass_g = volume_ml * density_g_ml
    mass_ug = mass_g * 1e6
    return mass_ug / MASS_CONVERSIONS[target_mass_unit]

def convert_mass_to_volume(mass_value, mass_unit, density_value, density_unit, target_volume_unit):
    mass_ug = mass_value * MASS_CONVERSIONS[mass_unit]
    mass_g = mass_ug / 1e6
    density_g_ml = density_value * DENSITY_CONVERSIONS[density_unit]
    volume_ml = mass_g / density_g_ml
    return volume_ml / VOLUME_CONVERSIONS[target_volume_unit]

# --- Streamlit Interface ---
st.title("Universal Unit Converter")

conversion_type = st.selectbox("Choose conversion type", [
    "Volume", "Mass", "Concentration", "Density", "Volume ↔ Mass"
])

if conversion_type == "Volume":
    value = st.number_input("Enter volume:", value=0.0)
    from_unit = st.selectbox("From unit", VOLUME_CONVERSIONS.keys())
    to_unit = st.selectbox("To unit", VOLUME_CONVERSIONS.keys())
    if st.button("Convert"):
        result = convert_volume(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")

elif conversion_type == "Mass":
    value = st.number_input("Enter mass:", value=0.0)
    from_unit = st.selectbox("From unit", MASS_CONVERSIONS.keys())
    to_unit = st.selectbox("To unit", MASS_CONVERSIONS.keys())
    if st.button("Convert"):
        result = convert_mass(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")

elif conversion_type == "Concentration":
    value = st.number_input("Enter concentration:", value=0.0)
    from_unit = st.selectbox("From unit", CONCENTRATION_CONVERSIONS.keys())
    to_unit = st.selectbox("To unit", CONCENTRATION_CONVERSIONS.keys())
    mw_required = 'M' in from_unit or 'M' in to_unit
    molecular_weight = st.number_input("Molecular weight (g/mol)", value=0.0) if mw_required else None
    if st.button("Convert"):
        result = convert_concentration(value, from_unit, to_unit, molecular_weight or None)
        if result is not None:
            st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")
        else:
            st.error("Molecular weight is required for molar conversions.")

elif conversion_type == "Density":
    value = st.number_input("Enter density:", value=0.0)
    from_unit = st.selectbox("From unit", DENSITY_CONVERSIONS.keys())
    to_unit = st.selectbox("To unit", DENSITY_CONVERSIONS.keys())
    if st.button("Convert"):
        result = convert_density(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")

elif conversion_type == "Volume ↔ Mass":
    direction = st.radio("Choose conversion direction", ["Volume → Mass", "Mass → Volume"])
    value = st.number_input("Enter value:", value=0.0)
    if direction == "Volume → Mass":
        from_unit = st.selectbox("Volume unit", VOLUME_CONVERSIONS.keys())
        to_unit = st.selectbox("Target mass unit", MASS_CONVERSIONS.keys())
    else:
        from_unit = st.selectbox("Mass unit", MASS_CONVERSIONS.keys())
        to_unit = st.selectbox("Target volume unit", VOLUME_CONVERSIONS.keys())
    density_value = st.number_input("Density value", value=1.0)
    density_unit = st.selectbox("Density unit", DENSITY_CONVERSIONS.keys())

    if st.button("Convert"):
        if direction == "Volume → Mass":
            result = convert_volume_to_mass(value, from_unit, density_value, density_unit, to_unit)
            st.success(f"{value} {from_unit} → {result:.6f} {to_unit}")
        else:
            result = convert_mass_to_volume(value, from_unit, density_value, density_unit, to_unit)
            st.success(f"{value} {from_unit} → {result:.6f} {to_unit}")
