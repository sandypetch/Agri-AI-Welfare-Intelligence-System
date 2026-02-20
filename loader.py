import pandas as pd
import os

def load_all_schemes(state):
    base_path = "data"
    central_path = os.path.join(base_path, "Central_Schemes.xlsx")
    state_path = os.path.join(base_path, "State_Schemes.xlsx")

    try:
        central = pd.read_excel(central_path)
        states = pd.read_excel(state_path)
        
        # CLEAN COLUMN NAMES: Standardizes headers like 'Scheme Name' to 'Scheme_Name'
        for df in [central, states]:
            df.columns = df.columns.str.strip().str.replace(' ', '_')
            
    except Exception as e:
        raise Exception(f"Excel Load Error: Ensure files are in the 'data' folder. {e}")

    # Robust State filtering
    states['State_Match'] = states['State'].astype(str).str.replace(" ", "").str.lower()
    state_filtered = states[states["State_Match"] == state.lower()]
    
    return pd.concat([central, state_filtered], ignore_index=True)