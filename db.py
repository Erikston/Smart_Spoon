# db.py
from pathlib import Path
import sqlite3

DB_PATH = Path("smart_spoon.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS smart_spoon_survey (
            age INTEGER,
            gender TEXT,
            low_sodium_diet TEXT,
            diet_condition TEXT,
            dining_frequency TEXT,
            low_sodium_satisfaction TEXT,
            add_salt_condiments TEXT,
            taste_enhancement_tech_aware TEXT,
            interest_in_device TEXT,
            importance_of_taste_enhancement TEXT,
            expected_device_features TEXT,
            purchase_consideration TEXT,
            concerns_on_technology TEXT,
            salt_usage_dal_gojju_palya TEXT,
            salt_usage_sambar_rasam_curd TEXT,
            salt_usage_biryani_pulao_rice TEXT,
            salt_usage_curry TEXT,
            salt_usage_snacks TEXT,
            salt_usage_roti_paratha TEXT,
            salt_usage_pickles_papad TEXT,
            salt_opinion TEXT
        );
        """)
        # Optional view for faster charts
        conn.execute("""
        CREATE VIEW IF NOT EXISTS avg_purchase_by_age_group AS
        SELECT
          CASE
            WHEN age BETWEEN 0 AND 30 THEN '18-30'
            WHEN age BETWEEN 31 AND 50 THEN '31-50'
            WHEN age BETWEEN 51 AND 70 THEN '51-70'
            ELSE 'Other'
          END AS age_group,
          AVG(
            CASE purchase_consideration
              WHEN 'Yes' THEN 1.0
              WHEN 'Maybe' THEN 0.5
              ELSE 0.0
            END
          ) AS avg_consideration
        FROM smart_spoon_survey
        GROUP BY age_group;
        """)
