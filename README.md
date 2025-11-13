# Smart_Spoon
A Streamlit app demonstrating food image analysis, SQL-backed market research insights, and quick sentiment analysis for a Smart Spoon concept.

Live Demo
https://smartspoongit-cxae2giwh4pwg2r7qjfdmt.streamlit.app/

🚀 Key Features

Food Recognition

Upload a food image and get estimated salt-related intensity using simple HSV/texture cues via OpenCV, plus a recommended stimulation level.

Market Research (SQL)

The survey CSV is ingested into SQLite (smart_spoon.db → smart_spoon_survey), and charts read data with SELECT queries for a consistent source of truth.

Sentiment Analysis

Analyze user feedback with TextBlob polarity scoring and quick positive/negative keyword hints.

🛠️ Tech Stack

Category	Technology	Description
Core	Python	Primary language
Frontend	Streamlit	Interactive multi-tab app
Data	SQLite, Pandas	Persistent store + DataFrames
Visualization	Plotly Express	Interactive charts
CV	OpenCV (headless)	HSV and texture features
NLP	TextBlob	Sentiment polarity
📦 Getting Started

Prerequisites

Python 3.10+

pip

Installation

Clone

git clone https://github.com/<your-username>/<your-repo>.git

cd <your-repo>

(Optional) Virtual environment

python -m venv .venv

Windows: .venv\Scripts\activate

macOS/Linux: source .venv/bin/activate

Install packages

pip install -r requirements.txt
If you don’t use a requirements file:

pip install streamlit pandas numpy plotly textblob pillow opencv-python-headless

Load survey into SQLite

python load_csv_to_db.py
This creates smart_spoon.db and table smart_spoon_survey from expanded_smart_spoon_market_research.csv.

Running Locally

streamlit run smart_spoon_analytics.py
Open the local URL (usually http://localhost:8501) and explore the three tabs.

💻 Usage

Food Recognition:

Upload an image → click Analyze → view Estimated Salt Content, Flavor Intensity, and Recommended Stimulation.

Market Research:

Charts for Age distribution, Purchase Consideration by age bucket, Top Requested Features, Diet Conditions; all sourced from SQL.

Sentiment Analysis:

Paste feedback text → Analyze → see sentiment score and detected themes.

📂 Project Structure

smart_spoon_analytics.py — Streamlit app entry.

db.py — DB helpers (connection, table/view creation).

load_csv_to_db.py — ETL from CSV to SQLite.

expanded_smart_spoon_market_research.csv — Survey data.

requirements.txt — Dependencies for local/cloud.

🗄️ SQL Usage

Ingestion: Pandas to_sql writes the CSV to SQLite as smart_spoon_survey.

Query: The app executes SELECT * FROM smart_spoon_survey and then applies light transformations (age groups, Yes/Maybe/No mapping).

Optional view: A sample view for age-group purchase interest is included in db.py.

📝 License

MIT (or your chosen license). Add a LICENSE file in the repo root.

📬 Contact

Live app: https://smartspoongit-cxae2giwh4pwg2r7qjfdmt.streamlit.app/

GitHub: https://github.com/Erikston/Smart_Spoon/

Email: uarbrb@gmail.com

💖 Thanks
Thanks for exploring Smart Spoon Analytics! Feedback and suggestions are welcome to improve the analytics, SQL modeling, and user experience.

