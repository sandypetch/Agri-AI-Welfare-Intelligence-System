import pandas as pd
from engine.loader import load_all_schemes

def check_eligibility(user, scheme):
    reasons = []
    
    # 1. Age Logic
    min_age = pd.to_numeric(scheme["Min_Age"], errors="coerce")
    max_age = pd.to_numeric(scheme["Max_Age"], errors="coerce")
    if pd.notna(min_age) and user["age"] < min_age:
        reasons.append(f"You are {user['age']} years old, but this scheme requires a minimum age of {min_age}.")
    if pd.notna(max_age) and user["age"] > max_age:
        reasons.append(f"At {user['age']}, you exceed the maximum age limit ({max_age}) for this specific benefit.")

    # 2. Income Logic
    income_limit = pd.to_numeric(scheme["Income_Limit"], errors="coerce")
    if pd.notna(income_limit) and user["income"] > income_limit:
        reasons.append(f"Your annual income (₹{user['income']:,}) is above the eligibility threshold of ₹{income_limit:,}.")

    # 3. Demographic Logic
    for field in ["Gender", "Category", "Occupation"]:
        if pd.notna(scheme[field]):
            s_val = str(scheme[field]).strip().lower()
            u_val = str(user[field.lower()]).strip().lower()
            if s_val != "all" and s_val != u_val:
                reasons.append(f"This scheme is specifically for {s_val} applicants, which does not match your profile ({u_val}).")

    # 4. Land Logic (Agritech)
    if user["occupation"].lower() == "farmer":
        desc = str(scheme["Description"]).lower()
        if ("small" in desc or "marginal" in desc) and user["land_size"] > 5.0:
            reasons.append(f"Your land size ({user['land_size']} acres) is too large for this 'Small/Marginal Farmer' scheme (max 5 acres).")

    return (True, []) if not reasons else (False, reasons)

def analyze_schemes(user, state):
    df = load_all_schemes(state)
    eligible, not_eligible = [], []
    for _, scheme in df.iterrows():
        status, reasons = check_eligibility(user, scheme)
        s_data = scheme.to_dict()
        if status: 
            eligible.append(s_data)
        else:
            s_data["Reason"] = " ".join(reasons) # Cleaner text join
            not_eligible.append(s_data)
    return pd.DataFrame(eligible), pd.DataFrame(not_eligible)