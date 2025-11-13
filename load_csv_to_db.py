# load_csv_to_db.py
import pandas as pd
from db import get_conn, init_db

CSV_PATH = "expanded_smart_spoon_market_research.csv"
TABLE = "smart_spoon_survey"

def main():
    init_db()
    df = pd.read_csv(CSV_PATH)

    # Normalize column names to match SQL schema
    rename_map = {
        "Age": "age",
        "Gender": "gender",
        "Low_Sodium_Diet": "low_sodium_diet",
        "Diet_Condition": "diet_condition",
        "Dining_Frequency": "dining_frequency",
        "Low_Sodium_Satisfaction": "low_sodium_satisfaction",
        "Add_Salt_Condiments": "add_salt_condiments",
        "Taste_Enhancement_Tech_Aware": "taste_enhancement_tech_aware",
        "Interest_In_Device": "interest_in_device",
        "Importance_Of_Taste_Enhancement": "importance_of_taste_enhancement",
        "Expected_Device_Features": "expected_device_features",
        "Purchase_Consideration": "purchase_consideration",
        "Concerns_On_Technology": "concerns_on_technology",
        "Salt_Usage_Dal_Gojju_Palya": "salt_usage_dal_gojju_palya",
        "Salt_Usage_Sambar_Rasam_Curd": "salt_usage_sambar_rasam_curd",
        "Salt_Usage_Biryani_Pulao_Rice": "salt_usage_biryani_pulao_rice",
        "Salt_Usage_Curry": "salt_usage_curry",
        "Salt_Usage_Snacks": "salt_usage_snacks",
        "Salt_Usage_Roti_Paratha": "salt_usage_roti_paratha",
        "Salt_Usage_Pickles_Papad": "salt_usage_pickles_papad",
        "Salt_Opinion": "salt_opinion",
    }
    df = df.rename(columns=rename_map)

    # Enforce dtypes where possible
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

    with get_conn() as conn:
        df.to_sql(TABLE, conn, if_exists="replace", index=False)

if __name__ == "__main__":
    main()
