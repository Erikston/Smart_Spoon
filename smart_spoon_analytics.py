import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from textblob import TextBlob
from PIL import Image
import cv2

from db import get_conn

# -----------------------
# Session State
# -----------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Food Recognition"

# -----------------------
# Data Loading (SQL)
# -----------------------
@st.cache_data
def load_data():
    with get_conn() as conn:
        df = pd.read_sql_query("SELECT * FROM smart_spoon_survey", conn)

    # Map lowercase DB columns to Title Case expected by charts
    if "age" in df.columns:
        df["Age"] = df["age"]
    if "purchase_consideration" in df.columns:
        df["Purchase_Consideration"] = df["purchase_consideration"]
    if "expected_device_features" in df.columns:
        df["Expected_Device_Features"] = df["expected_device_features"]
    if "diet_condition" in df.columns:
        df["Diet_Condition"] = df["diet_condition"]

    # Same preprocessing as before
    df["Age_Group"] = pd.cut(df["Age"], bins=[0, 30, 50, 70], labels=["18-30", "31-50", "51-70"])
    df["Purchase_Consideration"] = df["Purchase_Consideration"].map({"Yes": 1, "Maybe": 0.5, "No": 0})
    return df

# -----------------------
# Image Analysis
# -----------------------
def analyze_food(image):
    img_array = np.array(image)
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    color_hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    avg_saturation = np.mean(hsv[:, :, 1])
    avg_brightness = np.mean(hsv[:, :, 2])
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    texture = np.var(laplacian)
    return {
        "avg_saturation": avg_saturation,
        "avg_brightness": avg_brightness,
        "texture": texture,
        "color_hist": color_hist,
    }

# -----------------------
# App Sections
# -----------------------
def food_recognition():
    st.title("🍽️ Food Recognition System")
    st.write("Upload an image of food to estimate salt content and get taste enhancement recommendations")

    uploaded_file = st.file_uploader("Choose a food image", type=["jpg", "png", "jpeg"], key="food_upload")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Food Image", use_column_width=True)

        if st.button("Analyze Food", key="analyze_food"):
            with st.spinner("Analyzing food and estimating salt content..."):
                analysis = analyze_food(image)
                st.success("Analysis Complete!")

                st.subheader("Results")
                col1, col2 = st.columns(2)

                salt_estimate = "Medium"
                if analysis["avg_saturation"] > 100:
                    salt_estimate = "High"
                elif analysis["avg_saturation"] < 50:
                    salt_estimate = "Low"

                food_type = "Unknown"
                if analysis["texture"] > 1000:
                    food_type = "Curry/Dal"
                elif analysis["texture"] < 500:
                    food_type = "Soup"
                else:
                    food_type = "Solid Food"

                with col1:
                    st.metric(
                        "Estimated Salt Content",
                        salt_estimate,
                        f"{'+25%' if salt_estimate == 'High' else ('-15%' if salt_estimate == 'Low' else 'Normal')} vs recommended",
                    )
                    st.metric("Food Category", food_type)

                with col2:
                    stim_level = min(5, max(1, int(analysis["avg_saturation"] / 40)))
                    st.metric("Recommended Stimulation", f"Level {stim_level}")
                    st.metric(
                        "Flavor Intensity",
                        "Strong" if analysis["avg_saturation"] > 100 else ("Mild" if analysis["avg_saturation"] < 50 else "Medium"),
                    )

                st.progress(int(analysis["avg_saturation"] / 2.55))
                if salt_estimate == "High":
                    st.caption("Device adjustment recommendation: Reduce saltiness by 25%")
                elif salt_estimate == "Low":
                    st.caption("Device adjustment recommendation: Enhance saltiness by 15%")
                else:
                    st.caption("Device adjustment recommendation: Maintain current flavor profile")

def market_analysis(df):
    st.title("📊 Market Research Insights")
    st.write("Analyzing consumer preferences from survey data")

    st.subheader("Dataset Overview")
    st.write(f"Total respondents: {len(df)}")

    st.subheader("Age Distribution")
    age_fig = px.histogram(df, x="Age", nbins=10, title="Respondent Age Distribution")
    st.plotly_chart(age_fig, use_container_width=True)

    st.subheader("Purchase Consideration by Age Group")
    purchase_age = df.groupby("Age_Group")["Purchase_Consideration"].mean().reset_index()
    purchase_fig = px.bar(purchase_age, x="Age_Group", y="Purchase_Consideration", title="Average Purchase Consideration by Age Group")
    st.plotly_chart(purchase_fig, use_container_width=True)

    st.subheader("Most Desired Features")
    features = df["Expected_Device_Features"].fillna("").str.split(", ", expand=True).stack()
    feature_counts = features[features.str.len() > 0].value_counts().reset_index()
    feature_counts.columns = ["Feature", "Count"]
    feature_fig = px.bar(feature_counts, x="Feature", y="Count", title="Most Requested Features")
    st.plotly_chart(feature_fig, use_container_width=True)

    st.subheader("Diet Conditions Among Respondents")
    diet_counts = df["Diet_Condition"].value_counts(dropna=False).reset_index()
    diet_counts.columns = ["Condition", "Count"]
    diet_fig = px.pie(diet_counts, names="Condition", values="Count", title="Distribution of Diet Conditions")
    st.plotly_chart(diet_fig, use_container_width=True)

def sentiment_analysis():
    st.title("😊 User Feedback Analysis")
    st.write("Analyze user sentiment from feedback text")

    sample_feedback = """
    The smart spoon really helped me reduce my salt intake. I have hypertension and this device makes low-sodium food taste better.
    I'm not sure about the price point though - it seems expensive for what it does.
    The battery life could be improved.
    """
    user_feedback = st.text_area("Enter user feedback:", value=sample_feedback, height=150, key="feedback_text")

    if st.button("Analyze Sentiment", key="analyze_sentiment"):
        if user_feedback:
            analysis = TextBlob(user_feedback)
            sentiment = analysis.sentiment.polarity

            st.subheader("Results")
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.metric("Sentiment Score", f"{sentiment:.2f}")
                st.progress(int((sentiment + 1) * 50))

            if sentiment > 0.3:
                st.success("Strong Positive Sentiment")
            elif sentiment > 0.1:
                st.success("Positive Sentiment")
            elif sentiment < -0.3:
                st.error("Strong Negative Sentiment")
            elif sentiment < -0.1:
                st.error("Negative Sentiment")
            else:
                st.info("Neutral Sentiment")

            st.subheader("Key Themes")
            tags = {
                "positive": ["help", "improve", "better", "good", "love", "great"],
                "negative": ["expensive", "issue", "problem", "bad", "hate", "worse"],
            }
            pos_count = sum(user_feedback.lower().count(word) for word in tags["positive"])
            neg_count = sum(user_feedback.lower().count(word) for word in tags["negative"])
            st.write(f"Positive keywords detected: {pos_count}")
            st.write(f"Negative keywords detected: {neg_count}")

            if neg_count > 0:
                st.warning("Negative feedback detected about: ")
                for word in tags["negative"]:
                    if word in user_feedback.lower():
                        st.write(f"- {word}")
        else:
            st.warning("Please enter feedback to analyze")

# -----------------------
# Main App
# -----------------------
def main():
    st.set_page_config(page_title="Smart Spoon Analytics", layout="wide")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍽️ Food Recognition", use_container_width=True):
            st.session_state.active_tab = "Food Recognition"
    with col2:
        if st.button("📊 Market Research", use_container_width=True):
            st.session_state.active_tab = "Market Research"
    with col3:
        if st.button("😊 Sentiment Analysis", use_container_width=True):
            st.session_state.active_tab = "Sentiment Analysis"

    st.markdown("---")

    df = load_data()

    if st.session_state.active_tab == "Food Recognition":
        food_recognition()
    elif st.session_state.active_tab == "Market Research":
        market_analysis(df)
    elif st.session_state.active_tab == "Sentiment Analysis":
        sentiment_analysis()

if __name__ == "__main__":
    main()