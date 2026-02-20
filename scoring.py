import pandas as pd

def calculate_welfare_score(total_schemes, eligible_count):
    if total_schemes == 0: return 0
    return round((eligible_count / total_schemes) * 100, 2)

def estimate_total_benefit(eligible_df):
    benefit_map = {
        "Direct Income Support": 6000, "Health Insurance": 500000,
        "Crop Insurance": 40000, "Scholarship": 15000,
        "Pension": 12000, "Subsidy": 5000
    }
    total = 0
    if not eligible_df.empty:
        for _, row in eligible_df.iterrows():
            b_type = str(row.get("Benefits_Type", "")).strip()
            total += benefit_map.get(b_type, 2000)
    return total

def scheme_breakdown(eligible_df):
    if eligible_df.empty: return 0, 0
    central = eligible_df[eligible_df["Government_Level"] == "Central"]
    state = eligible_df[eligible_df["Government_Level"] == "State"]
    return len(central), len(state)

def recommend_top_scheme(eligible_df, occupation):
    if eligible_df.empty: return None
    occ = occupation.lower()
    
    # Smart prioritization based on occupation
    if "farmer" in occ:
        priority = ["Direct Income Support", "Crop Insurance", "Agricultural Development"]
    elif "student" in occ:
        priority = ["Scholarship", "Skill Training", "Loan"]
    else:
        priority = ["Health Insurance", "Financial Assistance"]

    for p in priority:
        match = eligible_df[eligible_df["Benefits_Type"] == p]
        if not match.empty: return match.iloc[0]
        
    return eligible_df.iloc[0]